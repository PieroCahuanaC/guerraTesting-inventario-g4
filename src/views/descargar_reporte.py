# src/views/descargar_reporte.py
import tkinter as tk

def crear_frame_reporte(root):
    frame = tk.Frame(root, bg="white")

    titulo = tk.Label(frame, text="DESCARGAR REPORTE DE INVENTARIO", font=("Sans-serif", 30, "bold"), bg="white")
    titulo.pack(pady=50)

    return frame