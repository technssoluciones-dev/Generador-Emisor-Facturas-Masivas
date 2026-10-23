import pandas as pd
import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# ==============================================================================
# 1. FUNCIÓN DE GENERACIÓN DE PDF MULTI-ÍTEM (ESTILO SII)
# ==============================================================================
def generar_factura_sii_profesional(datos_factura, ruta_pdf):
    """Genera el PDF con formato oficial del SII soportando múltiples ítems."""
    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    story = []
    styles = getSampleStyleSheet()

    # Recuadro Rojo Tributario (SII)
    datos_sii = [
        [Paragraph("<font color='red'><b>R.U.T.: 76.123.456-7</b></font>", styles['Normal'])],
        [Paragraph("<font color='red'><b>FACTURA ELECTRÓNICA</b></font>", styles['Normal'])],
        [Paragraph(f"<font color='red'><b>Nº {datos_factura['ID_Factura']}</b></font>", styles['Normal'])],
        [Paragraph("<font color='red'><b>S.I.I. - SANTIAGO ORIENTE</b></font>", styles['Normal'])]
    ]
    tabla_sii = Table(datos_sii, colWidths=[200])
    tabla_sii.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 2, colors.red),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))

    # Encabezado Emisor
    emisor_text = """<b>MI EMPRESA AUTOMATIZADA SpA</b><br/>
    <b>Giro:</b> Servicios Informáticos, Software y Automatización<br/>
    <b>Dirección:</b> Av. Providencia 1234, Of. 501 - Providencia<br/>
    <b>Teléfono:</b> +56 2 2345 6789 | <b>Email:</b> contacto@miempresa.cl"""
    p_emisor = Paragraph(emisor_text, styles['Normal'])

    header_table = Table([[p_emisor, tabla_sii]], colWidths=[330, 210])
    header_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(header_table)
    story.append(Spacer(1, 15))

    # Datos del Receptor (Cliente)
    receptor_data = [
        [
            Paragraph(f"<b>Señor(es):</b> {datos_factura['Cliente']}", styles['Normal']),
            Paragraph(f"<b>Fecha Emisión:</b> {datos_factura['Fecha']}", styles['Normal'])
        ],
        [
            Paragraph(f"<b>R.U.T.:</b> {datos_factura['Rut_Ruc']}", styles['Normal']),
            Paragraph("<b>Forma de Pago:</b> Crédito / Contado", styles['Normal'])
        ],
        [
            Paragraph(f"<b>Giro:</b> {datos_factura.get('Giro', 'Servicios Varios')}", styles['Normal']),
            Paragraph(f"<b>Comuna:</b> {datos_factura.get('Comuna', 'Santiago')}", styles['Normal'])
        ],
        [
            Paragraph(f"<b>Dirección:</b> {datos_factura.get('Direccion', 'Dirección Comercial')}", styles['Normal']),
            Paragraph("<b>Ciudad:</b> Santiago", styles['Normal'])
        ]
    ]
    t_receptor = Table(receptor_data, colWidths=[340, 200])
    t_receptor.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#a0a0a0')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9f9f9')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_receptor)
    story.append(Spacer(1, 15))

    # Tabla de Detalle con Múltiples Ítems
    detalle_data = [["Código", "Descripción / Concepto", "Cant.", "P. Unitario", "Monto Neto"]]
    
    for item in datos_factura['Items']:
        p_unit = f"${item['Precio_Unitario']:,.0f}".replace(",", ".")
        subtot = f"${item['Subtotal_Neto']:,.0f}".replace(",", ".")
        detalle_data.append([
            item['Codigo'],
            Paragraph(item['Concepto'], styles['Normal']),
            str(item['Cantidad']),
            p_unit,
            subtot
        ])

    t_detalle = Table(detalle_data, colWidths=[60, 260, 40, 90, 90])
    t_detalle.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a2a3a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
        ('ALIGN', (3,0), (-1,-1), 'RIGHT'),
        ('ALIGN', (4,0), (-1,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_detalle)
    story.append(Spacer(1, 15))

    # Totales
    neto_fmt = f"${datos_factura['Monto_Neto']:,.0f}".replace(",", ".")
    iva_fmt = f"${datos_factura['IVA_19']:,.0f}".replace(",", ".")
    total_fmt = f"${datos_factura['Total']:,.0f}".replace(",", ".")

    totales_data = [
        ["Monto Neto:", neto_fmt],
        ["19% I.V.A.:", iva_fmt],
        ["Monto Total:", total_fmt]
    ]
    t_totales = Table(totales_data, colWidths=[450, 90])
    t_totales.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,-1), (-1,-1), colors.HexColor('#1a2a3a')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_totales)

    doc.build(story)


