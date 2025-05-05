
import tkinter as tk
from tkinter import messagebox
from services.supabase_service import supabase  # Importar conexión a Supabase

def crear_frame_agregar(root, recargar_tabla=None):
    # Crea frame principal con fondo blanco
    frame = tk.Frame(root, bg="white")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(3, weight=1)

    # Título del formulario
    titulo = tk.Label(frame, text="AGREGAR PRODUCTO AL INVENTARIO", font=("Sans-serif", 32, "bold"), bg="white")
    titulo.grid(row=0, column=1, columnspan=2, pady=40)

    # Variables que almacenarán los valores ingresados por el usuario
    nombre_var = tk.StringVar()
    cantidad_var = tk.StringVar()
    precio_var = tk.StringVar()
    unidad_var = tk.StringVar(value="Selecciona unidad")  # Valor inicial
    categoria_var = tk.StringVar(value="Selecciona categoría")  # Valor inicial

    # Opciones fijas disponibles para unidad y categoría
    unidades = ["unidad", "juego", "par", "kit", "pieza"]
    categorias = ["Sala", "Comedor", "Oficina", "Dormitorio", "Exteriores"]

    # Campos del formulario (Nombre, Cantidad, Precio, Unidad, Categoría)
    tk.Label(frame, text="Nombre:", font=("Sans-serif", 16), bg="white").grid(row=1, column=1, sticky="e", pady=5)
    entry_nombre = tk.Entry(frame, textvariable=nombre_var, font=("Sans-serif", 16))
    entry_nombre.grid(row=1, column=2, sticky="w", pady=5)

    tk.Label(frame, text="Cantidad:", font=("Sans-serif", 16), bg="white").grid(row=2, column=1, sticky="e", pady=5)
    entry_cantidad = tk.Entry(frame, textvariable=cantidad_var, font=("Sans-serif", 16))
    entry_cantidad.grid(row=2, column=2, sticky="w", pady=5)

    tk.Label(frame, text="Precio (S/.):", font=("Sans-serif", 16), bg="white").grid(row=3, column=1, sticky="e", pady=5)
    entry_precio = tk.Entry(frame, textvariable=precio_var, font=("Sans-serif", 16))
    entry_precio.grid(row=3, column=2, sticky="w", pady=5)

    # Menú desplegable de unidades
    tk.Label(frame, text="Unidad:", font=("Sans-serif", 16), bg="white").grid(row=4, column=1, sticky="e", pady=5)
    unidad_menu = tk.OptionMenu(frame, unidad_var, *unidades)
    unidad_menu.config(font=("Sans-serif", 14), bg="white")
    unidad_menu.grid(row=4, column=2, sticky="w", pady=5)

    # Menú desplegable de categorías
    tk.Label(frame, text="Categoría:", font=("Sans-serif", 16), bg="white").grid(row=5, column=1, sticky="e", pady=5)
    categoria_menu = tk.OptionMenu(frame, categoria_var, *categorias)
    categoria_menu.config(font=("Sans-serif", 14), bg="white")
    categoria_menu.grid(row=5, column=2, sticky="w", pady=5)

    # Mensaje para mostrar éxito o error
    mensaje_label = tk.Label(frame, text="", font=("Sans-serif", 14), bg="white", fg="green")
    mensaje_label.grid(row=7, column=1, columnspan=2, pady=10)

    # Función que se ejecuta al hacer clic en "Guardar producto"
    def guardar_producto():
        # Obtene valores del formulario
        nombre = nombre_var.get().strip()
        cantidad = cantidad_var.get().strip()
        precio = precio_var.get().strip()
        unidad = unidad_var.get().strip()
        categoria = categoria_var.get().strip()

        import re  # al inicio del archivo si no está importado

        # Validar que el nombre contenga solo letras, números, espacios, guiones y comas
        if not re.match(r"^[\w\sáéíóúÁÉÍÓÚñÑ.,-]{3,50}$", nombre):
            messagebox.showerror("Error", "El nombre solo debe contener letras, números, espacios, comas o guiones.\nDebe tener entre 3 y 50 caracteres.")
            return

        # Valida que todos los campos estén completos
        if not nombre or not cantidad or not precio or unidad == "Selecciona unidad" or categoria == "Selecciona categoría":
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        # Valida tipos de datos para cantidad y precio
        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número entero y precio un número decimal.")
            return

        try:
            # Obtener ID correspondiente de la unidad desde Supabase
            unidad_response = supabase.table("unidades").select("id_unidad").eq("nombre_unidad", unidad).execute()
            if not unidad_response.data:
                raise Exception("Unidad no encontrada en la base de datos.")
            id_unidad = unidad_response.data[0]["id_unidad"]

            # Obtene ID correspondiente de la categoría desde Supabase
            categoria_response = supabase.table("categorias").select("id_categoria").eq("nombre_categoria", categoria).execute()
            if not categoria_response.data:
                raise Exception("Categoría no encontrada en la base de datos.")
            id_categoria = categoria_response.data[0]["id_categoria"]

            # Verificar si ya existe un producto con el mismo nombre
            nombre_normalizado = nombre.lower()
            respuesta_existente = supabase.table("productos").select("nombre").execute()
            for prod in respuesta_existente.data:
                if prod["nombre"].lower() == nombre_normalizado:
                    messagebox.showwarning("Duplicado", f"Ya existe un producto con el nombre '{prod['nombre']}' (sin distinguir mayúsculas).")
                    return

            # Inserta producto en la tabla productos
            supabase.table("productos").insert({
                "nombre": nombre,
                "cantidad": cantidad,
                "precio": precio,
                "id_unidad": id_unidad,
                "id_categoria": id_categoria
            }).execute()

            # Mostrar mensaje de éxito
            mensaje_label.config(text="Producto agregado exitosamente.", fg="green")
            mensaje_label.after(3000, lambda: mensaje_label.config(text=""))

            # Limpiar campos luego de guardar
            nombre_var.set("")
            cantidad_var.set("")
            precio_var.set("")
            unidad_var.set("Selecciona unidad")
            categoria_var.set("Selecciona categoría")
        
        
            if recargar_tabla:
                recargar_tabla()  # ACTUALIZA la tabla al instante

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el producto:\n{str(e)}")


    # Botón que llama a la función guardar_producto()
    btn_guardar = tk.Button(frame, text="Guardar producto", command=guardar_producto,
                            font=("Sans-serif", 16, "bold"), bg="orange", fg="white", height=2)
    btn_guardar.grid(row=6, column=1, columnspan=2, pady=20)

    return frame
