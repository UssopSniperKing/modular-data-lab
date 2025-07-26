import sys
from modular_data_lab.utils import create_module, list_modules, run_module, remove_module

def show_help() -> None:
    """Show help information"""

    help_text = """
📋 Available Commands:
  
  lab-setup                   # Initialize the project structure
  lab list                    # List modules
  lab add <module_name>       # Create a new module
  lab run <module_name>       # Run a module
  lab remove <module_name>    # Remove a module
  lab help                    # Show this help

📁 Structure created for each module:
  modules/module_name/run.py           # Entry point
  modules/module_name/load_data.py     # Data loading
  modules/module_name/analyze.py       # Analysis
  data/module_name/                    # Folder for CSV files
"""
    print(help_text)


def main() -> None:
    """Main entry point for the script"""

    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "add" and len(sys.argv) == 3:
        create_module(sys.argv[2])
    elif command == "list":
        list_modules()
    elif command == "run" and len(sys.argv) == 3:
        run_module(sys.argv[2])
    elif command == "remove" and len(sys.argv) == 3:
        remove_module(sys.argv[2])
    elif command == "help":
        show_help()
    else:
        print("❌ Invalid command")
        show_help()

if __name__ == "__main__":
    main()
