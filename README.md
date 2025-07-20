# Modular Data Lab

A Python framework for organizing and managing data analysis projects in a modular structure. Each module contains its own data loading, analysis functions, and dedicated data directory.

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. **Install uv** (if not already installed):
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows (PowerShell)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Clone the project from GitHub**:
   ```bash
   # Clone the repository
   git clone https://github.com/ussopsniperking/modular-data-lab.git
   cd modular-data-lab
   
   # Or fork it first, then clone your fork
   
   # Install dependencies (virtual environment is automatically created)
   uv sync
   
   # Set up project structure
   uv run setup
   ```

### First Run

After initialization, you should see:
```
🚀 Project Initialization
Created Folder: modules/
Created Folder: data/
✅ Base Structure Created!
💡 Use 'uv run lab add <module_name>' to add a module
```

## 📋 Usage

### Basic Commands

All commands use `uv run` with the script directly:

```bash
# Show help
uv run lab help
# or
uv run help

# Create a new analysis module
uv run lab add my_analysis

# List all available modules
uv run lab list

# Run a specific module
uv run lab run my_analysis

# Remove a module (with confirmation)
uv run lab remove my_analysis
```

### 📦 Adding Dependencies

Use uv to add Python packages:

```bash
# Add data science packages
uv add pandas numpy matplotlib seaborn scikit-learn

# Add specific versions
uv add "pandas>=2.0.0"

# Sync all dependencies (after cloning)
uv sync
```

### 🏗️ Project Structure

```
modular-data-lab/
├── README.md              # This file
├── pyproject.toml         # uv project configuration
├── setup.py               # Project initialization
├── run.py                 # Main CLI interface
├── utils.py               # Utility functions
├── modules/               # Analysis modules
│   └── module_name/
│       ├── run.py         # Module entry point
│       ├── load_data.py   # Data loading logic
│       ├── analyze.py     # Analysis functions
|       └── # any python files
└── data/                  # Data storage
    └── module_name/       # Module-specific data (which can contain subfolders)
        └── *.csv          # Your data files (.csv for example)
```

## 🚀 Example

### Complete Example: Sales Analysis

Let's walk through a complete example analyzing sales data:

**1. Create the module:**
```bash
uv run lab add sales_analysis
```

**2. Create sample data file `data/sales_analysis/sales.csv`:**
```csv
date,product,category,revenue,quantity,region
2024-01-15,Laptop,Electronics,1200,2,North
2024-01-16,Coffee Maker,Appliances,89,1,South
2024-01-17,Smartphone,Electronics,799,3,East
2024-01-18,Desk Chair,Furniture,299,1,West
2024-01-19,Tablet,Electronics,499,2,North
2024-01-20,Microwave,Appliances,159,1,South
2024-01-21,Monitor,Electronics,349,2,East
2024-01-22,Sofa,Furniture,899,1,West
2024-01-23,Headphones,Electronics,199,4,North
2024-01-24,Blender,Appliances,79,2,South
2024-02-01,Laptop,Electronics,1200,1,East
2024-02-02,Coffee Maker,Appliances,89,3,West
2024-02-03,Smartphone,Electronics,799,2,North
2024-02-04,Desk Chair,Furniture,299,2,South
2024-02-05,Gaming Console,Electronics,499,1,East
```

**3. Implement data loading (`modules/sales_analysis/load_data.py`):**
```python
"""Load data for sales_analysis"""

import pandas as pd
from pathlib import Path

def load_data():
    """Load module data"""
    
    data_dir = Path(__file__).parent.parent.parent / "data" / "sales_analysis"
    
    # Load CSV file
    sales_data = pd.read_csv(data_dir / "sales.csv")
    
    # Convert date column
    sales_data['date'] = pd.to_datetime(sales_data['date'])
    sales_data['month'] = sales_data['date'].dt.strftime('%Y-%m')
    
    print(f"✅ Loaded {len(sales_data)} sales records")
    print(f"📅 Date range: {sales_data['date'].min()} to {sales_data['date'].max()}")
    
    return sales_data
```

