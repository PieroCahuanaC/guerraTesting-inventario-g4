import tkinter as tk
from PIL import Image, ImageTk
import os

# Ventaja principal
root = tk.Tk()
root.title("Menú Principal - Muebles Moderno")
root.geometry("800x800")
root.state("zoomed")  # Maximiza la ventana

# Frame del menú principal
frame_menu = tk.Frame(root, bg="white")
frame_menu.pack(fill="both", expand=True)

# Logo
ruta_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets/logo.png')
if os.path.exists(ruta_logo):
    logo_img = Image.open(ruta_logo).resize((150, 150), Image.LANCZOS)
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(frame_menu, image=logo, bg="white")
    logo_label.pack(pady=10)
else:
    print("Logo no encontrado en la ruta especificada.")

# Titulo
titulo = tk.Label(frame_menu, text="MUEBLES MODERNO", bg="white", font=("Arial", 45, "bold"))
titulo.pack(pady=10)

# Ejecutar ventana
root.mainloop()
