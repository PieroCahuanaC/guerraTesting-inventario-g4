# src/views/editar_producto.py

import tkinter as tk
from tkinter import messagebox
from services.supabase_service import supabase

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
    for label, var in [("Nombre:", nombre_var), ("Cantidad:", cantidad_var), ("Precio:", precio_var)]:
        tk.Label(ventana, text=label, font=("Sans-serif", 14), bg="white").pack()
        tk.Entry(ventana, textvariable=var, font=("Sans-serif", 14)).pack(pady=5)

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
            nuevo_nombre = nombre_var.get().strip()
            nueva_cantidad = int(cantidad_var.get().strip())
            nuevo_precio = float(precio_var.get().strip())
            nueva_unidad = unidad_var.get().strip()
            nueva_categoria = categoria_var.get().strip()

            # Validación básica
            if not nuevo_nombre:
                raise ValueError("El nombre no puede estar vacío.")

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
            messagebox.showerror("Error", f"No se pudo actualizar el producto:\n{str(e)}")

    # Botón para guardar cambios
    tk.Button(
        ventana, text="Guardar Cambios", command=guardar_cambios,
        font=("Sans-serif", 14, "bold"), bg="green", fg="white"
    ).pack(pady=20)

    # Espera hasta que la ventana se cierre (bloquea la ejecución)
    ventana.wait_window()