**4. Implement analysis (`modules/sales_analysis/analyze.py`):**
```python
"""Analyze data for sales_analysis"""

import pandas as pd
import matplotlib.pyplot as plt

def analyze(data):
    """Perform data analysis"""
    
    if data is None or data.empty:
        print("❌ No data to analyze")
        return None
    
    print("\n📊 Sales Analysis Results:")
    
    # Basic statistics
    total_revenue = data['revenue'].sum()
    total_quantity = data['quantity'].sum()
    avg_order_value = data['revenue'].mean()
    
    print(f"💰 Total Revenue: ${total_revenue:,.2f}")
    print(f"📦 Total Quantity: {total_quantity}")
    print(f"📈 Average Order Value: ${avg_order_value:.2f}")
    
    # Create visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # Revenue by category (pie chart)
    ax1.pie(category_revenue.values, labels=category_revenue.index, autopct='%1.1f%%')
    ax1.set_title('Revenue Distribution by Category')
    
    # Monthly revenue (bar chart)
    monthly_revenue.plot(kind='bar', ax=ax2, color='steelblue')
    ax2.set_title('Monthly Revenue')
    ax2.set_ylabel('Revenue ($)')
    ax2.tick_params(axis='x', rotation=45)
    
    # Revenue by region
    region_revenue = data.groupby('region')['revenue'].sum()
    region_revenue.plot(kind='bar', ax=ax3, color='lightcoral')
    ax3.set_title('Revenue by Region')
    ax3.set_ylabel('Revenue ($)')
    ax3.tick_params(axis='x', rotation=0)
    
    # Top products
    top_products.plot(kind='barh', ax=ax4, color='gold')
    ax4.set_title('Top 5 Products by Revenue')
    ax4.set_xlabel('Revenue ($)')
    
    plt.tight_layout()
    plt.show()
    
    print("\n✅ Analysis completed with visualizations!")
```

**5. Run the complete analysis:**
```bash
uv run lab run sales_analysis
```

**Expected output:**
```
▶️  Running: sales_analysis
=== Module sales_analysis ===
✅ Loaded 15 sales records
📅 Date range: 2024-01-15 00:00:00 to 2024-02-05 00:00:00

📊 Sales Analysis Results:
💰 Total Revenue: $7,458.00
📦 Total Quantity: 27
📈 Average Order Value: $497.20

✅ Analysis completed with visualizations!
=== Finished ===
✅ Module 'sales_analysis' finished
```

This example demonstrates the complete workflow from data creation to analysis with meaningful insights and visualizations.

## 🔧 Configuration

The framework uses a simple file-based structure. You can customize:

1. **Module Templates**: Edit the content templates in `utils.py` `create_module()` function
2. **Project Structure**: Modify `setup.py` to create additional directories
3. **CLI Commands**: Extend `run.py` with additional commands
4. **Commands Aliases**: Create aliases by modifying the `pyproject.toml` file

## 💡 Tips

- **Data Organization**: Keep related datasets in the same module's data directory
- **Code Reusability**: Create utility functions in separate files within each module
- **Version Control**: Add `data/` to `.gitignore` if your datasets are large (this is done by default)
- **Virtual Environment**: uv automatically manages your virtual environment via `pyproject.toml`
- **Dependencies**: Dependencies are managed in `pyproject.toml` and installed with `uv sync`

## 🐛 Troubleshooting

**Module not found errors:**
```bash
# Ensure you're in the project directory
pwd

# Recreate project structure if needed
uv run setup
```

**Import errors in modules:**
```bash
# Check if dependencies are installed
uv list

# Add missing packages
uv add package_name

# Sync dependencies if pyproject.toml was updated
uv sync
```

**Permission errors:**
```bash
# Ensure uv is properly installed and in PATH
uv --version

# Reinstall uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 📄 License

This project is open source. Feel free to modify and distribute according to your needs.

---

**Happy analyzing! 📊✨**