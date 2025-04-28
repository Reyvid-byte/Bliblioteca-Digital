import tkinter as tk
from tkinter import ttk, messagebox
from backend_library import cargar_datos, buscar_libros, realizar_prestamo, agregar_libro, registrar_devolucion, crear_usuario, pagar_monto
import customtkinter as ctk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import shutil
import os
from tkinter import filedialog


libros = cargar_datos("libros.json")
prestamos = cargar_datos("prestamos.json")
usuarios = cargar_datos("usuarios.json")

def seleccionar_imagen(entry_portada):
    ruta_imagen = filedialog.askopenfilename(
        title="Seleccionar portada",
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
    )
    
    if ruta_imagen:
        carpeta_portadas = "portadas"
        if not os.path.exists(carpeta_portadas):
            os.makedirs(carpeta_portadas)
        
        nombre_archivo = os.path.basename(ruta_imagen)
        destino = os.path.join(carpeta_portadas, nombre_archivo)
        
        if os.path.abspath(ruta_imagen) != os.path.abspath(destino):
            shutil.copy(ruta_imagen, destino)  
        
        entry_portada.delete(0, "end")
        entry_portada.insert(0, f"{carpeta_portadas}/{nombre_archivo}")

def configurar_fondo(ventana, ruta_imagen):
    try:
        # Almacenar la imagen como atributo de la ventana
        ventana.imagen_fondo = Image.open(ruta_imagen)
        label_fondo = ctk.CTkLabel(ventana, text="")
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        # Almacenar PhotoImage como atributo
        ventana.imagen_tk = ImageTk.PhotoImage(ventana.imagen_fondo.resize(
            (ventana.winfo_width(), ventana.winfo_height()), 
            Image.LANCZOS
        ))
        label_fondo.configure(image=ventana.imagen_tk)

        def redimensionar(event=None):
            nueva_img = ventana.imagen_fondo.resize(
                (ventana.winfo_width(), ventana.winfo_height()), 
                Image.LANCZOS
            )
            ventana.imagen_tk = ImageTk.PhotoImage(nueva_img)
            label_fondo.configure(image=ventana.imagen_tk)

        ventana.bind("<Configure>", lambda e: root.after(100, redimensionar))  

    except Exception as e:
        print(f"Error cargando fondo: {e}")


def pantalla_inicio():
    global root, imagen_original, imagen_tk, label_fondo, current_size
    root = ctk.CTk()
    root.title("Biblitoteca Digital")
    root.geometry("800x600")
    root.iconbitmap("./Blibliotecaria.ico")

    imagen_original = Image.open("./BibliotecaFondo.jpg")
    current_size = (0, 0)  
    
    frame = ctk.CTkFrame(root, fg_color="transparent")
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_fondo = ctk.CTkLabel(master=frame, text="")
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

    def redimensionar_imagen(event=None):
        global imagen_tk, current_size
        ancho, alto = root.winfo_width(), root.winfo_height()
        if (ancho, alto) != current_size:  
            nueva_img = imagen_original.resize((ancho, alto), Image.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(nueva_img)
            label_fondo.configure(image=imagen_tk)
            current_size = (ancho, alto)

    root.bind("<Configure>", lambda e: root.after(150, redimensionar_imagen))  

    frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="cols")
    frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1, uniform="rows")

    icono_usuarios = ctk.CTkImage(light_image=Image.open("./iconoUsuario.png"), size=(40, 40))
    icono_libros = ctk.CTkImage(light_image=Image.open("./iconoLibros.png"), size=(40, 40))
    icono_prestar = ctk.CTkImage(light_image=Image.open("./iconoPrestar.png"), size=(40, 40))
    icono_catologo = ctk.CTkImage(light_image=Image.open("./iconoCatalogo.png"), size=(40, 40))

    frame_titulo = ctk.CTkFrame(
        master=frame,
        fg_color="#F3C776",
        corner_radius=8
    )
    frame_titulo.grid(
        column=0, row=0,
        columnspan=4, rowspan=1,
        sticky="nsew", padx=4, pady=4
    )


    ctk.CTkLabel(frame_titulo, text="Bienvenido a la Biblioteca", font=("Arial", 25)).pack(pady=10, expand=True)

    boton_icono = {
    "master": frame,
    "compound": "top",          # Texto debajo de la imagen
    "width": 120,               
    "height": 120,              
    "corner_radius": 10,        # Bordes redondeados
    "fg_color": "transparent",  
    "hover_color": "#498AF3",  
    "text_color": "#333333",    # Color del texto
    "anchor": "center",         # Centrar contenido
    "font": ("Arial", 12)      # Fuente del texto
    }
    
    ctk.CTkButton(
        **boton_icono,
        text="Administrar Usuarios",
        image=icono_usuarios,
        command=administrar_usuarios_ui
    ).grid(column=1, row=2, sticky="nsew", padx=10, pady=10)

    ctk.CTkButton(
        **boton_icono,
        text="Buscar Libros",
        image=icono_libros,
        command=buscar_libros_ui
    ).grid(column=2, row=2, sticky="nsew", padx=10, pady=10)
    
    ctk.CTkButton(
        **boton_icono,
        text="Prestar Libros",
        image=icono_prestar,
        command=realizar_prestamo_ui, 
        ).grid(column=1, row=3, sticky="nsew", padx=10, pady=10)
    
    ctk.CTkButton(
        **boton_icono,
        text="Administrar Catalogo",
        image=icono_catologo,
        command=administrar_catalogo_ui, 
        ).grid(column=2, row=3, sticky="nsew", padx=10, pady=10)
    
    root.mainloop()

