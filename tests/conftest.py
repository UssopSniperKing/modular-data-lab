import pytest
import tempfile
from pathlib import Path
import os


@pytest.fixture
def temp_project():
    """Crée un projet temporaire pour les tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "test_project"
        project_dir.mkdir()
        
        # Créer la structure de base
        (project_dir / "modules").mkdir()
        (project_dir / "data").mkdir()
        
        # Créer un module de test avec des fichiers
        test_module = project_dir / "modules" / "test_module"
        test_module.mkdir()
        
        # Fichiers du module
        (test_module / "run.py").write_text('''"""Module test_module"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))
from load_data import load_data
from analyze import analyze

def run() -> None:
    """Main execution function"""
    print("=== Module test_module ===")
    data = load_data()
    results = analyze(data)
    print("=== Finished ===")

if __name__ == "__main__":
    run()
''')
        
        (test_module / "load_data.py").write_text('''"""Load data for test_module"""
from pathlib import Path

def load_data() -> str:
    """Load module data"""
    data_dir = Path(__file__).parent.parent.parent / "data" / "test_module"
    return "test_data"
''')
        
        (test_module / "analyze.py").write_text('''"""Analyze data for test_module"""

def analyze(data) -> str:
    """Perform data analysis"""
    return f"analyzed_{data}"
''')
        
        # Créer des données de test
        test_data_dir = project_dir / "data" / "test_module"
        test_data_dir.mkdir()
        (test_data_dir / "data.csv").write_text("col1,col2\n1,2\n3,4\n")
        (test_data_dir / "extra.txt").write_text("Extra test file")
        
        # Créer un deuxième module pour les tests "all modules"
        second_module = project_dir / "modules" / "second_module"
        second_module.mkdir()
        (second_module / "run.py").write_text("# Second module")
        
        second_data = project_dir / "data" / "second_module"
        second_data.mkdir()
        (second_data / "data2.csv").write_text("a,b\n5,6\n")
        
        yield project_dir


@pytest.fixture
def mock_cwd(monkeypatch, temp_project):
    """Mock du répertoire courant - positionne dans la racine du projet"""
    original_cwd = os.getcwd()
    monkeypatch.chdir(temp_project)
    yield temp_project
    monkeypatch.chdir(original_cwd)


@pytest.fixture
def mock_cwd_in_modules(monkeypatch, temp_project):
    """Mock du répertoire courant - positionne dans le dossier modules/"""
    original_cwd = os.getcwd()
    modules_dir = temp_project / "modules"
    monkeypatch.chdir(modules_dir)
    yield modules_dir
    monkeypatch.chdir(original_cwd)


@pytest.fixture
def mock_cwd_outside_project(monkeypatch):
    """Mock du répertoire courant - positionne en dehors du projet"""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        monkeypatch.chdir(tmpdir)
        yield Path(tmpdir)
        monkeypatch.chdir(original_cwd)


@pytest.fixture
def backup_target(tmp_path):
    """Répertoire temporaire pour les backups"""
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()
    return backup_dir