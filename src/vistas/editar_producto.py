# src/views/editar_producto.py

import tkinter as tk
from tkinter import messagebox
from services.supabase_service import supabase
import re
import unicodedata

def normalizar_nombre(nombre):
    """
    Normaliza el nombre para evitar duplicados: minúsculas, sin tildes, sin signos y espacios simples.
    """
    nombre = nombre.strip().lower()
    nombre = unicodedata.normalize('NFD', nombre)
    nombre = nombre.encode('ascii', 'ignore').decode('utf-8')  # elimina tildes
    nombre = re.sub(r'[^\w\s]', '', nombre)  # elimina signos
    nombre = re.sub(r'\s+', ' ', nombre)
    return nombre

def limpiar_espacios(nombre):
    """
    Elimina múltiples espacios y los reemplaza por uno solo.
    """
    nombre = nombre.strip()
    nombre = re.sub(r'\s+', ' ', nombre)
    return nombre

def formatear_nombre(nombre):
    """
    Aplica formato visual estándar: primera letra de cada palabra en mayúscula.
    """
    nombre = limpiar_espacios(nombre)
    return nombre.title()

# Variable global para evitar múltiples ventanas de edición simultáneas
ventana_edicion_activa = False

def abrir_ventana_edicion(id_producto, frame_padre=None, recargar_tabla=None):
    """
    Abre una ventana emergente (modal) para editar los datos de un producto existente.
    
    Parámetros:
    - id_producto: ID del producto a editar.
    - frame_padre: Frame que contiene la vista del inventario. Se puede usar para refrescar visualmente.
    - recargar_tabla: Función opcional que se ejecuta para volver a cargar los datos del inventario en pantalla.
    """
    global ventana_edicion_activa

    # Para que solo se pueda escribir 2 decimales máximo
    def validar_precio_entrada(texto):
        import re
        # Permitir solo números con máximo 2 decimales
        return re.fullmatch(r"^\d{0,9}(\.\d{0,2})?$", texto) is not None

    # Evita que se abran múltiples ventanas de edición
    if ventana_edicion_activa:
        messagebox.showinfo("Aviso", "Ya hay una ventana de edición abierta.")
        return

    # Obtener datos del producto desde Supabase
    try:
        response = supabase.table("productos").select("""
            *,
            unidades(id_unidad,nombre_unidad),
            categorias(id_categoria,nombre_categoria)
        """).eq("id_producto", id_producto).single().execute()
        producto = response.data
        if not producto:
            messagebox.showerror("Error", "No se encontró el producto.")
            return
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener el producto:\n{str(e)}")
        return

    # Obtener opciones de unidades y categorías desde Supabase
    try:
        unidades = supabase.table("unidades").select("*").execute().data
        categorias = supabase.table("categorias").select("*").execute().data
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener unidades o categorías:\n{str(e)}")
        return

    # Crear ventana modal
    ventana = tk.Toplevel()
    ventana.title(f"Editar Producto: {producto['nombre']}")
    ventana.geometry("400x500")
    ventana.configure(bg="white")
    ventana.grab_set()  # Hace la ventana modal
    ventana_edicion_activa = True

    # Al cerrar la ventana, se libera el control
    def on_close():
        global ventana_edicion_activa
        ventana_edicion_activa = False
        ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", on_close)

    # Variables para los campos editables
    nombre_var = tk.StringVar(value=producto['nombre'])
    cantidad_var = tk.StringVar(value=str(producto['cantidad']))
    precio_var = tk.StringVar(value=str(producto['precio']))
    unidad_var = tk.StringVar(value=producto['unidades']['nombre_unidad'])
    categoria_var = tk.StringVar(value=producto['categorias']['nombre_categoria'])

    # Título
    tk.Label(ventana, text="Editar Producto", font=("Sans-serif", 20, "bold"), bg="white").pack(pady=20)

    # Campos de texto
    # Campo: Nombre
    tk.Label(ventana, text="Nombre:", font=("Sans-serif", 14), bg="white").pack()
    tk.Entry(ventana, textvariable=nombre_var, font=("Sans-serif", 14)).pack(pady=5)

    # Campo: Cantidad
    tk.Label(ventana, text="Cantidad:", font=("Sans-serif", 14), bg="white").pack()
    tk.Entry(ventana, textvariable=cantidad_var, font=("Sans-serif", 14)).pack(pady=5)

    # Campo: Precio con validación de máximo 2 decimales
    tk.Label(ventana, text="Precio:", font=("Sans-serif", 14), bg="white").pack()
    vcmd = ventana.register(validar_precio_entrada)
    entry_precio = tk.Entry(
        ventana,
        textvariable=precio_var,
        font=("Sans-serif", 14),
        validate="key",
        validatecommand=(vcmd, "%P")
    )
    entry_precio.pack(pady=5)

    # Menú desplegable para unidad
    tk.Label(ventana, text="Unidad:", font=("Sans-serif", 14), bg="white").pack()
    opciones_unidades = [u["nombre_unidad"] for u in unidades]
    tk.OptionMenu(ventana, unidad_var, *opciones_unidades).pack(pady=5)

    # Menú desplegable para categoría
    tk.Label(ventana, text="Categoría:", font=("Sans-serif", 14), bg="white").pack()
    opciones_categorias = [c["nombre_categoria"] for c in categorias]
    tk.OptionMenu(ventana, categoria_var, *opciones_categorias).pack(pady=5)

    # Función para guardar los cambios en la base de datos
    def guardar_cambios():
        try:
            nombre_original = nombre_var.get()
            nuevo_nombre = formatear_nombre(nombre_original)  # Visual limpio
            nombre_normalizado = normalizar_nombre(nombre_original)  # Para validación

            cantidad_str = cantidad_var.get().strip()
            precio_str = precio_var.get().strip()
            nueva_unidad = unidad_var.get().strip()
            nueva_categoria = categoria_var.get().strip()

            # Validar que el nombre comience con mínimo 3 letras y luego números o signos opcionalmente
            if not re.fullmatch(r"[A-Za-záéíóúÁÉÍÓÚñÑ]{3,}[A-Za-z0-9\s.,-]*", nuevo_nombre):
                messagebox.showerror("Error", "El nombre debe comenzar con al menos 3 letras antes de incluir números o signos.")
                return

            # Validar longitud mínima
            if len(nuevo_nombre) < 3:
                messagebox.showerror("Error", "El nombre debe tener al menos 3 caracteres.")
                return

            # Validar longitud máxima
            if len(nuevo_nombre) > 50:
                messagebox.showerror("Error", "El nombre no puede tener más de 50 caracteres.")
                return

            # Validar campos vacíos
            if not nuevo_nombre or not cantidad_str or not precio_str:
                messagebox.showerror("Error", "Todos los campos deben estar completos.")
                return

            # Validar que cantidad y precio sean números válidos
            if not cantidad_str.isdigit() or int(cantidad_str) <= 0:
                messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
                return

            try:
                nuevo_precio = float(precio_str)
                if nuevo_precio <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número decimal positivo.")
                return

            nueva_cantidad = int(cantidad_str)

            # Validación básica
            if not nuevo_nombre:
                raise ValueError("El nombre no puede estar vacío.")

            # Validar que no exista otro producto con el mismo nombre (normalizado)
            respuesta_existente = supabase.table("productos").select("id_producto", "nombre").execute()
            for prod in respuesta_existente.data:
                if normalizar_nombre(prod["nombre"]) == nombre_normalizado and prod["id_producto"] != producto["id_producto"]:
                    messagebox.showwarning("Duplicado", f"Ya existe otro producto con un nombre similar: '{prod['nombre']}'")
                    return

            # Buscar IDs de unidad y categoría seleccionadas
            id_unidad = next(u["id_unidad"] for u in unidades if u["nombre_unidad"] == nueva_unidad)
            id_categoria = next(c["id_categoria"] for c in categorias if c["nombre_categoria"] == nueva_categoria)

            # Actualizar el producto en Supabase
            supabase.table("productos").update({
                "nombre": nuevo_nombre,
                "cantidad": nueva_cantidad,
                "precio": nuevo_precio,
                "id_unidad": id_unidad,
                "id_categoria": id_categoria
            }).eq("id_producto", producto['id_producto']).execute()

            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            if recargar_tabla:
                recargar_tabla()  # Refrescar la tabla sin redibujar el frame
            on_close()

        except Exception as e:
            mensaje_error = str(e).lower()
            if ("failed to establish a new connection" in mensaje_error or 
                "name or service not known" in mensaje_error or
                "getaddrinfo failed" in mensaje_error):
                messagebox.showerror("Error de conexión", "No se pudo actualizar el producto porque no hay conexión a internet.\nVerifica tu red e inténtalo nuevamente.")
            else:
                messagebox.showerror("Error inesperado", f"No se pudo actualizar el producto:\n{str(e)}")


    # Botón para guardar cambios
    tk.Button(
        ventana, text="Guardar Cambios", command=guardar_cambios,
        font=("Sans-serif", 14, "bold"), bg="green", fg="white"
    ).pack(pady=20)

    # Espera hasta que la ventana se cierre (bloquea la ejecución)
    ventana.wait_window()
