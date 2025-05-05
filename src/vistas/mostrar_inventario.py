import tkinter as tk
from tkinter import ttk
from services.supabase_service import supabase

from vistas.editar_producto import abrir_ventana_edicion

# Función principal que construye y retorna el frame para mostrar el inventario
def crear_frame_mostrar(root):
    # Crea frame con fondo blanco
    frame = tk.Frame(root, bg="white")

    # Título del frame
    titulo = tk.Label(frame, text="Inventario de Productos", font=("Sans-serif", 32, "bold"), bg="white")
    titulo.pack(pady=40)

    # Indicaciones de doble click
    titulo = tk.Label(frame, text="Haz un doble click sobre un producto para editar", font=("Sans-serif", 12, "bold"), bg="white")
    titulo.pack(pady=10)

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

    # Función para recargar la tabla
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

    # Función para cargar los productos desde Supabase y mostrarlos en la tabla
    def cargar_datos():
        try:
            # Consulta a la tabla 'productos', incluyendo campos anidados de las relaciones
            response = supabase.from_("productos").select("""
                id_producto,
                nombre,
                cantidad,
                precio,
                unidades(nombre_unidad),
                categorias(nombre_categoria)
            """).order("id_producto", desc=False).execute()

            productos = response.data  # Lista de productos obtenidos

            # Recorrer cada producto y agregarlo como fila a la tabla
            for producto in productos:
                tree.insert("", "end", values=(
                    producto['id_producto'],                     # ID del producto
                    producto['nombre'],                          # Nombre del producto
                    producto['cantidad'],                        # Cantidad disponible
                    producto['precio'],                          # Precio unitario
                    producto['unidades']['nombre_unidad'],       # Unidad (relación con tabla 'unidades')
                    producto['categorias']['nombre_categoria']   # Categoría (relación con tabla 'categorias')
                ))
        except Exception as e:
            # En caso de error durante la carga de datos, imprimir el error
            print("Error al cargar productos:", str(e))

    # Llama a la función de carga al iniciar el frame
    cargar_datos()

    # Devuelve el frame creado para ser usado en la interfaz principal
    return frame, tree, cargar_datos
