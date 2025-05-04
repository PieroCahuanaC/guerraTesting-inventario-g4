# src/views/agregar_producto.py
import tkinter as tk
from tkinter import messagebox
from services.supabase_service import supabase

def crear_frame_agregar(root):
    frame = tk.Frame(root, bg="white")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(3, weight=1)

    # Título
    titulo = tk.Label(frame, text="AGREGAR PRODUCTO AL INVENTARIO", font=("Sans-serif", 32, "bold"), bg="white")
    titulo.grid(row=0, column=1, columnspan=2, pady=40)

    # Variables del formulario
    nombre_var = tk.StringVar()
    cantidad_var = tk.StringVar()
    precio_var = tk.StringVar()
    unidad_var = tk.StringVar(value="Selecciona unidad")
    unidades = ["unidad", "juego", "par", "kit", "pieza"]

    # Campo: Nombre del producto
    tk.Label(frame, text="Nombre:", font=("Sans-serif", 16), bg="white").grid(row=1, column=1, sticky="e", pady=5)
    entry_nombre = tk.Entry(frame, textvariable=nombre_var, font=("Sans-serif", 16))
    entry_nombre.grid(row=1, column=2, sticky="w", pady=5)

    # Campo: Cantidad
    tk.Label(frame, text="Cantidad:", font=("Sans-serif", 16), bg="white").grid(row=2, column=1, sticky="e", pady=5)
    entry_cantidad = tk.Entry(frame, textvariable=cantidad_var, font=("Sans-serif", 16))
    entry_cantidad.grid(row=2, column=2, sticky="w", pady=5)

    # Campo: Precio
    tk.Label(frame, text="Precio (S/.):", font=("Sans-serif", 16), bg="white").grid(row=3, column=1, sticky="e", pady=5)
    entry_precio = tk.Entry(frame, textvariable=precio_var, font=("Sans-serif", 16))
    entry_precio.grid(row=3, column=2, sticky="w", pady=5)

    # Campo: Unidad
    tk.Label(frame, text="Unidad:", font=("Sans-serif", 16), bg="white").grid(row=4, column=1, sticky="e", pady=5)
    unidad_menu = tk.OptionMenu(frame, unidad_var, *unidades)
    unidad_menu.config(font=("Sans-serif", 14), bg="white")
    unidad_menu.grid(row=4, column=2, sticky="w", pady=5)

    # Etiqueta para mostrar mensajes temporales
    mensaje_label = tk.Label(frame, text="", font=("Sans-serif", 14), bg="white", fg="green")
    mensaje_label.grid(row=6, column=1, columnspan=2, pady=10)

    # Función para guardar el producto en Supabase
    def guardar_producto():
        nombre = nombre_var.get().strip()
        cantidad = cantidad_var.get().strip()
        precio = precio_var.get().strip()
        unidad = unidad_var.get().strip()

        if not nombre or not cantidad or not precio or unidad == "Selecciona unidad":
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número entero y precio un número decimal.")
            return

        try:
            # Buscar el ID de la unidad en la tabla unidades
            unidad_response = supabase.table("unidades").select("id_unidad").eq("nombre_unidad", unidad).execute()
            if not unidad_response.data:
                raise Exception("Unidad no encontrada en la base de datos.")
            id_unidad = unidad_response.data[0]["id_unidad"]

            # Insertar nuevo producto
            supabase.table("productos").insert({
                "nombre": nombre,
                "cantidad": cantidad,
                "precio": precio,
                "id_unidad": id_unidad,
                "id_categoria": 1 
            }).execute()

            mensaje_label.config(text="Producto agregado exitosamente.", fg="green")
            mensaje_label.after(3000, lambda: mensaje_label.config(text=""))

            # Limpiar los campos
            nombre_var.set("")
            cantidad_var.set("")
            precio_var.set("")
            unidad_var.set("Selecciona unidad")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el producto:\n{str(e)}")

    # Botón de guardar
    btn_guardar = tk.Button(frame, text="Guardar producto", command=guardar_producto,
                            font=("Sans-serif", 16, "bold"), bg="orange", fg="white", height=2)
    btn_guardar.grid(row=5, column=1, columnspan=2, pady=20)

    return frame
