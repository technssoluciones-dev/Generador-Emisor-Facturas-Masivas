import subprocess
import sys

def run_local_ci():
    print("==================================================")
    print("   SIMULADOR LOCAL DE CI (GITHUB ACTIONS)         ")
    print("==================================================\n")
    
    # 1. Ejecutar el Auditor
    print("[*] Paso 1: Ejecutando auditoría de productividad...")
    auditor_result = subprocess.run([sys.executable, "project_auditor.py"])
    if auditor_result.returncode != 0:
        print("[✘] Error: La auditoría del proyecto falló.")
        sys.exit(1)
        
    # 2. Ejecutar Pruebas con pytest
    print("\n[*] Paso 2: Ejecutando pruebas unitarias (pytest)...")
    pytest_result = subprocess.run([sys.executable, "-m", "pytest"])
    if pytest_result.returncode != 0:
        print("[✘] Error: Hay pruebas unitarias fallando.")
        sys.exit(1)
        
    print("\n==================================================")
    print(" [✔] ¡TODO OK! El código está listo para hacer push y pasar en VERDE en GitHub Actions.")
    print("==================================================")

if __name__ == "__main__":
    run_local_ci()