def limpiar_entradas(*entradas):
    for entrada in entradas:
        entrada.delete(0, "end")

def administrar_usuarios_ui():
    root1 = ctk.CTkToplevel()
    root1.title("Administrar Usuarios")
    root1.geometry("600x400")
    root1.after(100, lambda: root1.focus())

    configurar_fondo(root1, "FondoGeneral.jpg")
    
    root1.grid_columnconfigure((0, 1), weight=1)
    root1.grid_rowconfigure((0, 1), weight=1)


    frame_registrar = ctk.CTkFrame(
        master=root1, 
        fg_color="#A6F8F1",
        corner_radius=8
    )
    frame_registrar.grid(
        column=0, row=0,
        padx=10, pady=10,
        sticky="nsew"
    )

    ctk.CTkLabel(frame_registrar, text="Agregar Usuario", font=("Arial", 12, "bold")).pack(pady=5)

    ctk.CTkLabel(frame_registrar, text="Nombre:").pack()
    entrada_nombre = ctk.CTkEntry(frame_registrar)
    entrada_nombre.pack()
    
    ctk.CTkLabel(frame_registrar, text="ID Usuario:").pack()
    entrada_id_usuario = ctk.CTkEntry(frame_registrar)
    entrada_id_usuario.pack()
    
    def registrar():
        exito, mensaje = crear_usuario(entrada_nombre.get(), entrada_id_usuario.get(), usuarios)
        messagebox.showinfo("Registro", mensaje)

        limpiar_entradas(entrada_nombre, entrada_id_usuario)

    
    ctk.CTkButton(frame_registrar, text="Registrar",hover_color = "#12E82E", command=registrar).pack(pady=5)

    frame_penalizacion = ctk.CTkFrame(
        master=root1,  
        fg_color="#FFEEEE",
        corner_radius=8
    )
    frame_penalizacion.grid(
        column=1, row=0,
        padx=10, pady=10,
        sticky="nsew"
    )

    ctk.CTkLabel(frame_penalizacion, text="Gestion Penalizaciones", font=("Arial", 12, "bold")).pack(pady=5)

    ctk.CTkLabel(frame_penalizacion, text="ID Usuario:").pack()
    entrada_id = ctk.CTkEntry(frame_penalizacion)
    entrada_id.pack()

    ctk.CTkLabel(frame_penalizacion, text="Monto Pagado:").pack()
    entrada_monto_pagado = ctk.CTkEntry(frame_penalizacion)
    entrada_monto_pagado.pack()

    def pagar_monto_ui():
        exito, mensaje = pagar_monto(entrada_id.get(), usuarios, entrada_monto_pagado.get())
        messagebox.showinfo("Pago", mensaje)

        limpiar_entradas(entrada_id, entrada_monto_pagado)

    ctk.CTkButton(
        frame_penalizacion,
        text="Registrar Pago",
        hover_color = "#12E82E",
        command=pagar_monto_ui
    ).pack(pady=5)

    ctk.CTkButton(
        root1,
        text="Cerrar",
        command=root1.destroy,
        fg_color="#D35B58",
        hover_color="#C34C49",
        width=80
    ).grid(
        column=1, row=1,
        padx=10, pady=10,
        sticky="se"
    )

    root1.mainloop()