# ==============================================================================
# 2. PROCESAMIENTO DINÁMICO DE EXCEL
# ==============================================================================
def procesar_excel_masivo(ruta_excel):
    """Lee cualquier Excel especificado y genera las facturas en PDF dinámicamente."""
    output_dir = "Facturas_PDF"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Limpiar comillas si el usuario arrastra el archivo a la terminal
    ruta_excel = ruta_excel.strip("'\"")

    if not os.path.exists(ruta_excel):
        print(f"\n❌ Error: El archivo '{ruta_excel}' no fue encontrado.")
        return

    df = pd.read_excel(ruta_excel)

    # Validar que exista la columna mínima requerida
    if 'ID_Factura' not in df.columns:
        print("\n❌ Error: El Excel debe incluir al menos la columna 'ID_Factura'.")
        return

    # Agrupar las filas por ID_Factura
    facturas_agrupadas = df.groupby('ID_Factura')

    print("\n==================================================")
    print(f"   PROCESANDO {len(facturas_agrupadas)} FACTURA(S) DESDE: {os.path.basename(ruta_excel)}")
    print("==================================================")

    resumen_procesados = []

    for id_factura, grupo in facturas_agrupadas:
        primer_registro = grupo.iloc[0]
        
        items = []
        monto_neto_total = 0.0

        for idx, (_, row) in enumerate(grupo.iterrows(), 1):
            cantidad = int(row.get('Cantidad', 1))
            
            # Cálculo flexible de precios
            if 'Precio_Unitario' in row and pd.notna(row['Precio_Unitario']):
                precio_unitario = float(row['Precio_Unitario'])
                subtotal = cantidad * precio_unitario
            elif 'Monto_Neto' in row and pd.notna(row['Monto_Neto']):
                subtotal = float(row['Monto_Neto'])
                precio_unitario = subtotal / cantidad if cantidad > 0 else 0.0
            else:
                subtotal = 0.0
                precio_unitario = 0.0

            monto_neto_total += subtotal

            items.append({
                'Codigo': str(row.get('Codigo', f"SRV-{idx:02d}")),
                'Concepto': str(row.get('Concepto', row.get('Descripcion', 'Servicio'))),
                'Cantidad': cantidad,
                'Precio_Unitario': precio_unitario,
                'Subtotal_Neto': subtotal
            })

        iva = round(monto_neto_total * 0.19)
        total = monto_neto_total + iva

        fecha_val = primer_registro.get('Fecha', datetime.now().strftime("%Y-%m-%d"))
        if isinstance(fecha_val, datetime):
            fecha_val = fecha_val.strftime("%Y-%m-%d")

        datos_factura = {
            'ID_Factura': str(id_factura),
            'Cliente': str(primer_registro.get('Cliente', 'Cliente General')),
            'Rut_Ruc': str(primer_registro.get('Rut_Ruc', 'N/A')),
            'Email': str(primer_registro.get('Email', 'N/A')),
            'Fecha': str(fecha_val),
            'Giro': str(primer_registro.get('Giro', 'Servicios Varios')),
            'Comuna': str(primer_registro.get('Comuna', 'Santiago')),
            'Direccion': str(primer_registro.get('Direccion', 'Dirección Comercial')),
            'Items': items,
            'Monto_Neto': monto_neto_total,
            'IVA_19': iva,
            'Total': total
        }

        nombre_pdf = f"{id_factura}.pdf"
        ruta_pdf = os.path.join(output_dir, nombre_pdf)
        generar_factura_sii_profesional(datos_factura, ruta_pdf)
        print(f"📄 PDF Generado: {ruta_pdf} ({len(items)} ítem/s)")

        resumen_conceptos = " | ".join([f"{it['Concepto']} (x{it['Cantidad']})" for it in items])
        resumen_procesados.append({
            'ID_Factura': id_factura,
            'Cliente': datos_factura['Cliente'],
            'Rut_Ruc': datos_factura['Rut_Ruc'],
            'Email': datos_factura['Email'],
            'Fecha': datos_factura['Fecha'],
            'Conceptos_Incluidos': resumen_conceptos,
            'Monto_Neto': monto_neto_total,
            'IVA_19': iva,
            'Total': total,
            'Estado': 'PDF Generado desde Excel'
        })

    # Guardar reporte de salida basado en el nombre original
    directorio, nombre_archivo = os.path.split(ruta_excel)
    nombre_salida = f"reporte_{nombre_archivo}"
    ruta_salida = os.path.join(directorio, nombre_salida) if directorio else nombre_salida

    df_resultado = pd.DataFrame(resumen_procesados)
    df_resultado.to_excel(ruta_salida, index=False)
    print("==================================================")
    print(f"✅ Proceso completado. Reporte generado en '{ruta_salida}'")
    print("==================================================")


