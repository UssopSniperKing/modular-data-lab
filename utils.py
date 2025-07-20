from pathlib import Path
import shutil
import importlib.util

def create_module(module_name: str) -> None:
    """Create a new module with its structure
    Args:
        module_name (str): Name of the module to create
    """

    module_dir = Path(f"modules/{module_name}")
    data_dir = Path(f"data/{module_name}")

    module_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # run.py file
    run_content = f'''"""Module {module_name}"""

from pathlib import Path
import sys

# Import other module functions
sys.path.append(str(Path(__file__).parent))
from load_data import load_data
from analyze import analyze

def run() -> None:
    """Main execution function"""

    print(f"=== Module {module_name} ===")
    
    data = load_data()
    results = analyze(data)
    
    print(f"=== Finished ===")


if __name__ == "__main__":
    run()
'''

    # load_data.py file
    load_data_content = f'''"""Load data for {module_name}"""
    from pathlib import Path

def load_data() -> None:
    """Load module data"""

    data_dir = Path(__file__).parent.parent.parent / "data" / "{module_name}"

    # TODO: Implement loading
    pass
'''
    
    # analyze.py file
    analyze_content = f'''"""Analyze data for {module_name}"""

def analyze(data) -> None:
    """Perform data analysis"""

    # TODO: Implement analysis
    pass
'''

    # Writing files
    files = {
        "run.py": run_content,
        "load_data.py": load_data_content,
        "analyze.py": analyze_content
    }
    
    for filename, content in files.items():
        with open(module_dir / filename, "w") as f:
            f.write(content)
    
    print(f"✅ Module '{module_name}' created:")
    print(f"   📁 modules/{module_name}/")
    print(f"   📁 data/{module_name}/")
    print(f"   📄 Files: {', '.join(files.keys())}")


def list_modules() -> None:
    """List all available modules"""

    modules_dir = Path("modules")
    
    if not modules_dir.exists():
        print("❌ Modules directory does not exist. Run 'python setup.py'")
        return
    
    # Get all directories in the modules directory
    modules = [d.name for d in modules_dir.iterdir() if d.is_dir()]
    
    if not modules:
        print("📋 No module found")
        print("💡 Use 'python run.py add <module_name>'")
        return
    
    def format_size(size_bytes:int) -> str:
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
    
    print(f"📋 Available Modules ({len(modules)}):")
    for module in sorted(modules):
        data_path = Path(f"data/{module}")
        
        if data_path.exists():
            # Get all files in the data directory
            data_files = [f for f in data_path.glob("*") if f.is_file()]
            
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

    module_path = Path(f"modules/{module_name}/run.py")
    
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
            result = module.run()
            print(f"✅ Module '{module_name}' finished")
            return True
        else:
            print(f"❌ Function 'run' not found in {module_name}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def remove_module(module_name: str) -> None:
    """Remove a module (modules and data directories)
    Args:
        module_name (str): Name of the module to remove
    """

    module_dir = Path(f"modules/{module_name}")
    data_dir = Path(f"data/{module_name}")
    
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