def buscar_libros_ui():
    root2 = ctk.CTkToplevel()
    root2.title("Buscar Libros")
    root2.geometry("600x400")
    root2.after(100, lambda: root2.focus())
    
    imagenes = []
    frame_principal = ctk.CTkFrame(root2, fg_color="transparent")
    frame_principal.pack(expand=True, fill="both", padx=10, pady=10)
    
    frame_busqueda = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_busqueda.pack(fill="x", pady=5)
    
    ctk.CTkLabel(frame_busqueda, text="Buscar por:").pack(side="left", padx=5)
    
    filtro = ctk.CTkComboBox(
        frame_busqueda,
        values=["Autor", "Género", "Título"],
        state="readonly"
    )
    filtro.pack(side="left", padx=5)
    
    entrada = ctk.CTkEntry(frame_busqueda)
    entrada.pack(side="left", padx=5, expand=True, fill="x")
    
    def filtrar():
        resultados = buscar_libros(libros, filtro.get().lower(), entrada.get().lower())
        actualizar_lista(resultados)
    
    ctk.CTkButton(
        frame_busqueda,
        text="Buscar",
        command=filtrar,
        width=80
    ).pack(side="left", padx=5)
    
    frame_tabla = ctk.CTkFrame(frame_principal)
    frame_tabla.pack(expand=True, fill="both", pady=10)
    
    lista = ttk.Treeview(
        frame_tabla,
        columns=("Título", "Autor", "Género"),
        show="tree headings", 
        style="Custom.Treeview"
    )

    lista.heading("#0", text="Portada", anchor="center")
    lista.column("#0", width=100, anchor="center", stretch=False)  # Ancho fijo

    lista.heading("Título", text="Título")
    lista.column("Título", width=180, anchor="w")

    lista.heading("Autor", text="Autor")
    lista.column("Autor", width=150, anchor="w")

    lista.heading("Género", text="Género")
    lista.column("Género", width=120, anchor="w")

    lista["displaycolumns"] = ("Título", "Autor", "Género")

    lista.column("#0", width=100, anchor="center")
    lista.heading("#0", text="Portada", anchor="center")
    
    style = ttk.Style()
    style.configure("Custom.Treeview",
        background="#333333",
        foreground="white",
        fieldbackground="#333333",
        borderwidth=0,
        rowheight=122,  # Altura de fila = altura de la imagen
        padding=(5, 5),  # Espaciado interno para mejor visualización
        font=("Arial", 12)
    )
    style.map("Custom.Treeview", background=[("selected", "#1F6AA5")])
    
    lista.heading("Título", text="Título")
    lista.heading("Autor", text="Autor")
    lista.heading("Género", text="Género")
    lista.pack(expand=True, fill="both")
        
    scrollbar = ttk.Scrollbar(
        frame_tabla,
        orient="vertical",
        command=lista.yview
    )
    lista.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    lista.pack(expand=True, fill="both", side="left")  
    
    def actualizar_lista(datos):
        nonlocal imagenes
        imagenes.clear()
        for row in lista.get_children():
            lista.delete(row)
            
        for libro in datos:
            img = Image.new("RGB", (80, 120), color="#EEEEEE")  # Imagen por defecto
            if libro.get("portada"):
                try:
                    img = Image.open(libro["portada"])
                    img = img.resize((80, 120), Image.LANCZOS)
                except Exception as e:
                    print(f"Error: {e}")
                    
            imagen = ImageTk.PhotoImage(img)
            imagenes.append(imagen)  # ¡Referencia persistente!
            
            lista.insert(
                "", 
                "end", 
                image=imagen, 
                values=(libro["título"], libro["autor"], libro["género"])
            )

    
    frame_inferior = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_inferior.pack(fill="x", pady=5)
    
    ctk.CTkButton(
        frame_inferior,
        text="Cerrar",
        command=root2.destroy,
        fg_color="#D35B58",
        hover_color="#C34C49",
        width=80
    ).pack(side="right", padx=5)
    
    actualizar_lista(libros)

