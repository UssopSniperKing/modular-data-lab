from pathlib import Path

def main() -> None:
    """Initialize the project structure"""

    print("🚀 Project Initialization")

    directories = ["modules", "data"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created Folder: {directory}/")
    
    print("✅ Base Structure Created!")
    print("💡 Use 'uv run lab add <module_name>' to add a module")

if __name__ == "__main__":
    main()
