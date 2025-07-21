import sys
from utils import create_module, list_modules, run_module, remove_module

def show_help() -> None:
    """Show help information"""

    help_text = """
📋 Available Commands:

  uv lab list                    # List modules
  uv lab add <module_name>       # Create a new module
  uv lab run <module_name>       # Run a module
  uv lab remove <module_name>    # Remove a module
  uv lab help                    # Show this help

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
