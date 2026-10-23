import pandas as pd

datos_facturas = {
    'ID_Factura': ['FAC-2026-001', 'FAC-2026-002', 'FAC-2026-003'],
    'Cliente': ['Empresa Alfa S.A.', 'Comercial Beta SpA', 'Servicios Gamma Ltda.'],
    'Rut_Ruc': ['76.123.456-7', '77.987.654-3', '78.555.444-1'],
    'Email': ['cliente1@ejemplo.com', 'cliente2@ejemplo.com', 'cliente3@ejemplo.com'],
    'Fecha': ['2026-09-22', '2026-09-22', '2026-09-22'],
    'Concepto': ['Servicio de Consultoría TI', 'Mantenimiento de Servidores', 'Licenciamiento de Software'],
    'Monto_Neto': [1500000, 850000, 2300000],
    'IVA_19': [285000, 161500, 437000],
    'Total': [1785000, 1011500, 2737000],
    'Estado': ['Pendiente', 'Pendiente', 'Pendiente']
}

df = pd.DataFrame(datos_facturas)
df.to_excel('facturas_emision.xlsx', index=False)
print("✅ Archivo 'facturas_emision.xlsx' creado exitosamente.")