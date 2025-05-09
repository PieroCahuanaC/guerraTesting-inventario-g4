import tkinter as tk
from tkinter import messagebox
from services.supabase_service import supabase  # Conexión a la base de datos Supabase
import re  # Para validación del nombre del producto

def crear_frame_agregar(root, recargar_tabla=None):
    """
    Crea y retorna el frame que permite agregar nuevos productos al inventario.

    Parámetros:
    - root: ventana principal donde se agregará el frame.
    - recargar_tabla (opcional): función para actualizar la vista de inventario tras agregar un producto.

    Retorna:
    - Frame con todos los widgets necesarios para el formulario.
    """
    
    # Crear el frame principal y configurar su diseño
    frame = tk.Frame(root, bg="white")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(3, weight=1)

    # Título del formulario
    titulo = tk.Label(frame, text="AGREGAR PRODUCTO AL INVENTARIO", font=("Sans-serif", 32, "bold"), bg="white")
    titulo.grid(row=0, column=1, columnspan=2, pady=40)

    # Variables para capturar los datos del formulario
    nombre_var = tk.StringVar()
    cantidad_var = tk.StringVar()
    precio_var = tk.StringVar()
    unidad_var = tk.StringVar(value="Selecciona unidad")      # Valor por defecto
    categoria_var = tk.StringVar(value="Selecciona categoría")  # Valor por defecto

    # Opciones disponibles para los campos desplegables
    unidades = ["unidad", "juego", "par", "kit", "pieza"]
    categorias = ["Sala", "Comedor", "Oficina", "Dormitorio", "Exteriores"]

    # Campos de entrada (labels + inputs)
    tk.Label(frame, text="Nombre:", font=("Sans-serif", 16), bg="white").grid(row=1, column=1, sticky="e", pady=5)
    tk.Entry(frame, textvariable=nombre_var, font=("Sans-serif", 16)).grid(row=1, column=2, sticky="w", pady=5)

    tk.Label(frame, text="Cantidad:", font=("Sans-serif", 16), bg="white").grid(row=2, column=1, sticky="e", pady=5)
    tk.Entry(frame, textvariable=cantidad_var, font=("Sans-serif", 16)).grid(row=2, column=2, sticky="w", pady=5)

    tk.Label(frame, text="Precio (S/.):", font=("Sans-serif", 16), bg="white").grid(row=3, column=1, sticky="e", pady=5)
    tk.Entry(frame, textvariable=precio_var, font=("Sans-serif", 16)).grid(row=3, column=2, sticky="w", pady=5)

    # Menú desplegable: Unidad
    tk.Label(frame, text="Unidad:", font=("Sans-serif", 16), bg="white").grid(row=4, column=1, sticky="e", pady=5)
    tk.OptionMenu(frame, unidad_var, *unidades).grid(row=4, column=2, sticky="w", pady=5)

    # Menú desplegable: Categoría
    tk.Label(frame, text="Categoría:", font=("Sans-serif", 16), bg="white").grid(row=5, column=1, sticky="e", pady=5)
    tk.OptionMenu(frame, categoria_var, *categorias).grid(row=5, column=2, sticky="w", pady=5)

    # Label que muestra mensajes de éxito o error
    mensaje_label = tk.Label(frame, text="", font=("Sans-serif", 14), bg="white", fg="green")
    mensaje_label.grid(row=7, column=1, columnspan=2, pady=10)

    # -----------------------------------------------
    # FUNCIÓN PRINCIPAL: Guardar el producto
    # -----------------------------------------------
    def guardar_producto():
        """
        Valida e inserta un nuevo producto en la base de datos Supabase.
        """
        # Obtener valores del formulario
        nombre = nombre_var.get().strip()
        cantidad = cantidad_var.get().strip()
        precio = precio_var.get().strip()
        unidad = unidad_var.get().strip()
        categoria = categoria_var.get().strip()

        # Validación del nombre con expresión regular
        if not re.match(r"^[\w\sáéíóúÁÉÍÓÚñÑ.,-]{3,50}$", nombre):
            messagebox.showerror("Error", "El nombre solo debe contener letras, números, espacios, comas o guiones.\nDebe tener entre 3 y 50 caracteres.")
            return

        # Validar que todos los campos estén completos
        if not nombre or not cantidad or not precio or unidad == "Selecciona unidad" or categoria == "Selecciona categoría":
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        # Validar tipos de datos
        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número entero y precio un número decimal.")
            return

        try:
            # Buscar ID de unidad desde Supabase
            unidad_response = supabase.table("unidades").select("id_unidad").eq("nombre_unidad", unidad).execute()
            if not unidad_response.data:
                raise Exception("Unidad no encontrada en la base de datos.")
            id_unidad = unidad_response.data[0]["id_unidad"]

            # Buscar ID de categoría desde Supabase
            categoria_response = supabase.table("categorias").select("id_categoria").eq("nombre_categoria", categoria).execute()
            if not categoria_response.data:
                raise Exception("Categoría no encontrada en la base de datos.")
            id_categoria = categoria_response.data[0]["id_categoria"]

            # Validación de nombre duplicado (insensible a mayúsculas)
            nombre_normalizado = nombre.lower()
            respuesta_existente = supabase.table("productos").select("nombre").execute()
            for prod in respuesta_existente.data:
                if prod["nombre"].lower() == nombre_normalizado:
                    messagebox.showwarning("Duplicado", f"Ya existe un producto con el nombre '{prod['nombre']}' (sin distinguir mayúsculas).")
                    return

            # Inserción del producto
            supabase.table("productos").insert({
                "nombre": nombre,
                "cantidad": cantidad,
                "precio": precio,
                "id_unidad": id_unidad,
                "id_categoria": id_categoria
            }).execute()

            # Éxito: mostrar mensaje y limpiar campos
            mensaje_label.config(text="Producto agregado exitosamente.", fg="green")
            mensaje_label.after(3000, lambda: mensaje_label.config(text=""))

            nombre_var.set("")
            cantidad_var.set("")
            precio_var.set("")
            unidad_var.set("Selecciona unidad")
            categoria_var.set("Selecciona categoría")

            # Recarga tabla en vista principal si se ha enviado función
            if recargar_tabla:
                recargar_tabla()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el producto:\n{str(e)}")

    # Botón para guardar el producto
    btn_guardar = tk.Button(frame, text="Guardar producto", command=guardar_producto,
                            font=("Sans-serif", 16, "bold"), bg="orange", fg="white", height=2)
    btn_guardar.grid(row=6, column=1, columnspan=2, pady=20)

    return frame
