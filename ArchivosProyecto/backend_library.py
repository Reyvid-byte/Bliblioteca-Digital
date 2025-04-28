import json
import os
from datetime import datetime, timedelta

LIBROS_JSON = "libros.json"
PRESTAMOS_JSON = "prestamos.json"
USUARIOS_JSON = "usuarios.json"

def cargar_datos(archivo):
    if not os.path.exists(archivo):
        return []
    try:
        with open(archivo, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos(archivo, datos):
    with open(archivo, "w") as f:
        json.dump(datos, f, indent=4)

class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.penalizaciones = 0
        self.monto_penalizaciones = 0

def crear_usuario(nombre, id_usuario, usuarios):
    if not nombre or not id_usuario:
        return False, "Campos incompletos"
    elif any(u["id_usuario"] == id_usuario for u in usuarios):
        return False, "El usuario ya existe"
    
    nuevo_usuario = {"nombre": nombre, "id_usuario": id_usuario, "penalizaciones": 0, "monto_penalizaciones" : 0}
    usuarios.append(nuevo_usuario)
    guardar_datos(USUARIOS_JSON, usuarios)
    return True, "Usuario creado exitosamente"

def pagar_monto(id_usuario, usuarios, monto_pagado):
    if not id_usuario or not monto_pagado:
        return False, "Campos incompletos"
    usuario = next((u for u in usuarios if u["id_usuario"] == id_usuario), None)
    if not usuario:
        return False, "Usuario no registrado"
    
    monto_a_pagar = usuario.get("monto_penalizaciones", 0)

    try:
        monto_pagado = float(monto_pagado)
    except ValueError:
        return False, "Monto ingresado inválido"
    
    if usuario['penalizaciones'] == 0:
        return True, "El usuario no cuenta con penalizaciones"
                               
    elif monto_pagado >= monto_a_pagar:
        usuario["penalizaciones"] -= 1
        usuario["monto_penalizaciones"] = 0
        guardar_datos(USUARIOS_JSON, usuarios)
        return True, "El usuario ha liberado correctamente su penalizacion"

    else:
        usuario["monto_penalizaciones"] -= monto_pagado
        guardar_datos(USUARIOS_JSON, usuarios)
        faltante = usuario['monto_penalizaciones']
        return True, f"Al usuario aun le falta pagar ${faltante}"

    

def buscar_libros(libros, criterio, valor):
    return [libro for libro in libros if valor.lower() in libro[criterio].lower()]

def realizar_prestamo(libros, prestamos, usuarios, id_usuario, titulo):
    usuario = next((u for u in usuarios if u["id_usuario"] == id_usuario), None)
    if not usuario:
        return False, "Usuario no registrado"
    if usuario["penalizaciones"] > 0:
        return False, "Usuario tiene penalizaciones activas"
    
    libro_prestado = next((p for p in prestamos if p["título"].lower() == titulo.lower()), None)
    if libro_prestado:
        return False, "Libro ya prestado"
    
    libro = next((l for l in libros if l["título"].lower() == titulo.lower()), None)
    if libro:
        fecha_para_devolver = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        prestamos.append({"título": titulo, "fecha_para_devolver": fecha_para_devolver, "id_usuario": id_usuario})
        guardar_datos(PRESTAMOS_JSON, prestamos)
        return True, f"Préstamo registrado. Devuelva antes del {fecha_para_devolver}"
    return False, "Libro no encontrado"

def agregar_libro(libros, titulo, autor, genero, portada=None):
    titulo_nuevo = next((p for p in libros if p["título"].lower() == titulo.lower()), None)
    if titulo_nuevo:
        return False, "Libro ya registrado"
    elif not titulo or not autor or not genero:
        return False, "Campos incompletos"
    nuevo_libro = {"título": titulo, "autor": autor, "género": genero, "portada": portada}
    libros.append(nuevo_libro)
    guardar_datos(LIBROS_JSON, libros)
    return True, "Libro agregado correctamente"

def registrar_devolucion(prestamos, usuarios, id_usuario, titulo, fecha_actual_str):
    prestamo = next((p for p in prestamos if p["título"].lower() == titulo.lower() and p["id_usuario"] == id_usuario), None)
    
    if prestamo:
        fecha_actual = datetime.strptime(fecha_actual_str, '%Y-%m-%d')
        usuario = next((u for u in usuarios if u["id_usuario"] == id_usuario), None)
  
        fecha_para_devolver = datetime.strptime(prestamo["fecha_para_devolver"], '%Y-%m-%d')
        
        if fecha_actual > fecha_para_devolver and usuario:

            dias_excedidos = (fecha_actual - fecha_para_devolver).days
            monto_penalizacion = dias_excedidos * 5

            usuario["penalizaciones"] += 1
            usuario["monto_penalizaciones"] += monto_penalizacion
        
            guardar_datos(USUARIOS_JSON, usuarios)
            prestamos.remove(prestamo)
            guardar_datos(PRESTAMOS_JSON, prestamos)
            return True, f"El usuario excedió la fecha límite. Penalización agregada de ${monto_penalizacion}."
            
        
        prestamos.remove(prestamo)
        guardar_datos(PRESTAMOS_JSON, prestamos)
        
        return True, "Libro devuelto correctamente"
    
    return False, "No hay préstamos para este libro"
