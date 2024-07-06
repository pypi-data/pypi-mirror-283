import os
from os.path import expanduser
import urllib.request
import tarfile
from loguru import logger
import json
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich import print as rprint

from byzerllm.apps.byzer_storage.env import get_latest_byzer_retrieval_lib
from byzerllm.apps.byzer_storage import env

console = Console()

class StorageSubCommand:
        
    @staticmethod
    def install(args):
        version = args.version
        home = expanduser("~")        
        base_dir = args.base_dir or os.path.join(home, ".auto-coder")
        libs_dir = os.path.join(base_dir, "storage", "libs", f"byzer-retrieval-lib-{version}")
        if os.path.exists(libs_dir):
            print(f"Byzer Storage version {version} already installed.")
            return
        
        if not os.path.exists(base_dir):
            os.makedirs(base_dir,exist_ok=True)            

        env_info = env.detect_env()

        logger.info("Current environment:")
        logger.info(env_info)
        
        if env_info.java_version == "" or int(env_info.java_version) < 21:
            logger.info("JDK 21 not found, downloading and installing JDK 21...")
            try:
                env.download_and_install_jdk21(env_info, base_dir)
            except Exception as e:
                logger.error(f"Error downloading and installing JDK 21: {str(e)}. You may need to install JDK 21 manually.")
                        
        download_url = f"https://download.byzer.org/byzer-retrieval/byzer-retrieval-lib-{version}.tar.gz"
        libs_dir = os.path.join(base_dir, "storage", "libs")
        
        os.makedirs(libs_dir, exist_ok=True)
        download_path = os.path.join(libs_dir, f"byzer-retrieval-lib-{version}.tar.gz")
        if os.path.exists(download_path):
            logger.info(f"Byzer Storage version {version} already downloaded.")
        else:             
            def download_with_progressbar(url, filename):
                def progress(count, block_size, total_size):
                    percent = int(count * block_size * 100 / total_size)
                    print(f"\rDownload progress: {percent}%", end="")
            
                urllib.request.urlretrieve(url, filename,reporthook=progress)                
  
            logger.info(f"Download Byzer Storage version {version}: {download_url}")
            download_with_progressbar(download_url, download_path)    

            with tarfile.open(download_path, "r:gz") as tar:
                tar.extractall(path=libs_dir)
        
        print("Byzer Storage installed successfully")

    def collection(args):        
        from byzerllm.apps.llama_index.collection_manager import CollectionManager, CollectionItem
        home = expanduser("~")        
        base_dir = args.base_dir or os.path.join(home, ".auto-coder")
        collection_manager = CollectionManager(base_dir)
        if args.name:            
            collection = CollectionItem(name=args.name, description=args.description)
            collection_manager.add_collection(collection)
            print(f"Collection {args.name} added successfully.")
        else:
            print("Please provide collection name.")    
    
    @staticmethod
    def start(args):
        import byzerllm
        from byzerllm.utils.retrieval import ByzerRetrieval
        version = args.version
        cluster = args.cluster
        home = expanduser("~")        
        base_dir = args.base_dir or os.path.join(home, ".auto-coder")
        
        with console.status("[bold green]Starting Byzer Storage...") as status:
            libs_dir = os.path.join(base_dir, "storage", "libs", f"byzer-retrieval-lib-{version}")
            data_dir = os.path.join(base_dir, "storage", "data")

            if not os.path.exists(os.path.join(data_dir,cluster)):
                os.makedirs(data_dir,exist_ok=True)
                rprint("[green]✓[/green] Created data directory")

            if not os.path.exists(libs_dir):            
                StorageSubCommand.install(args)
                rprint("[green]✓[/green] Installed Byzer Storage")

            code_search_path = [libs_dir]
            
            status.update("[bold blue]Connecting to cluster...")
            env_vars = byzerllm.connect_cluster(address=args.ray_address,code_search_path=code_search_path)
            rprint("[green]✓[/green] Connected to cluster")
            
            retrieval = ByzerRetrieval()
            retrieval.launch_gateway()
            rprint("[green]✓[/green] Launched gateway")

            if retrieval.is_cluster_exists(name=cluster):
                console.print(Panel(f"[yellow]Cluster {cluster} already exists. Please stop it first.[/yellow]"))
                return 
            
            base_model_dir = os.path.join(base_dir, "storage","models")
            os.makedirs(base_model_dir,exist_ok=True)
            bge_model = os.path.join(base_model_dir,"AI-ModelScope","bge-large-zh")
            
            status.update("[bold blue]Downloading embedding model...")
            from modelscope.hub.snapshot_download import snapshot_download
            import huggingface_hub
            if not os.path.exists(bge_model):
                model_path = snapshot_download(
                    model_id="AI-ModelScope/bge-large-zh",
                    cache_dir=base_model_dir,
                    local_files_only=huggingface_hub.constants.HF_HUB_OFFLINE                
                )
            else:
                model_path = bge_model        
            rprint(f"[green]✓[/green] Embedding model downloaded: {model_path}")

            llm = byzerllm.ByzerLLM()        
            if not llm.is_model_exist("emb"): 
                status.update("[bold blue]Deploying embedding model...")
                from byzerllm.utils.client import InferBackend         
                llm.setup_num_workers(1).setup_infer_backend(InferBackend.Transformers)
                llm.setup_gpus_per_worker(0).setup_cpus_per_worker(0.01).setup_worker_concurrency(20)
                llm.deploy(
                    model_path=bge_model,
                    pretrained_model_type="custom/bge",
                    udf_name="emb",            
                    infer_params={}
                )               
                rprint("[green]✓[/green] Deployed embedding model")
            
            cluster_json = os.path.join(base_dir, "storage", "data",f"{cluster}.json")
            if os.path.exists(cluster_json):
                StorageSubCommand.restore(args)
                console.print(Panel("[green]Byzer Storage restored and started successfully[/green]"))
                return 
                
            status.update("[bold blue]Starting cluster...")
            builder = retrieval.cluster_builder()
            builder.set_name(cluster).set_location(data_dir).set_num_nodes(1).set_node_cpu(1).set_node_memory("2g")
            builder.set_java_home(env_vars["JAVA_HOME"]).set_path(env_vars["PATH"]).set_enable_zgc()
            builder.start_cluster()
            
            with open(os.path.join(base_dir, "storage", "data",f"{cluster}.json"),"w") as f:
                f.write(json.dumps(retrieval.cluster_info(cluster),ensure_ascii=False))
            
            console.print(Panel("[green]Byzer Storage started successfully[/green]"))
        

    @staticmethod 
    def stop(args):    
        import byzerllm
        from byzerllm.utils.retrieval import ByzerRetrieval
        version = args.version
        cluster = args.cluster
        home = expanduser("~")        
        base_dir = args.base_dir or os.path.join(home, ".auto-coder")
        libs_dir = os.path.join(base_dir, "storage", "libs", f"byzer-retrieval-lib-{version}")
        cluster_json = os.path.join(base_dir, "storage", "data",f"{cluster}.json")        

        if not os.path.exists(cluster_json) or not os.path.exists(libs_dir):
            print("No instance find.")
            return

        code_search_path = [libs_dir]
        
        logger.info(f"Connect and start Byzer Retrieval version {version}")
        byzerllm.connect_cluster(address=args.ray_address,code_search_path=code_search_path)             
        retrieval = ByzerRetrieval()
        retrieval.launch_gateway()
        retrieval.shutdown_cluster(cluster_name=cluster)

    @staticmethod 
    def export(args):   
        import byzerllm
        from byzerllm.utils.retrieval import ByzerRetrieval
        version = args.version
        cluster = args.cluster
        home = expanduser("~")        
        base_dir = args.base_dir or os.path.join(home, ".auto-coder")
        libs_dir = os.path.join(base_dir, "storage", "libs", f"byzer-retrieval-lib-{version}")
        cluster_json = os.path.join(base_dir, "storage", "data",f"{cluster}.json")        

        if not os.path.exists(cluster_json) or not os.path.exists(libs_dir):
            print("No instance find.")
            return

        code_search_path = [libs_dir]
        
        logger.info(f"Connect and restore Byzer Retrieval version {version}")
        byzerllm.connect_cluster(address=args.ray_address,code_search_path=code_search_path)        
     
        retrieval = ByzerRetrieval()
        retrieval.launch_gateway()
        
        with open(cluster_json,"w") as f:
            f.write(json.dumps(retrieval.cluster_info(cluster),ensure_ascii=False))

        print(f"Byzer Storage export successfully. Please check {cluster_json}")    


    
    def restore(args):
        import byzerllm
        from byzerllm.utils.retrieval import ByzerRetrieval
        version = args.version
        cluster = args.cluster
        home = expanduser("~")        
        base_dir = args.base_dir or os.path.join(home, ".auto-coder")
        libs_dir = os.path.join(base_dir, "storage", "libs", f"byzer-retrieval-lib-{version}")
        cluster_json = os.path.join(base_dir, "storage", "data",f"{cluster}.json")

        if not os.path.exists(cluster_json) or not os.path.exists(libs_dir):
            print("No instance find.")
            return

        code_search_path = [libs_dir]
        
        logger.info(f"Connect and restore Byzer Retrieval version {version}")
        byzerllm.connect_cluster(address=args.ray_address,code_search_path=code_search_path)        
     
        retrieval = ByzerRetrieval()
        retrieval.launch_gateway()

        if not retrieval.is_cluster_exists(cluster):
            with open(cluster_json,"r") as f:
                cluster_info = f.read()
            
            retrieval.restore_from_cluster_info(json.loads(cluster_info))
            
            print("Byzer Storage restore successfully")
        else:
            print(f"Cluster {cluster} is already exists")

