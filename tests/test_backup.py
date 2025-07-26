from pathlib import Path
import sys
import zipfile

# Import the module under test
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from modular_data_lab.utils import backup_modules


class TestBackupModules:
    
    def test_backup_single_module_success(self, mock_cwd, backup_target, capsys):
        """Test backup d'un module spécifique"""
        backup_modules(str(backup_target), "test_module")
        
        # Vérifier qu'un fichier zip a été créé
        zip_files = list(backup_target.glob("test_module_backup_*.zip"))
        assert len(zip_files) == 1
        
        zip_file = zip_files[0]
        
        # Vérifier le contenu du zip
        with zipfile.ZipFile(zip_file, 'r') as zf:
            files = zf.namelist()
            
            # Vérifier la structure
            assert "modules/test_module/run.py" in files
            assert "modules/test_module/load_data.py" in files
            assert "modules/test_module/analyze.py" in files
            assert "data/test_module/data.csv" in files
            assert "data/test_module/extra.txt" in files
        
        # Vérifier la sortie
        captured = capsys.readouterr()
        assert "✅ Module 'test_module' backed up:" in captured.out
        assert "📁 Files: 5" in captured.out
        assert "📊 Original size:" in captured.out
        assert "🗜️  Compressed size:" in captured.out
    
    def test_backup_all_modules_success(self, mock_cwd, backup_target, capsys):
        """Test backup de tous les modules"""
        backup_modules(str(backup_target))
        
        # Vérifier qu'un fichier zip a été créé
        zip_files = list(backup_target.glob("all_modules_backup_*.zip"))
        assert len(zip_files) == 1
        
        zip_file = zip_files[0]
        
        # Vérifier le contenu du zip
        with zipfile.ZipFile(zip_file, 'r') as zf:
            files = zf.namelist()
            
            # Vérifier que les deux modules sont présents
            assert "modules/test_module/run.py" in files
            assert "modules/second_module/run.py" in files
            assert "data/test_module/data.csv" in files
            assert "data/second_module/data2.csv" in files
        
        # Vérifier la sortie
        captured = capsys.readouterr()
        assert "✅ Backup completed:" in captured.out
        assert "📁 Modules: 2/2" in captured.out
        assert "📦 second_module: 2 files" in captured.out
        assert "📦 test_module: 5 files" in captured.out
    
    def test_backup_data_only(self, mock_cwd, backup_target, capsys):
        """Test backup data seulement"""
        backup_modules(str(backup_target), "test_module", data_only=True)
        
        zip_files = list(backup_target.glob("test_module_backup_data_*.zip"))
        assert len(zip_files) == 1
        
        # Vérifier le contenu du zip
        with zipfile.ZipFile(zip_files[0], 'r') as zf:
            files = zf.namelist()
            
            # Seulement les fichiers data/
            assert "data/test_module/data.csv" in files
            assert "data/test_module/extra.txt" in files
            
            # Pas de fichiers modules/
            assert not any("modules/" in f for f in files)
        
        captured = capsys.readouterr()
        assert "📁 Files: 2" in captured.out
    
    def test_backup_code_only(self, mock_cwd, backup_target, capsys):
        """Test backup code seulement"""
        backup_modules(str(backup_target), "test_module", code_only=True)
        
        zip_files = list(backup_target.glob("test_module_backup_code_*.zip"))
        assert len(zip_files) == 1
        
        # Vérifier le contenu du zip
        with zipfile.ZipFile(zip_files[0], 'r') as zf:
            files = zf.namelist()
            
            # Seulement les fichiers modules/
            assert "modules/test_module/run.py" in files
            assert "modules/test_module/load_data.py" in files
            assert "modules/test_module/analyze.py" in files
            
            # Pas de fichiers data/
            assert not any("data/" in f for f in files)
        
        captured = capsys.readouterr()
        assert "📁 Files: 3" in captured.out
    
    def test_backup_invalid_flags(self, mock_cwd, backup_target, capsys):
        """Test flags data et code ensemble (invalide)"""
        backup_modules(str(backup_target), "test_module", data_only=True, code_only=True)
        
        # Aucun zip ne devrait être créé
        zip_files = list(backup_target.glob("*.zip"))
        assert len(zip_files) == 0
        
        captured = capsys.readouterr()
        assert "❌ Cannot use both --data and --code flags together" in captured.out
    
    def test_backup_nonexistent_module(self, mock_cwd, backup_target, capsys):
        """Test backup d'un module inexistant"""
        backup_modules(str(backup_target), "nonexistent_module")
        
        # Aucun zip ne devrait être créé
        zip_files = list(backup_target.glob("*.zip"))
        assert len(zip_files) == 0
        
        captured = capsys.readouterr()
        assert "❌ Module 'nonexistent_module' not found" in captured.out
    
    def test_backup_invalid_target_dir(self, mock_cwd, capsys):
        """Test backup vers un répertoire inexistant"""
        backup_modules("/nonexistent/directory", "test_module")
        
        captured = capsys.readouterr()
        assert "❌ Target directory '/nonexistent/directory' does not exist" in captured.out
    
    def test_backup_target_is_file(self, mock_cwd, tmp_path, capsys):
        """Test backup vers un fichier au lieu d'un répertoire"""
        target_file = tmp_path / "not_a_directory.txt"
        target_file.write_text("test")
        
        backup_modules(str(target_file), "test_module")
        
        captured = capsys.readouterr()
        assert f"❌ '{target_file}' is not a directory" in captured.out
    
    def test_backup_outside_project(self, mock_cwd_outside_project, backup_target, capsys):
        """Test backup en dehors d'un projet"""
        backup_modules(str(backup_target), "test_module")
        
        captured = capsys.readouterr()
        assert "❌ Project root not found" in captured.out
    
    def test_backup_empty_module(self, mock_cwd, backup_target, capsys):
        """Test backup d'un module vide"""
        # Créer un module vide
        empty_module = mock_cwd / "modules" / "empty_module"
        empty_module.mkdir()
        empty_data = mock_cwd / "data" / "empty_module"
        empty_data.mkdir()
        
        backup_modules(str(backup_target), "empty_module")
        
        # Aucun zip ne devrait être créé (ou supprimé s'il était vide)
        zip_files = list(backup_target.glob("empty_module_backup_*.zip"))
        assert len(zip_files) == 0
        
        captured = capsys.readouterr()
        assert "⚠️  No files found to backup for module 'empty_module'" in captured.out
    
    def test_backup_no_modules_directory(self, mock_cwd, backup_target, capsys):
        """Test backup quand il n'y a pas de dossier modules/"""
        import shutil
        shutil.rmtree(mock_cwd / "modules")
        
        backup_modules(str(backup_target))
        
        captured = capsys.readouterr()
        assert "❌ No modules directory found" in captured.out
    
    def test_backup_all_modules_empty_project(self, mock_cwd, backup_target, capsys):
        """Test backup de tous les modules dans un projet vide"""
        import shutil
        # Vider le dossier modules
        shutil.rmtree(mock_cwd / "modules")
        (mock_cwd / "modules").mkdir()
        
        backup_modules(str(backup_target))
        
        captured = capsys.readouterr()
        assert "❌ No modules found to backup" in captured.out