def realizar_prestamo_ui():
    root3 = ctk.CTkToplevel()
    root3.title("Realizar Prestamos")
    root3.geometry("800x600")
    root3.after(100, lambda: root3.focus())

    
    configurar_fondo(root3, "FondoGeneral.jpg")
    
    root3.grid_columnconfigure((0, 1, 2), weight=1)
    root3.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

    frame_prestamos = ctk.CTkFrame(
        master=root3,
        fg_color="#FDE289",
        corner_radius=8
    )
    frame_prestamos.grid(
        column=0, row=0,
        columnspan=3, rowspan=2,
        sticky="nsew", padx=4, pady=4
    )
    
    ctk.CTkLabel(frame_prestamos, text="ID Usuario:").pack()
    entrada_id_penalizaciones = ctk.CTkEntry(frame_prestamos)
    entrada_id_penalizaciones.pack()
    
    ctk.CTkLabel(frame_prestamos, text="Título del libro:").pack()
    entrada_titulo = ctk.CTkEntry(frame_prestamos)
    entrada_titulo.pack()
    
    def registrar():
        exito, mensaje = realizar_prestamo(libros, prestamos, usuarios, entrada_id_penalizaciones.get(), entrada_titulo.get())
        messagebox.showinfo("Préstamo", mensaje)
        limpiar_entradas(entrada_id_penalizaciones, entrada_titulo)
        actualizar_lista_prestamos()  # Actualizar tabla después de nuevo préstamo
    
    ctk.CTkButton(frame_prestamos, text="Prestar", command=registrar, hover_color = "#12E82E").pack(pady=10)

    frame_lista_prestamos = ctk.CTkFrame(root3)
    frame_lista_prestamos.grid(
        column=0, row=2,
        columnspan=3, rowspan=2,
        sticky="nsew", padx=10, pady=10
    )

    style = ttk.Style()
    style.configure("Prestamos.Treeview",
        background="#333333",
        foreground="white",
        fieldbackground="#333333",
        borderwidth=0,
        font=("Arial", 12)
    )
    style.map("Prestamos.Treeview", background=[("selected", "#1F6AA5")])

    lista_prestamos = ttk.Treeview(
        frame_lista_prestamos,
        columns=("Título", "ID Usuario", "Fecha Devolución"),
        show="headings",
        style="Prestamos.Treeview"
    )
    
    lista_prestamos.heading("Título", text="Título")
    lista_prestamos.heading("ID Usuario", text="ID Usuario")
    lista_prestamos.heading("Fecha Devolución", text="Fecha Devolución")
    
    scrollbar = ttk.Scrollbar(
        frame_lista_prestamos,
        orient="vertical",
        command=lista_prestamos.yview
    )
    lista_prestamos.configure(yscrollcommand=scrollbar.set)
    
    lista_prestamos.pack(side="left", expand=True, fill="both")
    scrollbar.pack(side="right", fill="y")

    def actualizar_lista_prestamos():
        for item in lista_prestamos.get_children():
            lista_prestamos.delete(item)
        for prestamo in prestamos:
            lista_prestamos.insert("", "end", values=(
                prestamo["título"],
                prestamo["id_usuario"],
                prestamo["fecha_para_devolver"]
            ))
    
    ctk.CTkButton(
        root3,
        text="Cerrar",
        command=root3.destroy,
        fg_color="#D35B58",
        hover_color="#C34C49",
        width=80
    ).grid(
        column=2, row=4,
        padx=10, pady=10,
        sticky="se"
    )

    # Cargar datos iniciales
    actualizar_lista_prestamos()

    root3.mainloop()

