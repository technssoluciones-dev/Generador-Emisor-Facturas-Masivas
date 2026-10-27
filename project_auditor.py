import os
from pathlib import Path

def audit_project():
    print("==================================================")
    print("   AUDITOR DE PRODUCTIVIDAD Y ESTADO DEL PROYECTO ")
    print("==================================================\n")
    
    root_dir = Path(".")
    score = 100
    deductions = []
    
    # 1. Verificar archivos esenciales
    essential_files = ["README.md", ".gitignore", "requirements.txt"]
    for file in essential_files:
        if not (root_dir / file).exists():
            score -= 15
            deductions.append(f"Falta archivo esencial: {file} (-15%)")
            
    # 2. Verificar carpetas clave
    expected_dirs = ["tests", "assets"]
    for d in expected_dirs:
        if not (root_dir / d).is_dir():
            score -= 10
            deductions.append(f"Falta directorio clave: {d}/ (-10%)")
            
    # 3. Comprobar archivos de código Python
    py_files = list(root_dir.glob("*.py"))
    if len(py_files) == 0:
        score -= 30
        deductions.append("No se encontraron scripts principales de Python en la raíz (-30%)")
    else:
        print(f"[+] Scripts de Python detectados en la raíz: {len(py_files)}")

    # 4. Verificar dependencias en requirements.txt
    req_path = root_dir / "requirements.txt"
    if req_path.exists():
        req_content = req_path.read_text(encoding="utf-8").strip()
        if not req_content:
            score -= 10
            deductions.append("El archivo requirements.txt está vacío (-10%)")
            
    # 5. Asegurar límites del score
    score = max(0, score)
    
    print("\n--------------------------------------------------")
    print(f"📊 ÍNDICE DE PRODUCTIVIDAD Y MADUREZ: {score}%")
    print("--------------------------------------------------")
    
    if score == 100:
        print("[✔] ¡El proyecto está 100% operativo y cumple con todos los estándares profesionales!")
    else:
        print("[!] Oportunidades de mejora detectadas:")
        for deduction in deductions:
            print(f"    - {deduction}")
            
    print("==================================================\n")
    return score

if __name__ == "__main__":
    audit_project()