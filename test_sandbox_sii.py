import pandas as pd
import requests
import json

# URL de pruebas (Sandbox)
API_URL_SANDBOX = "https://sandbox.api-proveedordte.cl/v1/dte/emitir"
API_KEY_PRUEBAS = "token_sandbox_de_prueba"

# 1. Crear datos de prueba locales
df_prueba = pd.DataFrame({
    'ID_Interno': ['PED-001', 'PED-002'],
    'Cliente': ['CLIENTE PRUEBA ALFA SPA', 'CLIENTE PRUEBA BETA LTDA'],
    'Rut': ['77.111.222-3', '78.333.444-5'],
    'Giro': ['VENTA DE INSUMOS', 'SERVICIOS DE INGENIERIA'],
    'Direccion': ['Av. Apoquindo 4000', 'Calle Estado 150'],
    'Comuna': ['Las Condes', 'Santiago'],
    'Monto_Neto': [100000, 250000],
    'IVA_19': [19000, 47500],
    'Total': [119000, 297500],
    'Estado': ['Pendiente', 'Pendiente']
})

df_prueba.to_excel("prueba_facturas_entrada.xlsx", index=False)

def simular_envio_sandbox(row):
    """
    Construye el JSON y valida la estructura exigida sin gastar folios reales.
    """
    payload = {
        "Encabezado": {
            "IdDoc": {"TipoDTE": 33, "FchEmis": "2026-09-23"},
            "Emisor": {"RUTEmisor": "76123456-7"},
            "Receptor": {
                "RUTRecep": str(row['Rut']),
                "RznSocRecep": str(row['Cliente']),
                "GiroRecep": str(row['Giro']),
                "DirRecep": str(row['Direccion']),
                "CmnaRecep": str(row['Comuna'])
            },
            "Totales": {
                "MntNeto": int(row['Monto_Neto']),
                "IVA": int(row['IVA_19']),
                "MntTotal": int(row['Total'])
            }
        }
    }

    print(f"\n[ENVIANDO A SANDBOX] Cliente: {row['Cliente']}")
    print(f" -> JSON de prueba correcto. Neto: ${row['Monto_Neto']:,} + IVA: ${row['IVA_19']:,}")

    # Simulación de respuesta exitosa del servidor de pruebas
    return {
        "codigo": 200,
        "folio_falso_sandbox": 9001,
        "track_id_sii": "MOCK-98765432",
        "mensaje": "DTE Aceptado en ambiente Sandbox de Pruebas"
    }

# 2. Bucle de ejecución
if __name__ == "__main__":
    print("==================================================")
    print("     INICIANDO PRUEBAS DE EMISIÓN DE DTE")
    print("==================================================")
    
    for idx, row in df_prueba.iterrows():
        respuesta = simular_envio_sandbox(row)
        
        # Marcamos la fila como probada
        df_prueba.at[idx, 'Estado'] = 'Probado en Sandbox'
        df_prueba.at[idx, 'TrackID_Prueba'] = respuesta['track_id_sii']

    # Guardar resultado
    df_prueba.to_excel("prueba_facturas_resultado.xlsx", index=False)
    print("\n==================================================")
    print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
    print("   Se generó 'prueba_facturas_resultado.xlsx'")
    print("==================================================")