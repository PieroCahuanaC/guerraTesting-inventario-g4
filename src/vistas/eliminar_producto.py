from tkinter import messagebox
from services.supabase_service import supabase

def eliminar_producto(tree, recargar_tabla):
    """
    Elimina un producto seleccionado de la tabla 'productos' en Supabase.

    Parámetros:
    - tree: widget ttk.Treeview que muestra el inventario de productos.
    - recargar_tabla: función que recarga los datos del Treeview después de eliminar.

    Proceso:
    1. Verifica que un producto esté seleccionado.
    2. Solicita confirmación al usuario.
    3. Elimina el producto por su ID desde la base de datos Supabase.
    4. Muestra mensajes de éxito o error, y actualiza la tabla visual.
    """
    
    # Obtener el ID del elemento seleccionado en la tabla
    item_id = tree.focus()
    if not item_id:
        messagebox.showwarning("Advertencia", "Selecciona un producto para eliminar.")
        return

    # Obtener el contenido del item seleccionado
    item = tree.item(item_id)
    valores = item.get("values")

    # Validar que existan datos en la fila seleccionada
    if not valores or len(valores) < 2:
        messagebox.showwarning("Advertencia", "No se pudo obtener el producto seleccionado.")
        return

    # Extraer ID y nombre del producto
    id_producto = int(valores[0])
    nombre = valores[1]

    # Mostrar mensaje de confirmación
    confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de que deseas eliminar '{nombre}'?")
    if not confirmacion:
        return

    # Intentar eliminar el producto en Supabase
    try:
        supabase.table("productos").delete().eq("id_producto", id_producto).execute()
        messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        recargar_tabla()  # Refrescar visualmente la tabla
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el producto:\n{str(e)}")
