# src/views/mostrar_inventario.py
import tkinter as tk

def crear_frame_mostrar(root):
    frame = tk.Frame(root, bg="white")

    titulo = tk.Label(frame, text="MOSTRAR Y EDITAR INVENTARIO", font=("Sans-serif", 30, "bold"), bg="white")
    titulo.pack(pady=50)

    return frame
