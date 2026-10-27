import os
from pathlib import Path

def fix_project():
    print("==================================================")
    print("   REPARADOR Y OPTIMIZADOR AUTOMÁTICO DE REPO     ")
    print("==================================================\n")
    
    root_dir = Path(".")
    
    # 1. Crear directorios clave (incluyendo .github/workflows para GitHub Actions)
    dirs_to_create = ["tests", "assets", ".github/workflows"]
    for d in dirs_to_create:
        dir_path = root_dir / d
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"[+] Directorio creado: {d}/")
            
    # 2. Crear el archivo de GitHub Actions (ci.yml) para que pase en verde
    ci_path = root_dir / ".github" / "workflows" / "ci.yml"
    ci_content = """name: CI Auditor & Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-verify:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
        
    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install pytest
        
    - name: Run Project Auditor
      run: python project_auditor.py
      
    - name: Run Unit Tests
      run: pytest
"""
    if not ci_path.exists():
        ci_path.write_text(ci_content, encoding="utf-8")
        print("[+] Archivo de configuración de GitHub Actions (.github/workflows/ci.yml) creado.")
    else:
        print("[*] El archivo de GitHub Actions ya existe.")

    # 3. Asegurar un archivo .gitignore seguro
    gitignore_path = root_dir / ".gitignore"
    gitignore_content = """# Entornos virtuales y cachés
venv/
.venv/
__pycache__/
.pytest_cache/
.env
*.log

# Archivos de datos fiscales, facturas de prueba y planillas (Privacidad)
*.xlsx
*.xls
*.csv
*.pdf
output/
facturas_generadas/
"""
    if not gitignore_path.exists():
        gitignore_path.write_text(gitignore_content, encoding="utf-8")
        print("[+] Archivo .gitignore creado exitosamente.")
    else:
        print("[*] El archivo .gitignore ya existe.")
        
    # 4. Asegurar estructura de tests básica si no existe
    test_init = root_dir / "tests" / "__init__.py"
    if not test_init.exists():
        test_init.write_text("# Inicializador de pruebas", encoding="utf-8")
        print("[+] Archivo tests/__init__.py creado.")
        
    print("\n[✔] ¡Reparación y preparación para GitHub Actions completada con éxito!")

if __name__ == "__main__":
    fix_project()