class TestBackupFileStructure:
    
    def test_zip_file_naming_with_timestamp(self, mock_cwd, backup_target):
        """Test que les noms de fichiers incluent un timestamp"""
        backup_modules(str(backup_target), "test_module")
        
        zip_files = list(backup_target.glob("test_module_backup_*.zip"))
        assert len(zip_files) == 1
        
        zip_name = zip_files[0].name
        # Le nom devrait contenir un timestamp au format YYYYMMDD_HHMMSS
        assert len(zip_name.split('_')[-1].replace('.zip', '')) == 6  # HHMMSS
        assert len(zip_name.split('_')[-2]) == 8  # YYYYMMDD
    
    def test_zip_file_naming_all_modules(self, mock_cwd, backup_target):
        """Test noms de fichiers pour backup de tous les modules"""
        backup_modules(str(backup_target))
        
        zip_files = list(backup_target.glob("all_modules_backup_*.zip"))
        assert len(zip_files) == 1
        
        zip_name = zip_files[0].name
        assert zip_name.startswith("all_modules_backup_")
    
    def test_multiple_backups_no_overwrite(self, mock_cwd, backup_target):
        """Test que les backups multiples ne s'écrasent pas"""
        backup_modules(str(backup_target), "test_module")
        backup_modules(str(backup_target), "test_module")
        
        # Devrait y avoir 2 fichiers zip différents
        zip_files = list(backup_target.glob("test_module_backup_*.zip"))
        assert len(zip_files) == 2
        
        # Les noms devraient être différents
        assert zip_files[0].name != zip_files[1].name
