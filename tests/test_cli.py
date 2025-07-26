from pathlib import Path
import sys
from unittest.mock import patch

# Import the module under test
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from modular_data_lab.run import main, show_help, setup


class TestShowHelp:
    
    def test_show_help_output(self, capsys):
        """Test que l'aide s'affiche correctement"""
        show_help()
        
        captured = capsys.readouterr()
        assert "📋 Available Commands:" in captured.out
        assert "lab add <module_name>" in captured.out
        assert "lab backup <module_name> <dir>" in captured.out
        assert "🔧 Backup Options:" in captured.out
        assert "-d, --data" in captured.out
        assert "-c, --code" in captured.out


class TestSetup:
    
    def test_setup_creates_directories(self, tmp_path, monkeypatch, capsys):
        """Test que setup crée les répertoires"""
        monkeypatch.chdir(tmp_path)
        
        setup()
        
        # Vérifier que les dossiers ont été créés
        assert (tmp_path / "modules").exists()
        assert (tmp_path / "data").exists()
        
        captured = capsys.readouterr()
        assert "🚀 Project Initialization" in captured.out
        assert "Created Folder: modules/" in captured.out
        assert "Created Folder: data/" in captured.out
        assert "✅ Base Structure Created!" in captured.out


class TestMain:
    
    def test_main_no_args_shows_help(self, capsys):
        """Test que main sans arguments affiche l'aide"""
        with patch('sys.argv', ['lab']):
            main()
        
        captured = capsys.readouterr()
        assert "📋 Available Commands:" in captured.out
    
    def test_main_help_command(self, capsys):
        """Test commande help"""
        with patch('sys.argv', ['lab', 'help']):
            main()
        
        captured = capsys.readouterr()
        assert "📋 Available Commands:" in captured.out
    
    @patch('modular_data_lab.run.create_module')
    def test_main_add_command(self, mock_create, capsys):
        """Test commande add"""
        with patch('sys.argv', ['lab', 'add', 'test_module']):
            main()
        
        mock_create.assert_called_once_with('test_module')
    
    @patch('modular_data_lab.run.list_modules')
    def test_main_list_command(self, mock_list, capsys):
        """Test commande list"""
        with patch('sys.argv', ['lab', 'list']):
            main()
        
        mock_list.assert_called_once()
    
    @patch('modular_data_lab.run.run_module')
    def test_main_run_command(self, mock_run, capsys):
        """Test commande run"""
        with patch('sys.argv', ['lab', 'run', 'test_module']):
            main()
        
        mock_run.assert_called_once_with('test_module')
    
    @patch('modular_data_lab.run.remove_module')
    def test_main_remove_command(self, mock_remove, capsys):
        """Test commande remove"""
        with patch('sys.argv', ['lab', 'remove', 'test_module']):
            main()
        
        mock_remove.assert_called_once_with('test_module')
    
    @patch('modular_data_lab.run.setup')
    def test_main_setup_command(self, mock_setup, capsys):
        """Test commande setup"""
        with patch('sys.argv', ['lab', 'setup']):
            main()
        
        mock_setup.assert_called_once()
    
    @patch('modular_data_lab.run.backup_modules')
    def test_main_backup_single_module(self, mock_backup, capsys):
        """Test backup d'un module spécifique"""
        with patch('sys.argv', ['lab', 'backup', 'test_module', './backups']):
            main()
        
        mock_backup.assert_called_once_with('./backups', 'test_module', False, False)
    
    @patch('modular_data_lab.run.backup_modules')
    def test_main_backup_all_modules(self, mock_backup, capsys):
        """Test backup de tous les modules"""
        with patch('sys.argv', ['lab', 'backup', './backups']):
            main()
        
        mock_backup.assert_called_once_with('./backups', None, False, False)
    
    @patch('modular_data_lab.run.backup_modules')
    def test_main_backup_with_data_flag(self, mock_backup, capsys):
        """Test backup avec flag --data"""
        with patch('sys.argv', ['lab', 'backup', 'test_module', './backups', '-d']):
            main()
        
        mock_backup.assert_called_once_with('./backups', 'test_module', True, False)
    
    @patch('modular_data_lab.run.backup_modules')
    def test_main_backup_with_code_flag(self, mock_backup, capsys):
        """Test backup avec flag --code"""
        with patch('sys.argv', ['lab', 'backup', 'test_module', './backups', '--code']):
            main()
        
        mock_backup.assert_called_once_with('./backups', 'test_module', False, True)
    
    @patch('modular_data_lab.run.backup_modules')
    def test_main_backup_all_with_flags(self, mock_backup, capsys):
        """Test backup de tous les modules avec flags"""
        with patch('sys.argv', ['lab', 'backup', './backups', '-d']):
            main()
        
        mock_backup.assert_called_once_with('./backups', None, True, False)
    
    def test_main_invalid_command(self, capsys):
        """Test commande invalide"""
        with patch('sys.argv', ['lab', 'invalid_command']):
            main()
        
        captured = capsys.readouterr()
        assert "❌ Invalid command" in captured.out
        assert "📋 Available Commands:" in captured.out
    
    def test_main_incomplete_add_command(self, capsys):
        """Test commande add incomplète"""
        with patch('sys.argv', ['lab', 'add']):
            main()
        
        captured = capsys.readouterr()
        assert "❌ Invalid command" in captured.out
    
    def test_main_incomplete_run_command(self, capsys):
        """Test commande run incomplète"""
        with patch('sys.argv', ['lab', 'run']):
            main()
        
        captured = capsys.readouterr()
        assert "❌ Invalid command" in captured.out
    
    def test_main_incomplete_backup_command(self, capsys):
        """Test commande backup incomplète"""
        with patch('sys.argv', ['lab', 'backup']):
            main()
        
        captured = capsys.readouterr()
        assert "❌ Invalid command" in captured.out


class TestFlagParsing:
    """Tests spécifiques pour le parsing des flags"""
    
    @patch('modular_data_lab.run.backup_modules')
    def test_flag_parsing_both_short_and_long(self, mock_backup):
        """Test que les flags courts et longs sont reconnus"""
        # Test flag court -d
        with patch('sys.argv', ['lab', 'backup', './backups', '-d']):
            main()
        mock_backup.assert_called_with('./backups', None, True, False)
        
        mock_backup.reset_mock()
        
        # Test flag long --data
        with patch('sys.argv', ['lab', 'backup', './backups', '--data']):
            main()
        mock_backup.assert_called_with('./backups', None, True, False)
    
    @patch('modular_data_lab.run.backup_modules')
    def test_flag_parsing_multiple_flags(self, mock_backup):
        """Test parsing avec plusieurs flags (même si invalide)"""
        with patch('sys.argv', ['lab', 'backup', './backups', '-d', '-c']):
            main()
        # Les deux flags devraient être détectés
        mock_backup.assert_called_with('./backups', None, True, True)
    
    @patch('modular_data_lab.run.backup_modules')
    def test_flag_position_independence(self, mock_backup):
        """Test que la position des flags n'importe pas"""
        # Flag au milieu
        with patch('sys.argv', ['lab', 'backup', '-d', 'test_module', './backups']):
            main()
        mock_backup.assert_called_with('./backups', 'test_module', True, False)
        
        mock_backup.reset_mock()
        
        # Flag à la fin
        with patch('sys.argv', ['lab', 'backup', 'test_module', './backups', '-d']):
            main()
        mock_backup.assert_called_with('./backups', 'test_module', True, False)
