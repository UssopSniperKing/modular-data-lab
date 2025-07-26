from pathlib import Path
import shutil
import importlib.util
import traceback
from modular_data_lab.templates import get_templates
from zipfile import ZipFile
from datetime import datetime

def get_project_root() -> Path | None:
    """Get the root directory of the project
    Returns:
        Path | None: The root directory path or None if not found
    """

    current_path = Path.cwd()

    # Check if the current directory is the root
    if (current_path / "modules").exists() and (current_path / "data").exists():
        return current_path
    
    # Traverse up the directory tree to find the root
    for parent in current_path.parents:
        if (parent / "modules").exists() and (parent / "data").exists():
            return parent
    return None


def create_module(module_name: str) -> None:
    """Create a new module with its structure
    Args:
        module_name (str): Name of the module to create
    """
    project_root = get_project_root()
    if project_root is None:
        print("❌ Project root not found. You're not in a modular data lab project.")
        print("💡 Run 'lab setup' to initialize the project structure")
        return


    module_dir = project_root / f"modules/{module_name}"
    data_dir = project_root / f"data/{module_name}"

    module_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Get templates
    files = get_templates()
    files = {filename: content.format(module_name=module_name) for filename, content in files.items()}

    # Write files
    for filename, content in files.items():
        with open(module_dir / filename, "w") as f:
            f.write(content)
    
    print(f"✅ Module '{module_name}' created:")
    print(f"   📁 modules/{module_name}/")
    print(f"   📁 data/{module_name}/")
    print(f"   📄 Files: {', '.join(files.keys())}")


def list_modules() -> None:
    """List all available modules"""

    project_root = get_project_root()
    if project_root is None:
        print("❌ Project root not found. You're not in a modular data lab project.")
        print("💡 Run 'lab setup' to initialize the project structure")
        return

    modules_dir = project_root / "modules"

    if not modules_dir.exists():
        print("❌ Modules directory does not exist")
        print("💡 Run 'lab setup' to initialize the project structure")
        return
    
    # Get all directories in the modules directory
    modules = [d.name for d in modules_dir.iterdir() if d.is_dir()]
    
    if not modules:
        print("📋 No module found")
        print("💡 Use 'lab add <module_name>'")
        return

    print(f"📋 Available Modules ({len(modules)}):")
    for module in sorted(modules):
        data_path = Path(f"data/{module}")
        
        if data_path.exists():
            # Get all files in the data directory
            data_files = [f for f in data_path.rglob("*") if f.is_file()]
            
            if data_files:
                # Compute total size of data files
                total_size = sum(f.stat().st_size for f in data_files)
                data_info = f"({len(data_files)} fichiers, {format_size(total_size)})"
            else:
                data_info = "(no data)"
        else:
            data_info = "(no data)"
        
        print(f"   📦 {module} {data_info}")


