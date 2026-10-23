import os
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

CARPETA_PDF = "Facturas_PDF_Test"
os.makedirs(CARPETA_PDF, exist_ok=True)

# 1. Crear datos de prueba directamente en el script
datos = {
    'ID_Factura': ['FAC-2026-001', 'FAC-2026-002', 'FAC-2026-003'],
    'Cliente': ['Empresa Alfa S.A.', 'Comercial Beta SpA', 'Servicios Gamma Ltda.'],
    'Rut_Ruc': ['76.123.456-7', '77.987.654-3', '78.555.444-1'],
    'Email': ['alfa@prueba.com', 'beta@prueba.com', 'gamma@prueba.com'],
    'Fecha': ['2026-09-22', '2026-09-22', '2026-09-22'],
    'Concepto': ['Servicio de Consultoría TI', 'Mantenimiento de Servidores', 'Licenciamiento Software'],
    'Monto_Neto': [1500000, 850000, 2300000],
    'IVA_19': [285000, 161500, 437000],
    'Total': [1785000, 1011500, 2737000],
    'Estado': ['Pendiente', 'Pendiente', 'Pendiente']
}

df = pd.DataFrame(datos)

def generar_pdf(row, ruta_pdf):
    doc = SimpleDocTemplate(ruta_pdf, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []

    # Encabezado
    story.append(Paragraph(f"<b>FACTURA: {row['ID_Factura']}</b>", styles['Heading1']))
    story.append(Paragraph(f"<b>Cliente:</b> {row['Cliente']} ({row['Rut_Ruc']})", styles['Normal']))
    story.append(Paragraph(f"<b>Fecha:</b> {row['Fecha']}", styles['Normal']))
    story.append(Spacer(1, 15))

    # Tabla de Detalle
    tabla_datos = [
        ['Concepto', 'Neto', 'IVA (19%)', 'Total'],
        [
            row['Concepto'],
            f"${row['Monto_Neto']:,.0f}",
            f"${row['IVA_19']:,.0f}",
            f"${row['Total']:,.0f}"
        ]
    ]
    
    t = Table(tabla_datos, colWidths=[240, 90, 90, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F4E78')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))
    
    story.append(t)
    doc.build(story)

# 2. Bucle de ejecución en consola
print("\n" + "="*50)
print("  EJECUTANDO GENERADOR DE FACTURAS EN TERMINAL")
print("="*50 + "\n")

for idx, row in df.iterrows():
    ruta_pdf = os.path.join(CARPETA_PDF, f"{row['ID_Factura']}.pdf")
    generar_pdf(row, ruta_pdf)
    print(f"  [PDF GENERADO] -> {ruta_pdf}")

print("\n" + "="*50)
print(f"✅ ¡Proceso finalizado! Revisa la carpeta '{CARPETA_PDF}/'")
print("="*50 + "\n")