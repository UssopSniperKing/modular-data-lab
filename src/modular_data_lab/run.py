import sys
from pathlib import Path
from modular_data_lab.utils import create_module, list_modules, run_module, remove_module, backup_modules

def show_help() -> None:
    """Show help information"""

    help_text = """
📋 Available Commands:
  
  lab setup                           # Initialize the project structure
  lab list                            # List modules
  lab add <module_name>               # Create a new module
  lab run <module_name>               # Run a module
  lab remove <module_name>            # Remove a module
  lab backup <module_name> <dir>      # Backup specific module
  lab backup <dir>                    # Backup all modules
  lab help                            # Show this help

  🔧 Backup Options:
  -d, --data    Backup only data directories
  -c, --code    Backup only code directories

📁 Structure created for each module:
  modules/module_name/run.py           # Entry point
  modules/module_name/load_data.py     # Data loading
  modules/module_name/analyze.py       # Analysis
  data/module_name/                    # Folder for CSV files
"""
    print(help_text)


def setup() -> None:
    """Initialize the project structure"""

    print("🚀 Project Initialization")

    directories = ["modules", "data"] # Base directories
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created Folder: {directory}/")
    
    print("✅ Base Structure Created!")
    print("💡 Use 'lab add <module_name>' to add a module")


def main() -> None:
    """Main entry point for the script"""

    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()

    # Parse flags
    data_only = "-d" in sys.argv or "--data" in sys.argv
    code_only = "-c" in sys.argv or "--code" in sys.argv
    
    # Remove flags from argv for cleaner parsing
    clean_argv = [arg for arg in sys.argv if arg not in ["-d", "--data", "-c", "--code"]]
    
    if command == "add" and len(clean_argv) == 3:  # Changed from sys.argv to clean_argv
        create_module(clean_argv[2])
    elif command == "list":
        list_modules()
    elif command == "run" and len(clean_argv) == 3:  # Changed from sys.argv to clean_argv
        run_module(clean_argv[2])
    elif command == "remove" and len(clean_argv) == 3:  # Changed from sys.argv to clean_argv
        remove_module(clean_argv[2])
    elif command == "backup" and len(clean_argv) == 4:  # 4 args: ['lab', 'backup', 'module', 'dir']
        backup_modules(clean_argv[3], clean_argv[2], data_only, code_only)
    elif command == "backup" and len(clean_argv) == 3:  # 3 args: ['lab', 'backup', 'dir']
        backup_modules(clean_argv[2], None, data_only, code_only)
    elif command == "setup":
        setup()
    elif command == "help":
        show_help()
    else:
        print("❌ Invalid command")
        show_help()

if __name__ == "__main__":
    main()
