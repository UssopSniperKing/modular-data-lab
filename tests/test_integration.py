from pathlib import Path
import sys
import zipfile
from unittest.mock import patch

# Import the modules under test
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from modular_data_lab.run import setup
from modular_data_lab.utils import create_module, run_module, backup_modules, list_modules, remove_module


class TestFullWorkflow:
    """Tests d'intégration pour le workflow complet"""
    
    def test_complete_project_workflow(self, tmp_path, monkeypatch, backup_target, capsys):
        """Test du workflow complet : setup -> add -> run -> backup -> remove"""
        # Se placer dans le répertoire temporaire
        monkeypatch.chdir(tmp_path)
        
        # 1. Setup du projet
        setup()
        assert (tmp_path / "modules").exists()
        assert (tmp_path / "data").exists()
        
        # 2. Créer un module
        create_module("integration_test")
        assert (tmp_path / "modules" / "integration_test").exists()
        assert (tmp_path / "data" / "integration_test").exists()
        
        # Vérifier les fichiers créés
        module_dir = tmp_path / "modules" / "integration_test"
        assert (module_dir / "run.py").exists()
        assert (module_dir / "load_data.py").exists()
        assert (module_dir / "analyze.py").exists()
        
        # 3. Ajouter des données de test
        data_dir = tmp_path / "data" / "integration_test"
        (data_dir / "test_data.csv").write_text("col1,col2\nval1,val2\n")
        
        # 4. Lister les modules
        list_modules()
        captured = capsys.readouterr()
        assert "integration_test" in captured.out
        
        # 5. Exécuter le module
        result = run_module("integration_test")
        assert result is True
        
        # 6. Backup du module
        backup_modules(str(backup_target), "integration_test")
        zip_files = list(backup_target.glob("integration_test_backup_*.zip"))
        assert len(zip_files) == 1
        
        # Vérifier le contenu du backup
        with zipfile.ZipFile(zip_files[0], 'r') as zf:
            files = zf.namelist()
            assert "modules/integration_test/run.py" in files
            assert "data/integration_test/test_data.csv" in files
        
        # 7. Backup de tous les modules
        backup_modules(str(backup_target))
        all_zip_files = list(backup_target.glob("all_modules_backup_*.zip"))
        assert len(all_zip_files) == 1
        
        # 8. Supprimer le module (avec confirmation automatique)
        with patch('builtins.input', return_value='y'):
            remove_module("integration_test")
        
        assert not (tmp_path / "modules" / "integration_test").exists()
        assert not (tmp_path / "data" / "integration_test").exists()
    
    def test_multiple_modules_workflow(self, tmp_path, monkeypatch, backup_target, capsys):
        """Test workflow avec plusieurs modules"""
        monkeypatch.chdir(tmp_path)
        
        # Setup
        setup()
        
        # Créer plusieurs modules
        modules = ["module_a", "module_b", "module_c"]
        for module_name in modules:
            create_module(module_name)
            
            # Ajouter des données différentes à chaque module
            data_dir = tmp_path / "data" / module_name
            (data_dir / f"{module_name}_data.csv").write_text(f"data for {module_name}\n")
        
        # Lister tous les modules
        list_modules()
        captured = capsys.readouterr()
        for module_name in modules:
            assert module_name in captured.out
        
        # Backup de tous les modules
        backup_modules(str(backup_target))
        
        # Vérifier le backup
        zip_files = list(backup_target.glob("all_modules_backup_*.zip"))
        assert len(zip_files) == 1
        
        with zipfile.ZipFile(zip_files[0], 'r') as zf:
            files = zf.namelist()
            for module_name in modules:
                assert f"modules/{module_name}/run.py" in files
                assert f"data/{module_name}/{module_name}_data.csv" in files
        
        # Backup sélectif de modules individuels
        for module_name in modules:
            backup_modules(str(backup_target), module_name, data_only=True)
        
        # Vérifier qu'on a maintenant 4 zips (1 all + 3 individuels)
        all_zips = list(backup_target.glob("*.zip"))
        assert len(all_zips) == 4  # 1 all_modules + 3 individuels
    
    def test_workflow_with_different_backup_options(self, tmp_path, monkeypatch, backup_target):
        """Test workflow avec différentes options de backup"""
        monkeypatch.chdir(tmp_path)
        
        # Setup et création d'un module
        setup()
        create_module("test_options")
        
        # Ajouter plusieurs fichiers
        module_dir = tmp_path / "modules" / "test_options"
        (module_dir / "extra_code.py").write_text("# Extra code file")
        
        data_dir = tmp_path / "data" / "test_options"
        (data_dir / "dataset1.csv").write_text("data1\n")
        (data_dir / "dataset2.csv").write_text("data2\n")
        
        # Test backup complet
        backup_modules(str(backup_target), "test_options")
        
        # Test backup data seulement
        backup_modules(str(backup_target), "test_options", data_only=True)
        
        # Test backup code seulement
        backup_modules(str(backup_target), "test_options", code_only=True)
        
        # Vérifier qu'on a 3 zips différents
        zip_files = list(backup_target.glob("*.zip"))
        assert len(zip_files) == 3
        
        # Vérifier les noms des fichiers
        filenames = [f.name for f in zip_files]
        assert any("test_options_backup_" in name and "_data_" in name for name in filenames)
        assert any("test_options_backup_" in name and "_code_" in name for name in filenames)
        assert any("test_options_backup_" in name and "_data_" not in name and "_code_" not in name for name in filenames)


