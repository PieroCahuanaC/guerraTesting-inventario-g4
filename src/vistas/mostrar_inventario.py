import tkinter as tk
from services.supabase_service import supabase
from vistas.editar_producto import abrir_ventana_edicion
from tkinter import messagebox
from tkinter import ttk

# Función principal que construye y retorna el frame para mostrar el inventario
def crear_frame_mostrar(root):
    # Crea frame con fondo blanco
    frame = tk.Frame(root, bg="white")

    # Título del frame
    tk.Label(frame, text="Inventario de Productos", font=("Sans-serif", 32, "bold"), bg="white").pack(pady=40)

    # Indicaciones de doble click
    tk.Label(frame, text="Haz un doble click sobre un producto para editar", font=("Sans-serif", 12, "bold"), bg="white").pack(pady=10)

    # Definición de columnas para la tabla que se mostrará
    columns = ("ID", "Nombre", "Cantidad", "Precio", "Unidad", "Categoría")

    # Crear widget Treeview para mostrar los datos en forma de tabla
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

    # Configurar encabezados de columna
    for col in columns:
        tree.heading(col, text=col)        # Título visible en cada columna
        tree.column(col, anchor="center")  # Centrar el contenido de cada celda

    # Mostrar la tabla con márgenes
    tree.pack(pady=20, padx=20, fill="both", expand=True)

    # Scrollbar vertical para la tabla
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Función para cargar los productos desde Supabase y mostrarlos en la tabla
    def cargar_datos():
        try:
            response = supabase.from_("productos").select("""
                id_producto,
                nombre,
                cantidad,
                precio,
                unidades(nombre_unidad),
                categorias(nombre_categoria)
            """).order("id_producto", desc=False).execute()

            productos = response.data

            for producto in productos:
                tree.insert("", "end", values=(
                    producto['id_producto'],
                    producto['nombre'],
                    producto['cantidad'],
                    producto['precio'],
                    producto['unidades']['nombre_unidad'],
                    producto['categorias']['nombre_categoria']
                ))
        except Exception as e:
            print("Error al cargar productos:", str(e))

    # Función para recargar limpiando la tabla primero
    def recargar_tabla():
        for row in tree.get_children():
            tree.delete(row)
        cargar_datos()

    # Evento doble clic para editar producto
    def abrir_ventana_emergente(event):
        item_id = tree.focus()
        if not item_id:
            return
        valores = tree.item(item_id, "values")
        if valores:
            id_producto = int(valores[0])
            abrir_ventana_edicion(id_producto, frame_padre=frame, recargar_tabla=recargar_tabla)

    tree.bind("<Double-1>", abrir_ventana_emergente)

    #Funcionalidad de eliminar productos
    def eliminar_producto():
        # Obtener el ID del ítem seleccionado en la tabla
        item_id = tree.focus()
        if not item_id:
            messagebox.showwarning("Advertencia", "Selecciona un producto para eliminar.")
            return
        # Obtener los valores del producto seleccionado
        valores = tree.item(item_id, "values")
        if not valores:
            return

         # Extraer el ID y nombre del producto desde la fila seleccionada
        id_producto = int(valores[0])
        nombre = valores[1]

        # Mostrar cuadro de confirmación antes de eliminar
        confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de que deseas eliminar '{nombre}'?")
        if not confirmacion:
            return

        try:
            # Ejecutar eliminación en la tabla 'productos' de Supabase
            supabase.table("productos").delete().eq("id_producto", id_producto).execute()
            
             # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            
             # Refrescar tabla para reflejar el cambio
            recargar_tabla()
        except Exception as e:
            # Mostrar mensaje de error en caso de fallo
            messagebox.showerror("Error", f"No se pudo eliminar el producto:\n{str(e)}")

    # Botón fuera de la función eliminar_producto
    btn_eliminar = tk.Button(frame, text="Eliminar producto seleccionado", command=eliminar_producto,
                             font=("Sans-serif", 14, "bold"), bg="red", fg="white", height=2)
    btn_eliminar.pack(pady=(5, 20))
    
    cargar_datos()
    
    return frame, tree, recargar_tabla