def administrar_catalogo_ui():
    root4 = ctk.CTkToplevel()
    root4.title("Administrar Catálogo")
    root4.geometry("600x400")
    root4.after(100, lambda: root4.focus())

    configurar_fondo(root4, "FondoGeneral.jpg")
    
    root4.grid_columnconfigure((0, 1, 2, 3), weight=1)
    root4.grid_rowconfigure((0, 1, 2, 3), weight=1)

    frame_devolucion = ctk.CTkFrame(
        master=root4,
        fg_color="#B6A9FB",
        corner_radius=8
    )
    frame_devolucion.grid(
        column=0, row=0,
        columnspan=2, rowspan=3,
        sticky="nsew", padx=4, pady=4
    )

    ctk.CTkLabel(frame_devolucion, text="Registrar Devolución", font=("Arial", 12, "bold")).pack(pady=5)
    
    ctk.CTkLabel(frame_devolucion, text="ID Usuario:").pack()
    entrada_id_devolucion = ctk.CTkEntry(frame_devolucion)
    entrada_id_devolucion.pack()
    
    ctk.CTkLabel(frame_devolucion, text="Título Prestado:").pack()
    entrada_titulo_prestado = ctk.CTkEntry(frame_devolucion)
    entrada_titulo_prestado.pack()

    ctk.CTkLabel(frame_devolucion, text="Fecha de Devolución:").pack()
    fecha_devolucion = DateEntry(frame_devolucion, date_pattern='yyyy-mm-dd')
    fecha_devolucion.pack()
    
    def registrar_devolucion_ui():
        fecha = fecha_devolucion.get_date().strftime('%Y-%m-%d')
        exito, mensaje = registrar_devolucion(prestamos, usuarios, entrada_id_devolucion.get(), entrada_titulo_prestado.get(), fecha)
        messagebox.showinfo("Devolución", mensaje)

        limpiar_entradas(entrada_id_devolucion, entrada_titulo_prestado)
    
    ctk.CTkButton(
        frame_devolucion,
        text="Registrar Devolución",
        hover_color = "#12E82E",
        command=registrar_devolucion_ui
    ).pack(pady=5)

    frame_libro = ctk.CTkFrame(
        master=root4,
        fg_color="#A9FBB5",
        corner_radius=8
    )
    frame_libro.grid(
        column=2, row=0,
        columnspan=2, rowspan=3,
        sticky="nsew", padx=4, pady=4
    )

    ctk.CTkLabel(frame_libro, text="Agregar Libro", font=("Arial", 12, "bold")).pack(pady=5)
    
    ctk.CTkLabel(frame_libro, text="Título:").pack()
    entrada_titulo = ctk.CTkEntry(frame_libro)
    entrada_titulo.pack()
    
    ctk.CTkLabel(frame_libro, text="Autor:").pack()
    entrada_autor = ctk.CTkEntry(frame_libro)
    entrada_autor.pack()
    
    ctk.CTkLabel(frame_libro, text="Género:").pack()
    entrada_genero = ctk.CTkEntry(frame_libro)
    entrada_genero.pack()
    
    ctk.CTkLabel(frame_libro, text="Portada:").pack()
    entrada_portada = ctk.CTkEntry(frame_libro)
    entrada_portada.pack()
    ctk.CTkButton(
        frame_libro,
        hover_color = "#12E82E",
        text="Cargar imagen",
        command=lambda: seleccionar_imagen(entrada_portada)
    ).pack(pady=5)
    
    def agregar():
        exito, mensaje = agregar_libro(
            libros,
            entrada_titulo.get(),
            entrada_autor.get(),
            entrada_genero.get(),
            entrada_portada.get()  
        )
        messagebox.showinfo("Agregar", mensaje)

        limpiar_entradas(entrada_titulo, entrada_autor, entrada_genero, entrada_portada)
    
    ctk.CTkButton(
        frame_libro,
        text="Agregar Libro",
        hover_color = "#12E82E",
        command=agregar
    ).pack(pady=5)

    ctk.CTkButton(
        root4,
        text="Cerrar",
        command=root4.destroy,
        fg_color="#D35B58",
        hover_color="#C34C49",
        width=80
    ).grid(
        column=3, row=3,
        padx=10, pady=10,
        sticky="se"
    )

    root4.mainloop()

if __name__ == "__main__":
    pantalla_inicio()