class TestErrorRecovery:
    """Tests de récupération d'erreurs et cas limites"""
    
    def test_workflow_with_corrupted_module(self, tmp_path, monkeypatch, capsys):
        """Test workflow avec un module corrompu"""
        monkeypatch.chdir(tmp_path)
        
        setup()
        create_module("corrupted_module")
        
        # Corrompre le fichier run.py
        module_dir = tmp_path / "modules" / "corrupted_module"
        (module_dir / "run.py").write_text("invalid python syntax !!!!")
        
        # Essayer d'exécuter le module corrompu
        result = run_module("corrupted_module")
        assert result is False
        
        captured = capsys.readouterr()
        assert "❌ An error occurred:" in captured.out
    
    def test_workflow_in_subdirectory(self, tmp_path, monkeypatch, backup_target):
        """Test workflow depuis un sous-répertoire"""
        monkeypatch.chdir(tmp_path)
        
        # Setup du projet
        setup()
        create_module("subdir_test")
        
        # Se déplacer dans le dossier modules
        modules_dir = tmp_path / "modules"
        monkeypatch.chdir(modules_dir)
        
        # Les opérations devraient toujours fonctionner
        backup_modules(str(backup_target), "subdir_test")
        
        zip_files = list(backup_target.glob("*.zip"))
        assert len(zip_files) == 1
    
    def test_partial_project_structure(self, tmp_path, monkeypatch, capsys):
        """Test avec structure de projet incomplète"""
        monkeypatch.chdir(tmp_path)
        
        # Créer seulement le dossier modules (pas data)
        (tmp_path / "modules").mkdir()
        
        # Essayer de créer un module
        create_module("partial_test")
        
        # Devrait fonctionner même sans dossier data initial
        assert (tmp_path / "modules" / "partial_test").exists()
        assert (tmp_path / "data" / "partial_test").exists()  # Devrait être créé


class TestConcurrentOperations:
    """Tests de gestion des opérations concurrentes"""
    
    def test_multiple_backups_same_module(self, tmp_path, monkeypatch, backup_target):
        """Test backups multiples du même module"""
        monkeypatch.chdir(tmp_path)
        
        setup()
        create_module("concurrent_test")
        
        # Faire plusieurs backups rapidement
        for i in range(3):
            backup_modules(str(backup_target), "concurrent_test")
        
        # Tous les backups devraient exister avec des noms différents
        zip_files = list(backup_target.glob("concurrent_test_backup_*.zip"))
        assert len(zip_files) == 3
        
        # Vérifier que tous les noms sont différents
        names = [f.name for f in zip_files]
        assert len(set(names)) == 3  # Tous uniques
