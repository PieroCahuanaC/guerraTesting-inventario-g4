import tkinter as tk
from PIL import Image, ImageTk
import os

from vistas.agregar_producto import crear_frame_agregar
from vistas.mostrar_inventario import crear_frame_mostrar
from vistas.descargar_reporte import crear_frame_reporte



# Ventaja principal
root = tk.Tk()
root.title("Menú Principal - Muebles Moderno")
root.geometry("800x800")
root.state("zoomed")  # Maximiza la ventana

# Frame del menú principal
frame_menu = tk.Frame(root, bg="white")
frame_menu.pack(fill="both", expand=True)

# Titulo
titulo = tk.Label(frame_menu, text="MUEBLES MODERNO - INVENTARIO", bg="white", font=("Sans-serif", 40, "bold"))
titulo.pack(pady=60)

# Logo
ruta_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets/logo.png')
if os.path.exists(ruta_logo):
    logo_img = Image.open(ruta_logo).resize((180, 180), Image.LANCZOS)
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(frame_menu, image=logo, bg="white")
    logo_label.pack(pady=10)
else:
    print("Logo no encontrado en la ruta especificada.")



# Botones--------------------------------------
# Frame para los botones
botones_frame = tk.Frame(frame_menu, bg="white")
botones_frame.pack(pady=15)

# Se crean frames para cada vista
frame_agregar = crear_frame_agregar(root)

frame_mostrar = crear_frame_mostrar(root)
frame_reporte = crear_frame_reporte(root)


# Se crean funciones para cambiar de vista
def mostrar_frame_agregar():
    frame_menu.pack_forget()
    frame_mostrar.pack_forget()
    frame_reporte.pack_forget()
    frame_agregar.pack(fill="both", expand=True)


def mostrar_frame_mostrar():
    frame_menu.pack_forget()
    frame_agregar.pack_forget()
    frame_reporte.pack_forget()
    frame_mostrar.pack(fill="both", expand=True)

def mostrar_frame_reporte():
    frame_menu.pack_forget()
    frame_agregar.pack_forget()
    frame_mostrar.pack_forget()
    frame_reporte.pack(fill="both", expand=True)



# Boton: agregar nuevo producto
btn_agregar = tk.Button(botones_frame, text="Agregar nuevo producto", width=25, height=3,
                        font=("Sans-serif", 20, "bold"), bg="#4CAF50", fg="white", command=mostrar_frame_agregar)
btn_agregar.grid(row=0, column=0, padx=(0, 10))

# Boton: mostrar los productos
btn_mostrar = tk.Button(botones_frame, text="Mostrar y Editar inventario", width=25, height=3,
                        font=("Sans-serif", 20, "bold"), bg="#2196F3", fg="white", command=mostrar_frame_mostrar)
btn_mostrar.grid(row=0, column=1, padx=(10, 0))

# Boton: descargar reporte
btn_reporte = tk.Button(frame_menu, text="Descargar reporte de inventario", width=25, height=3,
                        font=("Sans-serif", 20, "bold"), bg="#607D8B", fg="white", command=mostrar_frame_reporte)
btn_reporte.pack(pady=10)


# Ejecutar ventana
root.mainloop()