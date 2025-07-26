import pytest
from pathlib import Path
import sys

# Import the module under test
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from modular_data_lab.templates import get_templates


class TestGetTemplates:
    
    def test_get_templates_returns_dict(self):
        """Test que get_templates retourne un dictionnaire"""
        templates = get_templates()
        assert isinstance(templates, dict)
    
    def test_get_templates_has_required_files(self):
        """Test que tous les fichiers requis sont présents"""
        templates = get_templates()
        
        required_files = ["run.py", "load_data.py", "analyze.py"]
        for file_name in required_files:
            assert file_name in templates
            assert isinstance(templates[file_name], str)
            assert len(templates[file_name]) > 0
    
    def test_run_template_content(self):
        """Test le contenu du template run.py"""
        templates = get_templates()
        run_content = templates["run.py"]
        
        # Vérifier la structure de base
        assert 'def run() -> None:' in run_content
        assert 'from load_data import load_data' in run_content
        assert 'from analyze import analyze' in run_content
        assert '{module_name}' in run_content
        assert 'if __name__ == "__main__":' in run_content
    
    def test_load_data_template_content(self):
        """Test le contenu du template load_data.py"""
        templates = get_templates()
        load_data_content = templates["load_data.py"]
        
        # Vérifier la structure de base
        assert 'def load_data() -> None:' in load_data_content
        assert 'from pathlib import Path' in load_data_content
        assert '{module_name}' in load_data_content
        assert 'data_dir = Path(__file__).parent.parent.parent / "data"' in load_data_content
    
    def test_analyze_template_content(self):
        """Test le contenu du template analyze.py"""
        templates = get_templates()
        analyze_content = templates["analyze.py"]
        
        # Vérifier la structure de base
        assert 'def analyze(data) -> None:' in analyze_content
        assert '{module_name}' in analyze_content
        assert 'TODO: Implement analysis' in analyze_content
    
    def test_template_formatting(self):
        """Test que les templates peuvent être formatés correctement"""
        templates = get_templates()
        module_name = "test_module"
        
        for file_name, template in templates.items():
            # Tenter de formater chaque template
            try:
                formatted = template.format(module_name=module_name)
                # Vérifier que le placeholder a été remplacé
                assert '{module_name}' not in formatted
                assert module_name in formatted
            except KeyError as e:
                pytest.fail(f"Template {file_name} contient un placeholder non supporté: {e}")
            except Exception as e:
                pytest.fail(f"Erreur lors du formatage du template {file_name}: {e}")


class TestTemplateIntegration:
    
    def test_formatted_templates_are_valid_python(self):
        """Test que les templates formatés produisent du Python valide"""
        import ast
        
        templates = get_templates()
        module_name = "valid_test_module"
        
        for file_name, template in templates.items():
            formatted = template.format(module_name=module_name)
            
            # Vérifier que c'est du Python syntaxiquement valide
            try:
                ast.parse(formatted)
            except SyntaxError as e:
                pytest.fail(f"Template {file_name} produit du Python invalide: {e}")
    
    def test_run_template_execution_structure(self):
        """Test que le template run.py a la structure d'exécution correcte"""
        templates = get_templates()
        run_template = templates["run.py"].format(module_name="test_execution")
        
        # Vérifier que les imports sont corrects
        assert 'from load_data import load_data' in run_template
        assert 'from analyze import analyze' in run_template
        
        # Vérifier la fonction main
        assert 'def run() -> None:' in run_template
        assert 'data = load_data()' in run_template
        assert 'results = analyze(data)' in run_template
        
        # Vérifier le point d'entrée
        assert 'if __name__ == "__main__":' in run_template
        assert 'run()' in run_template
    
    def test_load_data_path_structure(self):
        """Test que le template load_data.py utilise la bonne structure de chemins"""
        templates = get_templates()
        load_data_template = templates["load_data.py"].format(module_name="path_test")
        
        # Vérifier que le chemin vers les données est correct
        assert 'Path(__file__).parent.parent.parent / "data" / "path_test"' in load_data_template
        
        # Vérifier l'import de Path
        assert 'from pathlib import Path' in load_data_template
    
    def test_all_templates_have_docstrings(self):
        """Test que tous les templates ont des docstrings appropriées"""
        templates = get_templates()
        
        for file_name, template in templates.items():
            formatted = template.format(module_name="docstring_test")
            
            # Vérifier qu'il y a au moins une docstring de module
            assert '"""' in formatted
            
            # Vérifier des docstrings spécifiques selon le fichier
            if file_name == "run.py":
                assert '"""Module docstring_test"""' in formatted or 'Module docstring_test' in formatted
            elif file_name == "load_data.py":
                assert 'Load data for docstring_test' in formatted
            elif file_name == "analyze.py":
                assert 'Analyze data for docstring_test' in formatted


class TestTemplateCustomization:
    
    def test_template_extensibility(self):
        """Test que les templates peuvent être étendus facilement"""
        templates = get_templates()
        
        # Vérifier qu'on peut ajouter de nouveaux templates
        custom_templates = templates.copy()
        custom_templates["custom.py"] = "# Custom template for {module_name}"
        
        assert "custom.py" in custom_templates
        formatted = custom_templates["custom.py"].format(module_name="custom_test")
        assert "custom_test" in formatted
    
    def test_template_consistency(self):
        """Test la cohérence entre les templates"""
        templates = get_templates()
        
        # Tous les templates devraient utiliser le même placeholder
        for template in templates.values():
            # Compter les occurrences de {module_name}
            count = template.count('{module_name}')
            assert count > 0, "Template should contain at least one {module_name} placeholder"
    
    def test_template_no_hardcoded_names(self):
        """Test qu'aucun nom de module n'est codé en dur"""
        templates = get_templates()
        
        # Liste de noms qui ne devraient pas apparaître en dur
        forbidden_names = ["test_module", "example", "sample", "demo"]
        
        for file_name, template in templates.items():
            for forbidden in forbidden_names:
                # Ignorer les occurrences dans les commentaires TODO
                if forbidden in template and "TODO" not in template:
                    lines_with_forbidden = [line for line in template.split('\n') 
                                          if forbidden in line and "TODO" not in line]
                    if lines_with_forbidden:
                        pytest.fail(f"Template {file_name} contains hardcoded name '{forbidden}' in: {lines_with_forbidden}")


class TestTemplateEdgeCases:
    
    def test_empty_module_name(self):
        """Test avec un nom de module vide"""
        templates = get_templates()
        
        # Ne devrait pas lever d'exception
        for template in templates.values():
            formatted = template.format(module_name="")
            assert formatted is not None
    
    def test_special_characters_module_name(self):
        """Test avec des caractères spéciaux dans le nom du module"""
        templates = get_templates()
        
        # Caractères qui pourraient poser problème
        special_names = ["test-module", "test_module", "test.module", "test123"]
        
        for special_name in special_names:
            for template in templates.values():
                try:
                    formatted = template.format(module_name=special_name)
                    assert special_name in formatted
                except Exception as e:
                    pytest.fail(f"Template failed with module name '{special_name}': {e}")
    
    def test_long_module_name(self):
        """Test avec un nom de module très long"""
        templates = get_templates()
        long_name = "very_long_module_name_that_might_cause_issues_in_templates"
        
        for template in templates.values():
            formatted = template.format(module_name=long_name)
            assert long_name in formatted
            # Vérifier que la longueur ne casse pas la syntaxe
            import ast
            try:
                ast.parse(formatted)
            except SyntaxError:
                pytest.fail("Long module name breaks Python syntax in template")
