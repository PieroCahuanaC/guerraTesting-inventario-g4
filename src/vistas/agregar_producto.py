# src/views/agregar_producto.py
import tkinter as tk

def crear_frame_agregar(root):
    frame = tk.Frame(root, bg="white")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(3, weight=1)

    # Título
    titulo = tk.Label(frame, text="AGREGAR PRODUCTO AL INVENTARIO", font=("Sans-serif", 32, "bold"), bg="white")
    titulo.grid(row=0, column=1, columnspan=2, pady=40)

    # Variables
    nombre_var = tk.StringVar()
    cantidad_var = tk.StringVar()
    precio_var = tk.StringVar()
    unidad_var = tk.StringVar(value="Selecciona unidad")
    unidades = ["unidad", "juego", "par", "kit", "pieza"]

    # Campos de entrada
    tk.Label(frame, text="Nombre:", font=("Sans-serif", 16), bg="white").grid(row=1, column=1, sticky="e", pady=5)
    entry_nombre = tk.Entry(frame, textvariable=nombre_var, font=("Sans-serif", 16))
    entry_nombre.grid(row=1, column=2, sticky="w", pady=5)

    tk.Label(frame, text="Cantidad:", font=("Sans-serif", 16), bg="white").grid(row=2, column=1, sticky="e", pady=5)
    entry_cantidad = tk.Entry(frame, textvariable=cantidad_var, font=("Sans-serif", 16))
    entry_cantidad.grid(row=2, column=2, sticky="w", pady=5)

    tk.Label(frame, text="Precio:", font=("Sans-serif", 16), bg="white").grid(row=3, column=1, sticky="e", pady=5)
    entry_precio = tk.Entry(frame, textvariable=precio_var, font=("Sans-serif", 16))
    entry_precio.grid(row=3, column=2, sticky="w", pady=5)

    tk.Label(frame, text="Unidad:", font=("Sans-serif", 16), bg="white").grid(row=4, column=1, sticky="e", pady=5)
    unidad_menu = tk.OptionMenu(frame, unidad_var, *unidades)
    unidad_menu.config(font=("Sans-serif", 14), bg="white")
    unidad_menu.grid(row=4, column=2, sticky="w", pady=5)

    # Mensaje temporal
    mensaje_label = tk.Label(frame, text="", font=("Sans-serif", 14), bg="white", fg="green")
    mensaje_label.grid(row=6, column=1, columnspan=2, pady=10)

    # Botón guardar 
    def guardar_producto():
        mensaje_label.config(text="Producto agregado exitosamente.")
        mensaje_label.after(3000, lambda: mensaje_label.config(text=""))

    btn_guardar = tk.Button(frame, text="Guardar producto", command=guardar_producto,
                            font=("Sans-serif", 16, "bold"), bg="orange", fg="white", height=2)
    btn_guardar.grid(row=5, column=1, columnspan=2, pady=20)

    return frame
