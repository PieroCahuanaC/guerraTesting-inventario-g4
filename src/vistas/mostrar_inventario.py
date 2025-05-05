import tkinter as tk
from tkinter import ttk, messagebox
from services.supabase_service import supabase
from vistas.editar_producto import abrir_ventana_edicion
from vistas.eliminar_producto import eliminar_producto  

def crear_frame_mostrar(root):
    """
    Crea y retorna un frame que muestra el inventario de productos en un Treeview interactivo.
    Permite editar productos mediante doble clic y eliminar productos seleccionados.

    Parámetros:
    - root: ventana o contenedor padre donde se agregará este frame.

    Retorna:
    - frame: el frame creado.
    - tree: widget Treeview con los productos cargados.
    - recargar_tabla: función que permite recargar los datos del inventario.
    """

    # Frame principal con fondo blanco
    frame = tk.Frame(root, bg="white")

    # Título principal
    tk.Label(frame, text="Inventario de Productos", font=("Sans-serif", 32, "bold"), bg="white").pack(pady=40)

    # Subtítulo con indicación de doble clic
    tk.Label(
        frame,
        text="Haz un doble click sobre un producto para editar",
        font=("Sans-serif", 12, "bold"),
        bg="white"
    ).pack(pady=10)

    # Definición de columnas para el Treeview
    columns = ("ID", "Nombre", "Cantidad", "Precio", "Unidad", "Categoría")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

    # Configurar encabezados y centrado de columnas
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    # Empaquetar la tabla
    tree.pack(pady=20, padx=20, fill="both", expand=True)

    # Scrollbar vertical
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def cargar_datos():
        """
        Carga los productos desde la base de datos Supabase y los muestra en el Treeview.
        """
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

            # Insertar cada producto en la tabla
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

    def recargar_tabla():
        """
        Limpia los datos actuales del Treeview y vuelve a cargar los productos actualizados.
        """
        for row in tree.get_children():
            tree.delete(row)
        cargar_datos()

    def abrir_ventana_emergente(event):
        """
        Abre una ventana de edición al hacer doble clic sobre un producto.

        Parámetro:
        - event: evento del doble clic sobre el Treeview.
        """
        item_id = tree.focus()
        if not item_id:
            return
        valores = tree.item(item_id, "values")
        if valores:
            id_producto = int(valores[0])
            abrir_ventana_edicion(id_producto, frame_padre=frame, recargar_tabla=recargar_tabla)

    # Asociar evento de doble clic al Treeview
    tree.bind("<Double-1>", abrir_ventana_emergente)

    # Botón para eliminar producto seleccionado
    btn_eliminar = tk.Button(
        frame,
        text="Eliminar producto seleccionado",
        command=lambda: eliminar_producto(tree, recargar_tabla),
        font=("Sans-serif", 14, "bold"),
        bg="red",
        fg="white",
        height=2
    )
    btn_eliminar.pack(pady=(5, 20))

    # Cargar los datos iniciales del inventario
    cargar_datos()

    return frame, tree, recargar_tabla
