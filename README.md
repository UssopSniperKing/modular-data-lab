# Modular Data Lab (MDL)

A Python framework for organizing data analysis projects in modular, reusable components. Each module contains its own data loading, analysis functions, and dedicated data directory, making it easy to manage multiple analysis workflows in a single project.

## ✨ What does it do?

**Modular Data Lab** helps you:
- **Organize** your data analysis projects into clean, modular components
- **Standardize** your workflow with consistent data loading and analysis patterns  
- **Manage** datasets in dedicated directories per module
- **Reuse** analysis code across different projects
- **Backup** and share specific modules or entire projects

### Project Structure

After initialization, your project will look like:

```
your-project/
├── modules/           # Analysis modules
│   └── module_name/
│       ├── run.py     # Entry point
│       ├── load_data.py
│       └── analyze.py
└── data/              # Data storage
    └── module_name/
        └── *.csv      # Your datasets
```

Each module follows a simple, consistent structure that makes it easy to understand and maintain your analysis workflows.

## 🚀 Installation

### Option 1: With uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package manager that handles virtual environments automatically.

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install MDL from GitHub (latest release)
uv add git+https://github.com/ussopsniperking/modular-data-lab.git@v0.1.0

# OR install from the last commit on the master branch
# uv add git+https://github.com/ussopsniperking/modular-data-lab.git

# Initialize your project
uv run lab setup
```

### Option 2: With standard Python

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install MDL from GitHub
pip install git+https://github.com/ussopsniperking/modular-data-lab.git

# Initialize your project
python -m modular_data_lab.run setup
```

## 📋 Commands

```bash
# Initialize project structure
uv run lab setup

# Create a new analysis module
uv run lab add <module_name>

# List all modules
uv run lab list

# Run a specific module
uv run lab run <module_name>

# Remove a module
uv run lab remove <module_name>

# Backup modules
uv run lab backup <target_directory>                    # Backup all modules
uv run lab backup <module_name> <target_directory>      # Backup specific module

# Show help
uv run lab help
```

**Without uv:** Replace `uv run lab` with `python -m modular_data_lab.run` in all commands.

## 📖 Quick Example

Let's create a simple sales analysis module:

### 1. Setup and create module
```bash
uv run lab setup
uv run lab add sales_analysis
```

### 2. Add sample data
Create `data/sales_analysis/sales.csv`:
```csv
date,product,revenue,region
2024-01-15,Laptop,1200,North
2024-01-16,Phone,800,South
2024-01-17,Tablet,500,East
2024-01-18,Monitor,300,West
```

### 3. Implement data loading
Edit `modules/sales_analysis/load_data.py`:
```python
import pandas as pd
from pathlib import Path

def load_data():
    """Load sales data"""
    data_dir = Path(__file__).parent.parent.parent / "data" / "sales_analysis"
    
    # Load CSV
    sales_data = pd.read_csv(data_dir / "sales.csv")
    sales_data['date'] = pd.to_datetime(sales_data['date'])
    
    print(f"✅ Loaded {len(sales_data)} sales records")
    return sales_data
```

### 4. Implement analysis
Edit `modules/sales_analysis/analyze.py`:
```python
def analyze(data):
    """Analyze sales data"""
    if data is None or data.empty:
        print("❌ No data to analyze")
        return
    
    print("\n📊 Sales Analysis:")
    print(f"💰 Total Revenue: ${data['revenue'].sum():,.2f}")
    print(f"📈 Average Sale: ${data['revenue'].mean():.2f}")
    
    # Revenue by region
    print("\n🌍 Revenue by Region:")
    region_revenue = data.groupby('region')['revenue'].sum()
    for region, revenue in region_revenue.items():
        print(f"   {region}: ${revenue:,.2f}")
```

### 5. Run the analysis
```bash
uv run lab run sales_analysis
```

**Output:**
```
▶️  Running: sales_analysis
=== Module sales_analysis ===
✅ Loaded 4 sales records

📊 Sales Analysis:
💰 Total Revenue: $2,800.00
📈 Average Sale: $700.00

🌍 Revenue by Region:
   East: $500.00
   North: $1,200.00
   South: $800.00
   West: $300.00
=== Finished ===
✅ Module 'sales_analysis' finished
```



## 🔧 Adding Dependencies

### With uv:
```bash
uv add pandas matplotlib seaborn scikit-learn
```

### With pip:
```bash
pip install pandas matplotlib seaborn scikit-learn
```

## 💾 Backup Features

The framework includes built-in backup functionality with optional flags:

```bash
# Backup all modules to a directory
uv run lab backup /path/to/backup/

# Backup specific module
uv run lab backup sales_analysis /path/to/backup/

# Backup only data files (using --data or -d flag)
uv run lab backup --data /path/to/backup/
uv run lab backup -d /path/to/backup/

# Backup only code files (using --code or -c flag)
uv run lab backup --code /path/to/backup/
uv run lab backup -c /path/to/backup/
```

**Backup flags:**
- `--data` or `-d`: Backup only data directories
- `--code` or `-c`: Backup only code directories  
- No flag: Backup everything (default)

Backups are created as timestamped ZIP files with compression.

## 💡 Best Practices

- **Keep modules focused**: One analysis goal per module
- **Use descriptive names**: `customer_segmentation` vs `analysis1`
- **Document your data**: Add comments about data sources and formats
- **Reuse code**: Create utility functions in separate files within modules

## 🔧 Advanced Usage

### Custom Module Structure
You can add additional Python files to any module:
```
modules/advanced_analysis/
├── run.py
├── load_data.py
├── analyze.py
├── utils.py          # Custom utilities
└── visualizations.py # Custom plots
```

### Data Organization
Organize complex datasets in subdirectories:
```
data/market_research/
├── raw/
│   ├── survey_2024.csv
│   └── demographics.csv
├── processed/
│   └── cleaned_data.csv
└── external/
    └── market_data.json
```

## 📄 License

MIT License - Feel free to use, modify, and distribute.# Modular Data Lab

---

**Happy analyzing! 📊✨**

*Need help? Check the command reference with `uv run lab help` or create an issue on GitHub.*