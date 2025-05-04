
import tkinter as tk
import os 
from tkinter import messagebox

import pandas as pd  # Para generar reporte Excel
from reportlab.lib.pagesizes import letter  # Para definir tamaño del PDF
from reportlab.pdfgen import canvas  # Generador de PDFs (no usado directamente en esta versión)

from services.supabase_service import supabase  # Cliente de conexión a Supabase
from datetime import datetime  # Para obtener fecha y hora actual

def crear_frame_reporte(root):
    """
    Crea un frame de interfaz gráfica para generar reportes en Excel y PDF
    con la información del inventario de productos almacenada en Supabase.
    """
    frame = tk.Frame(root, bg="white")

    # Título del frame
    titulo = tk.Label(frame, text="Descargar Reporte de Inventario", font=("Sans-serif", 32, "bold"), bg="white")
    titulo.pack(pady=60)

    # --- FUNCIÓN: Generar reporte Excel ---
    def generar_excel():
        """
        Consulta la base de datos y genera un archivo Excel (.xlsx) 
        con los datos del inventario.
        """
        try:
            # Consultar datos con relaciones (joins) a unidades y categorías
            response = supabase.table("productos").select(
                "id_producto, nombre, cantidad, precio, unidades(nombre_unidad), categorias(nombre_categoria)"
            ).execute()

            productos = response.data

            # Procesar datos en un formato plano para Excel
            datos_limpios = []
            for p in productos:
                datos_limpios.append({
                    "ID": p["id_producto"],
                    "Nombre": p["nombre"],
                    "Cantidad": p["cantidad"],
                    "Precio": p["precio"],
                    "Unidad": p["unidades"]["nombre_unidad"],
                    "Categoría": p["categorias"]["nombre_categoria"]
                })

            # Crear DataFrame y guardar como archivo Excel
            df = pd.DataFrame(datos_limpios)
            ruta_salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../reporte_inventario.xlsx")
            df.to_excel(ruta_salida, index=False)

            messagebox.showinfo("Éxito", "Reporte Excel generado correctamente en la carpeta del proyecto.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte Excel:\n{str(e)}")

    # Botón para generar Excel
    btn_excel = tk.Button(frame, text="Generar y Guardar Excel", command=generar_excel,
                          font=("Sans-serif", 18, "bold"), bg="#4CAF50", fg="white", height=2)
    btn_excel.pack(pady=30)

    # --- FUNCIÓN: Generar reporte PDF ---
    def generar_pdf():
        """
        Consulta la base de datos y genera un archivo PDF con los datos
        del inventario organizados en una tabla.
        """
        try:
            # Consultar datos con relaciones
            response = supabase.table("productos").select(
                "id_producto, nombre, cantidad, precio, unidades(nombre_unidad), categorias(nombre_categoria)"
            ).execute()

            productos = response.data

            # Cabecera + contenido plano para tabla PDF
            datos_limpios = [
                ["ID", "Nombre", "Cantidad", "Precio (S/.)", "Unidad", "Categoría"]
            ]
            for p in productos:
                datos_limpios.append([
                    p["id_producto"],
                    p["nombre"],
                    p["cantidad"],
                    f"{p['precio']:.2f}",
                    p["unidades"]["nombre_unidad"],
                    p["categorias"]["nombre_categoria"]
                ])

            # Importar herramientas de formateo para PDF
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet

            # Definir nombre y ruta del archivo PDF
            ruta_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../reporte_inventario.pdf")
            doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)

            elementos = []
            styles = getSampleStyleSheet()

            # Título del reporte
            titulo = Paragraph("Reporte de Inventario - Muebles Moderno", styles["Title"])
            elementos.append(titulo)
            elementos.append(Spacer(1, 20))

            # Fecha y hora de generación
            fecha_actual = datetime.now().strftime("%d/%m/%Y a las %H:%M")
            fecha_parrafo = Paragraph(f"Reporte generado el {fecha_actual}", styles["Normal"])
            elementos.append(fecha_parrafo)
            elementos.append(Spacer(1, 20))

            # Construir la tabla con estilos
            tabla = Table(datos_limpios, repeatRows=1)
            tabla.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black)
            ]))

            # Agregar tabla al documento
            elementos.append(tabla)
            doc.build(elementos)

            messagebox.showinfo("Éxito", "PDF generado correctamente en la carpeta del proyecto.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF:\n{str(e)}")

    # Botón para generar PDF
    btn_pdf = tk.Button(frame, text="Generar y Guardar PDF", command=generar_pdf,
                        font=("Sans-serif", 18, "bold"), bg="#607D8B", fg="white", height=2)
    btn_pdf.pack(pady=10)

    return frame
