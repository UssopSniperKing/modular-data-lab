
def get_templates() -> dict[str, str]:
    """Hold templates for module files"""

    # run.py content
    run_content = '''"""Module {module_name}"""

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

    # load_data.py content
    load_data_content = '''"""Load data for {module_name}"""
from pathlib import Path

def load_data() -> None:
    """Load module data"""

    data_dir = Path(__file__).parent.parent.parent / "data" / "{module_name}"

    # TODO: Implement loading
    pass
'''

    # analyze.py content
    analyze_content = '''"""Analyze data for {module_name}"""

def analyze(data) -> None:
    """Perform data analysis"""

    # TODO: Implement analysis
    pass
'''

    return {
        "run.py": run_content,
        "load_data.py": load_data_content,
        "analyze.py": analyze_content
    }