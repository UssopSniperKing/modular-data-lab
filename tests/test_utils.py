from pathlib import Path
import sys

# Import the module under test
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from modular_data_lab.utils import (
    get_project_root, create_module, list_modules, 
    run_module, remove_module, format_size
)


class TestGetProjectRoot:
    
    def test_get_project_root_in_root(self, mock_cwd):
        """Test quand on est dans la racine du projet"""
        result = get_project_root()
        assert result == mock_cwd
        assert result.name == "test_project"
    
    def test_get_project_root_in_modules(self, mock_cwd_in_modules):
        """Test quand on est dans le dossier modules/"""
        result = get_project_root()
        assert result == mock_cwd_in_modules.parent
        assert result.name == "test_project"
    
    def test_get_project_root_not_found(self, mock_cwd_outside_project):
        """Test quand on n'est pas dans un projet"""
        result = get_project_root()
        assert result is None


class TestCreateModule:
    
    def test_create_module_success(self, mock_cwd, capsys):
        """Test création réussie d'un module"""
        create_module("new_module")
        
        # Vérifier que les dossiers ont été créés
        assert (mock_cwd / "modules" / "new_module").exists()
        assert (mock_cwd / "data" / "new_module").exists()
        
        # Vérifier que les fichiers ont été créés
        module_dir = mock_cwd / "modules" / "new_module"
        assert (module_dir / "run.py").exists()
        assert (module_dir / "load_data.py").exists()
        assert (module_dir / "analyze.py").exists()
        
        # Vérifier le contenu des fichiers
        run_content = (module_dir / "run.py").read_text()
        assert "new_module" in run_content
        assert "def run() -> None:" in run_content
        
        # Vérifier la sortie
        captured = capsys.readouterr()
        assert "✅ Module 'new_module' created:" in captured.out
        assert "modules/new_module/" in captured.out
    
    def test_create_module_outside_project(self, mock_cwd_outside_project, capsys):
        """Test création d'un module en dehors du projet"""
        create_module("test_module")
        
        captured = capsys.readouterr()
        assert "❌ Project root not found" in captured.out
        assert "💡 Run 'lab setup'" in captured.out
    
    def test_create_module_already_exists(self, mock_cwd, capsys):
        """Test création d'un module qui existe déjà"""
        # Le module test_module existe déjà dans le fixture
        create_module("test_module")
        
        # Le module devrait être recréé/écrasé
        captured = capsys.readouterr()
        assert "✅ Module 'test_module' created:" in captured.out


class TestListModules:
    
    def test_list_modules_success(self, mock_cwd, capsys):
        """Test listage des modules"""
        list_modules()
        
        captured = capsys.readouterr()
        assert "📋 Available Modules (2):" in captured.out
        assert "📦 second_module" in captured.out
        assert "📦 test_module" in captured.out
        assert "fichiers" in captured.out  # Info sur les données
    
    def test_list_modules_empty(self, mock_cwd, capsys):
        """Test listage sans modules"""
        # Supprimer tous les modules
        import shutil
        shutil.rmtree(mock_cwd / "modules")
        (mock_cwd / "modules").mkdir()
        
        list_modules()
        
        captured = capsys.readouterr()
        assert "📋 No module found" in captured.out
        assert "💡 Use 'lab add <module_name>'" in captured.out
    
    def test_list_modules_outside_project(self, mock_cwd_outside_project, capsys):
        """Test listage en dehors du projet"""
        list_modules()
        
        captured = capsys.readouterr()
        assert "❌ Project root not found" in captured.out


class TestRunModule:
    
    def test_run_module_success(self, mock_cwd, capsys):
        """Test exécution réussie d'un module"""
        result = run_module("test_module")
        
        assert result is True
        captured = capsys.readouterr()
        assert "▶️  Running: test_module" in captured.out
        assert "=== Module test_module ===" in captured.out
        assert "✅ Module 'test_module' finished" in captured.out
    
    def test_run_module_not_found(self, mock_cwd, capsys):
        """Test exécution d'un module inexistant"""
        result = run_module("nonexistent_module")
        
        assert result is False
        captured = capsys.readouterr()
        assert "❌ Module 'nonexistent_module' not found" in captured.out
    
    def test_run_module_outside_project(self, mock_cwd_outside_project, capsys):
        """Test exécution en dehors du projet"""
        result = run_module("test_module")
        
        assert result is None  # La fonction retourne None quand pas de projet
        captured = capsys.readouterr()
        assert "❌ Project root not found" in captured.out
    
    def test_run_module_no_run_function(self, mock_cwd, capsys):
        """Test module sans fonction run()"""
        # Créer un module sans fonction run
        bad_module = mock_cwd / "modules" / "bad_module"
        bad_module.mkdir()
        (bad_module / "run.py").write_text("# No run function here")
        
        result = run_module("bad_module")
        
        assert result is False
        captured = capsys.readouterr()
        assert "❌ Function 'run' not found in bad_module" in captured.out


class TestRemoveModule:
    
    def test_remove_module_success(self, mock_cwd, capsys, monkeypatch):
        """Test suppression réussie d'un module"""
        # Mock input pour confirmer
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        
        remove_module("test_module")
        
        # Vérifier que les dossiers ont été supprimés
        assert not (mock_cwd / "modules" / "test_module").exists()
        assert not (mock_cwd / "data" / "test_module").exists()
        
        captured = capsys.readouterr()
        assert "✅ Folder modules/test_module/ removed" in captured.out
        assert "✅ Folder data/test_module/ removed" in captured.out
    
    def test_remove_module_cancelled(self, mock_cwd, capsys, monkeypatch):
        """Test suppression annulée"""
        # Mock input pour annuler
        monkeypatch.setattr('builtins.input', lambda _: 'n')
        
        remove_module("test_module")
        
        # Vérifier que les dossiers existent toujours
        assert (mock_cwd / "modules" / "test_module").exists()
        assert (mock_cwd / "data" / "test_module").exists()
        
        captured = capsys.readouterr()
        assert "❌ Deletion canceled" in captured.out
    
    def test_remove_module_not_found(self, mock_cwd, capsys):
        """Test suppression d'un module inexistant"""
        remove_module("nonexistent_module")
        
        captured = capsys.readouterr()
        assert "❌ Module 'nonexistent_module' not found" in captured.out
    
    def test_remove_module_outside_project(self, mock_cwd_outside_project, capsys):
        """Test suppression en dehors du projet"""
        remove_module("test_module")
        
        captured = capsys.readouterr()
        assert "❌ Project root not found" in captured.out


class TestFormatSize:
    
    def test_format_size_bytes(self):
        """Test formatage en bytes"""
        assert format_size(0) == "0 B"
        assert format_size(512) == "512.0 B"
    
    def test_format_size_kb(self):
        """Test formatage en KB"""
        assert format_size(1024) == "1.0 KB"
        assert format_size(1536) == "1.5 KB"
    
    def test_format_size_mb(self):
        """Test formatage en MB"""
        assert format_size(1024 * 1024) == "1.0 MB"
        assert format_size(1024 * 1024 * 2.5) == "2.5 MB"
    
    def test_format_size_gb(self):
        """Test formatage en GB"""
        assert format_size(1024 * 1024 * 1024) == "1.0 GB"
