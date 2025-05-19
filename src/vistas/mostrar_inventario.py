import tkinter as tk
from tkinter import ttk, messagebox
from services.supabase_service import supabase
from vistas.editar_producto import abrir_ventana_edicion
from vistas.eliminar_producto import eliminar_producto
import os
from PIL import Image, ImageTk



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

    # Frame para barra de búsqueda
    busqueda_frame = tk.Frame(frame, bg="white")
    busqueda_frame.pack(pady=(0, 10))

    # Placeholder para entrada de texto
    entry_busqueda = tk.Entry(busqueda_frame, font=("Sans-serif", 14), width=40, fg="gray")
    entry_busqueda.insert(0, "Ingrese el nombre del producto")
    entry_busqueda.grid(row=0, column=0, padx=(10, 5), pady=5)

    def on_entry_click(event):
        if entry_busqueda.get() == "Ingrese el nombre del producto":
            entry_busqueda.delete(0, "end")
            entry_busqueda.config(fg="black")

    def on_focusout(event):
        if entry_busqueda.get() == "":
            entry_busqueda.insert(0, "Ingrese el nombre del producto")
            entry_busqueda.config(fg="gray")

    entry_busqueda.bind('<FocusIn>', on_entry_click)
    entry_busqueda.bind('<FocusOut>', on_focusout)

    # Botón lupa
    ruta_directorio = os.path.dirname(os.path.abspath(__file__))
    ruta_lupa = os.path.join(ruta_directorio, '../../assets/lupa.png')
    if os.path.exists(ruta_lupa):
        lupa_image = Image.open(ruta_lupa).resize((30, 30), Image.LANCZOS)
        lupa_photo = ImageTk.PhotoImage(lupa_image)
        boton_buscar = tk.Button(
            busqueda_frame,
            image=lupa_photo,
            bg="white",
            command=lambda: buscar_producto(entry_busqueda.get()),
            borderwidth=0
        )
        boton_buscar.image = lupa_photo
        boton_buscar.grid(row=0, column=1, padx=(0, 10))

    # Casilla: Buscar por categoría
    var_categoria = tk.BooleanVar()
    chk_categoria = tk.Checkbutton(busqueda_frame, text="Buscar por Categoría", variable=var_categoria, bg="white",
                                   command=lambda: mostrar_opciones_categoria())
    chk_categoria.grid(row=0, column=2, padx=10)

    combo_categoria = ttk.Combobox(busqueda_frame, state="readonly", values=["Sala", "Comedor", "Oficina", "Dormitorio", "Exteriores"])
    combo_categoria.grid(row=0, column=3, padx=5)
    combo_categoria.grid_remove()

    # Casilla: Buscar por precio
    var_precio = tk.BooleanVar()
    chk_precio = tk.Checkbutton(busqueda_frame, text="Buscar por Precio", variable=var_precio, bg="white",
                                command=lambda: mostrar_opciones_precio())
    chk_precio.grid(row=0, column=4, padx=10)

    combo_precio = ttk.Combobox(busqueda_frame, state="readonly", values=["Más barato a más caro", "Más caro a más barato"])
    combo_precio.grid(row=0, column=5, padx=5)
    combo_precio.grid_remove()

    def mostrar_opciones_categoria():
        if var_categoria.get():
            combo_categoria.grid()
            if combo_categoria.get():
                buscar_producto(entry_busqueda.get())
        else:
            combo_categoria.set("")
            combo_categoria.grid_remove()
            buscar_producto(entry_busqueda.get())

    def mostrar_opciones_precio():
        if var_precio.get():
            combo_precio.grid()
            if combo_precio.get():
                buscar_producto(entry_busqueda.get())
        else:
            combo_precio.set("")
            combo_precio.grid_remove()
            buscar_producto(entry_busqueda.get())

    combo_categoria.bind("<<ComboboxSelected>>", lambda e: buscar_producto(entry_busqueda.get()))
    combo_precio.bind("<<ComboboxSelected>>", lambda e: buscar_producto(entry_busqueda.get()))

    # Definición de columnas para el Treeview
    columns = ("ID", "Nombre", "Cantidad", "Precio (S/.)", "Unidad", "Categoría")
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

    def buscar_producto(termino):
        """
        Filtra los productos según el texto ingresado, categoría y orden de precio.
        """
        for row in tree.get_children():
            tree.delete(row)

        try:
            termino_busqueda = termino.strip().lower()
            response = supabase.from_("productos").select("""
                id_producto,
                nombre,
                cantidad,
                precio,
                unidades(nombre_unidad),
                categorias(nombre_categoria)
            """).execute()
            productos = response.data

            # Filtro por nombre si no está vacío
            if termino_busqueda and termino != "Ingrese el nombre del producto":
                productos = [p for p in productos if termino_busqueda in p['nombre'].lower()]

            # Filtro por categoría
            if var_categoria.get() and combo_categoria.get():
                productos = [p for p in productos if p['categorias']['nombre_categoria'] == combo_categoria.get()]

            # Filtro por precio
            if var_precio.get() and combo_precio.get():
                reverse = combo_precio.get() == "Más caro a más barato"
                productos = sorted(productos, key=lambda x: x['precio'], reverse=reverse)

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
            print("Error al buscar productos:", str(e))

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
