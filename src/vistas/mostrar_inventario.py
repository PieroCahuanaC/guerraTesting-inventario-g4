
import tkinter as tk
from tkinter import ttk
from services.supabase_service import supabase



# Crear el frame para mostrar inventario
def crear_frame_mostrar(root):
    frame = tk.Frame(root, bg="white")

    # Título
    titulo = tk.Label(frame, text="Inventario de Productos", font=("Sans-serif", 32, "bold"), bg="white")
    titulo.pack(pady=40)

    # Tabla (Treeview)
    columns = ("ID", "Nombre", "Cantidad", "Precio", "Unidad")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(pady=20, padx=20, fill="both", expand=True)

    # Scroll vertical
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Obtener datos desde Supabase y llenar la tabla
    
    def cargar_datos():
        try:
            response = supabase.from_("productos").select("""
                id_producto,
                nombre,
                cantidad,
                precio,
                unidades(nombre_unidad)
            """).execute()
            productos = response.data
            for producto in productos:
                tree.insert("", "end", values=(
                    producto['id_producto'],
                    producto['nombre'],
                    producto['cantidad'],
                    producto['precio'],
                    producto['unidades']['nombre_unidad']  
                ))
        except Exception as e:
            print("Error al cargar productos:", str(e))

    cargar_datos()
    return frame