# ==============================================================================
# 3. CAPTURA INTERACTIVA POR TERMINAL
# ==============================================================================
def capturar_datos_por_terminal():
    """Solicita los datos del encabezado e itera para capturar múltiples ítems."""
    print("\n--------------------------------------------------")
    print("   INGRESO MANUAL DE FACTURA (MÚLTIPLES ÍTEMS)")
    print("--------------------------------------------------")
    
    id_fac = input("Nº / Folio Factura (ej: FAC-2026-005): ").strip() or "FAC-2026-005"
    cliente = input("Razón Social / Cliente: ").strip() or "Servicios Generales Ltda."
    rut = input("RUT / ID Fiscal (ej: 76.888.999-1): ").strip() or "76.888.999-1"
    email = input("Email Cliente: ").strip() or "contacto@cliente.cl"
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    fecha = input(f"Fecha (AAAA-MM-DD) [Enter para {fecha_hoy}]: ").strip() or fecha_hoy

    while True:
        try:
            num_items = int(input("\n¿Cuántos servicios/productos incluirá esta factura?: ").strip())
            if num_items > 0:
                break
            print("⚠️ Debe ingresar al menos 1 ítem.")
        except ValueError:
            print("⚠️ Ingrese un número entero válido.")

    items = []
    monto_neto_total = 0.0

    for idx in range(1, num_items + 1):
        print(f"\n--- Ítem {idx} de {num_items} ---")
        concepto = input(f"  Descripción del producto/servicio #{idx}: ").strip() or f"Servicio #{idx}"
        
        while True:
            try:
                cantidad = int(input("  Cantidad: ").strip())
                if cantidad > 0:
                    break
                print("  ⚠️ La cantidad debe ser mayor a 0.")
            except ValueError:
                print("  ⚠️ Ingrese una cantidad entera válida.")

        while True:
            try:
                precio_unitario = float(input("  Precio Unitario Neto (CLP $): ").replace('.', '').strip())
                if precio_unitario >= 0:
                    break
                print("  ⚠️ El precio debe ser un número positivo.")
            except ValueError:
                print("  ⚠️ Ingrese un número válido.")

        subtotal = cantidad * precio_unitario
        monto_neto_total += subtotal

        items.append({
            'Codigo': f"SRV-{idx:02d}",
            'Concepto': concepto,
            'Cantidad': cantidad,
            'Precio_Unitario': precio_unitario,
            'Subtotal_Neto': subtotal
        })

    iva = round(monto_neto_total * 0.19)
    total = monto_neto_total + iva

    datos_factura = {
        'ID_Factura': id_fac,
        'Cliente': cliente,
        'Rut_Ruc': rut,
        'Email': email,
        'Fecha': fecha,
        'Items': items,
        'Monto_Neto': monto_neto_total,
        'IVA_19': iva,
        'Total': total
    }

    return datos_factura


def guardar_factura_individual(datos_factura):
    """Guarda el PDF generado por terminal y lo registra en el histórico Excel."""
    output_dir = "Facturas_PDF"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    nombre_pdf = f"{datos_factura['ID_Factura']}.pdf"
    ruta_completa = os.path.join(output_dir, nombre_pdf)

    generar_factura_sii_profesional(datos_factura, ruta_completa)
    print(f"\n📄 PDF Generado con éxito: {ruta_completa}")

    resumen_conceptos = " | ".join([f"{item['Concepto']} (x{item['Cantidad']})" for item in datos_factura['Items']])
    
    registro_excel = [{
        'ID_Factura': datos_factura['ID_Factura'],
        'Cliente': datos_factura['Cliente'],
        'Rut_Ruc': datos_factura['Rut_Ruc'],
        'Email': datos_factura['Email'],
        'Fecha': datos_factura['Fecha'],
        'Conceptos_Incluidos': resumen_conceptos,
        'Monto_Neto': datos_factura['Monto_Neto'],
        'IVA_19': datos_factura['IVA_19'],
        'Total': datos_factura['Total'],
        'Estado': 'PDF Generado desde Terminal'
    }]

    df_nuevo = pd.DataFrame(registro_excel)
    archivo_excel = "facturas_emision_actualizado.xlsx"

    if os.path.exists(archivo_excel):
        df_existente = pd.read_excel(archivo_excel)
        df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
    else:
        df_final = df_nuevo

    df_final.to_excel(archivo_excel, index=False)
    print("==================================================")
    print("✅ Registro guardado en 'facturas_emision_actualizado.xlsx'")
    print("==================================================")


# ==============================================================================
# 4. MENÚ PRINCIPAL
# ==============================================================================
def menu_principal():
    print("\n" + "="*50)
    print("   SISTEMA DE EMISIÓN DE FACTURAS Y AUTOMATIZACIÓN")
    print("="*50)
    print("1. Cargar archivo Excel masivo (Ruta personalizable)")
    print("2. Iniciar ingreso manual por terminal (Múltiples Ítems)")
    print("3. Salir")
    print("="*50)

    opcion = input("Seleccione una opción (1-3): ").strip()

    if opcion == '1':
        archivo = input("\nIngrese el nombre o ruta del Excel (ej: facturas_1.xlsx) [Enter por defecto]: ").strip()
        if not archivo:
            archivo = "facturas_emision.xlsx"
        
        procesar_excel_masivo(archivo)

    elif opcion == '2':
        datos = capturar_datos_por_terminal()
        guardar_factura_individual(datos)

    elif opcion == '3':
        print("\nSaliendo del sistema...")
        sys.exit()
    else:
        print("\n⚠️ Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    while True:
        menu_principal()