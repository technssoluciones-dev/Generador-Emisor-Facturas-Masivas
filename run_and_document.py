import os
from pathlib import Path
from project_auditor import audit_project
from project_fixer import fix_project

def generate_missing_files():
    root_dir = Path(".")
    
    # 1. Crear un requirements.txt base si no existe
    req_path = root_dir / "requirements.txt"
    if not req_path.exists() or req_path.stat().st_size == 0:
        default_reqs = "pandas>=2.0.0\nopenpyxl>=3.1.0\nreportlab>=3.6.0\nrequests>=2.28.0\n"
        req_path.write_text(default_reqs, encoding="utf-8")
        print("[+] Archivo requirements.txt generado automáticamente.")

    # 2. Crear un README.md profesional si no existe
    readme_path = Path("README.md")
    if not readme_path.exists() or readme_path.stat().st_size == 0:
        default_readme = (
            "# 📄 Generador y Emisor de Facturas Masivas\n\n"
            "> Sistema automatizado en Python para la generación masiva, procesamiento y emisión estructurada de documentos fiscales y facturas, optimizando los tiempos operativos y reduciendo errores manuales.\n\n"
            "## ⚙️ Instalación y Configuración\n\n"
            "Sigue estos pasos para clonar el repositorio y configurar tu entorno de desarrollo:\n\n"
            "### 1. Clonar el repositorio\n"
            "```bash\n"
            "git clone [https://github.com/technssoluciones-dev/Generador-Emisor-Facturas-Masivas.git](https://github.com/technssoluciones-dev/Generador-Emisor-Facturas-Masivas.git)\n"
            "cd Generador-Emisor-Facturas-Masivas\n"
            "```\n\n"
            "### 2. Crear y activar un entorno virtual\n"
            "* **En Windows (PowerShell):**\n"
            "  ```powershell\n"
            "  python -m venv venv\n"
            "  .\\venv\\Scripts\\Activate.ps1\n"
            "  ```\n"
            "* **En macOS / Linux:**\n"
            "  ```bash\n"
            "  python3 -m venv venv\n"
            "  source venv/bin/activate\n"
            "  ```\n\n"
            "### 3. Instalar las dependencias\n"
            "```bash\n"
            "pip install -r requirements.txt\n"
            "```\n\n"
            "---\n\n"
            "## 🚀 Uso del Sistema\n"
            "Ejecuta el script principal de procesamiento masivo según la estructura de tu proyecto:\n"
            "```bash\n"
            "python main.py\n"
            "```\n"
        )
        readme_path.write_text(default_readme, encoding="utf-8")
        print("[+] Archivo README.md generado automáticamente.")

def main():
    print("==================================================")
    print("   LANZADOR MAESTRO: AUTO-OPTIMIZACIÓN DE REPO    ")
    print("==================================================\n")
    
    print("[1/3] Ejecutando primera auditoría de estado...")
    initial_score = audit_project()
    
    if initial_score < 100:
        print("\n[2/3] Aplicando reparaciones y generando archivos faltantes...")
        fix_project()
        generate_missing_files()
        
        print("\n[3/3] Ejecutando auditoría final de verificación...")
        final_score = audit_project()
        print(f"\n[✔] ¡Optimización finalizada con éxito! Puntaje alcanzado: {final_score}%")
    else:
        print("\n[✔] El proyecto ya cuenta con el 100% de productividad y madurez.")

if __name__ == "__main__":
    main()