def run_module(module_name: str) -> None:
    """Run a specific module
    Args:
        module_name (str): Name of the module to run
    """
    project_root = get_project_root()
    if project_root is None:
        print("❌ Project root not found. You're not in a modular data lab project.")
        print("💡 Run 'lab setup' to initialize the project structure")
        return

    module_path = project_root / f"modules/{module_name}/run.py"

    if not module_path.exists():
        print(f"❌ Module '{module_name}' not found")
        return False
    
    try:
        print(f"▶️  Running: {module_name}")

        # Import and run the module
        spec = importlib.util.spec_from_file_location("module", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Execute the module's run function
        if hasattr(module, 'run'):
            module.run()
            print(f"✅ Module '{module_name}' finished")
            return True
        else:
            print(f"❌ Function 'run' not found in {module_name}")
            return False
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        traceback.print_exc()
        return False


def remove_module(module_name: str) -> None:
    """Remove a module (modules and data directories)
    Args:
        module_name (str): Name of the module to remove
    """
    project_root = get_project_root()
    if project_root is None:
        print("❌ Project root not found. You're not in a modular data lab project.")
        return

    module_dir = project_root / f"modules/{module_name}"
    data_dir = project_root / f"data/{module_name}"

    if not module_dir.exists():
        print(f"❌ Module '{module_name}' not found")
        return
    
    # Confirmation
    response = input(f"⚠️  Remove module '{module_name}' and its data? (y/N): ")
    if response.lower() != 'y':
        print("❌ Deletion canceled")
        return

    # Deletion
    if module_dir.exists():
        shutil.rmtree(module_dir)
        print(f"✅ Folder modules/{module_name}/ removed")
    
    if data_dir.exists():
        shutil.rmtree(data_dir)
        print(f"✅ Folder data/{module_name}/ removed")


def backup_modules(target_dir: str, module_name: str = None, data_only: bool = False, code_only: bool = False) -> None:
    """Backup modules to a zip file
    Args:
        target_dir (str): Target directory for the backup
        module_name (str, optional): Specific module to backup, None for all
        data_only (bool): Backup only data directories
        code_only (bool): Backup only code directories
    """
    
    # Validation du projet
    project_root = get_project_root()
    if project_root is None:
        print("❌ Project root not found. You're not in a modular data lab project.")
        return
    
    # Validation du répertoire cible
    target_dir = Path(target_dir)
    if not target_dir.exists():
        print(f"❌ Target directory '{target_dir}' does not exist")
        return
    
    if not target_dir.is_dir():
        print(f"❌ '{target_dir}' is not a directory")
        return
    
    # Validation des flags
    if data_only and code_only:
        print("❌ Cannot use both --data and --code flags together")
        return
    
    # Déterminer les modules à sauvegarder
    modules_dir = project_root / "modules"
    if not modules_dir.exists():
        print("❌ No modules directory found")
        return
    
    if module_name:
        # Module spécifique
        if not (modules_dir / module_name).exists():
            print(f"❌ Module '{module_name}' not found")
            return
        modules = [module_name]
    else:
        # Tous les modules
        modules = [d.name for d in modules_dir.iterdir() if d.is_dir()]
        if not modules:
            print("❌ No modules found to backup")
            return
    
    # Créer le nom du fichier zip avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if module_name:
        # Backup d'un module spécifique
        backup_single_module(project_root, module_name, target_dir, timestamp, data_only, code_only)
    else:
        # Backup de tous les modules dans un seul zip
        backup_all_modules(project_root, modules, target_dir, timestamp, data_only, code_only)


def backup_single_module(project_root: Path, module_name: str, target_dir: Path, timestamp: str, data_only: bool, code_only: bool) -> None:
    """Backup a single module
    Args:
        project_root (Path): Root directory of the project
        module_name (str): Name of the module to backup
        target_dir (Path): Target directory for the backup
        timestamp (str): Timestamp for the backup file
        data_only (bool): Backup only data directories
        code_only (bool): Backup only code directories
    """
    
    # Déterminer le suffixe selon les options
    suffix = ""
    if data_only:
        suffix = "_data"
    elif code_only:
        suffix = "_code"
    
    zip_filename = f"{module_name}_backup{suffix}_{timestamp}.zip"
    zip_path = target_dir / zip_filename
    
    module_dir = project_root / "modules" / module_name
    data_dir = project_root / "data" / module_name
    
    # Vérifier qu'au moins un des dossiers existe
    if not module_dir.exists() and not data_dir.exists():
        print(f"❌ Neither code nor data found for module '{module_name}'")
        return
    
    files_added = 0
    total_size = 0
    
    try:
        with ZipFile(zip_path, 'w') as zipf:
            
            # Backup du code
            if not data_only and module_dir.exists():
                for file_path in module_dir.rglob("*"):
                    if file_path.is_file():
                        arc_name = f"modules/{module_name}/{file_path.relative_to(module_dir)}"
                        zipf.write(file_path, arc_name)
                        files_added += 1
                        total_size += file_path.stat().st_size
            
            # Backup des données
            if not code_only and data_dir.exists():
                for file_path in data_dir.rglob("*"):
                    if file_path.is_file():
                        arc_name = f"data/{module_name}/{file_path.relative_to(data_dir)}"
                        zipf.write(file_path, arc_name)
                        files_added += 1
                        total_size += file_path.stat().st_size
        
        if files_added == 0:
            print(f"⚠️  No files found to backup for module '{module_name}'")
            zip_path.unlink()  # Supprimer le zip vide
            return
        
        # Afficher le résultat
        zip_size = zip_path.stat().st_size
        print(f"✅ Module '{module_name}' backed up:")
        print(f"   📁 Files: {files_added}")
        print(f"   📊 Original size: {format_size(total_size)}")
        print(f"   🗜️  Compressed size: {format_size(zip_size)}")
        print(f"   📄 Saved as: {zip_filename}")
        
    except Exception as e:
        print(f"❌ Error creating backup for '{module_name}': {e}")
        if zip_path.exists():
            zip_path.unlink()


def backup_all_modules(project_root: Path, modules: list, target_dir: Path, timestamp: str, data_only: bool, code_only: bool) -> None:
    """Backup all modules in a single zip file
    Args:
        project_root (Path): Root directory of the project
        modules (list): List of module names to backup
        target_dir (Path): Target directory for the backup
        timestamp (str): Timestamp for the backup file
        data_only (bool): Backup only data directories
        code_only (bool): Backup only code directories"""
    
    # Déterminer le suffixe selon les options
    suffix = ""
    if data_only:
        suffix = "_data"
    elif code_only:
        suffix = "_code"
    
    zip_filename = f"all_modules_backup{suffix}_{timestamp}.zip"
    zip_path = target_dir / zip_filename
    
    files_added = 0
    total_size = 0
    modules_processed = 0
    
    try:
        with ZipFile(zip_path, 'w') as zipf:
            
            for module_name in modules:
                module_dir = project_root / "modules" / module_name
                data_dir = project_root / "data" / module_name
                module_files = 0
                
                # Backup du code
                if not data_only and module_dir.exists():
                    for file_path in module_dir.rglob("*"):
                        if file_path.is_file():
                            arc_name = f"modules/{module_name}/{file_path.relative_to(module_dir)}"
                            zipf.write(file_path, arc_name)
                            files_added += 1
                            module_files += 1
                            total_size += file_path.stat().st_size
                
                # Backup des données
                if not code_only and data_dir.exists():
                    for file_path in data_dir.rglob("*"):
                        if file_path.is_file():
                            arc_name = f"data/{module_name}/{file_path.relative_to(data_dir)}"
                            zipf.write(file_path, arc_name)
                            files_added += 1
                            module_files += 1
                            total_size += file_path.stat().st_size
                
                if module_files > 0:
                    modules_processed += 1
                    print(f"   📦 {module_name}: {module_files} files")
        
        if files_added == 0:
            print("⚠️  No files found to backup")
            zip_path.unlink()  # Supprimer le zip vide
            return
        
        # Afficher le résultat
        zip_size = zip_path.stat().st_size
        print("✅ Backup completed:")
        print(f"   📁 Modules: {modules_processed}/{len(modules)}")
        print(f"   📄 Total files: {files_added}")
        print(f"   📊 Original size: {format_size(total_size)}")
        print(f"   🗜️  Compressed size: {format_size(zip_size)}")
        print(f"   💾 Saved as: {zip_filename}")
        
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        if zip_path.exists():
            zip_path.unlink()


def format_size(size_bytes: int) -> str:
    """Format size in bytes to a human-readable string
    Args:
        size_bytes (int): Size in bytes
    Returns:
        str: Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"
