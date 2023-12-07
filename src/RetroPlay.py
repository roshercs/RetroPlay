#########################################################
# Consola Retro de entretenimineto: Emulación de NES, SNES y GameBoy Advanced
# 
# Autor código original: Rogelio Hernandez
# License: MIT
#   
# Fecha de realización: 05/Diciembre/2023
#########################################################


import tkinter as tk
from PIL import Image, ImageTk
import os
import hashlib
from time import sleep
#import pyudev
import subprocess as sp
import shutil
import threading
import RPi.GPIO as GPIO
from gpiozero import Button
#import pyautogui
import keyboard
import pyudev
import vlc

#Variables globales para ventanas
root=0
frame=0
runMednafen=0
# Parametros de paginacion
items_per_page = 4
selected_index = 0
start_index = 0
#Manejo de Carga de juegos
home = '/home/pi'
ruta_roms = '/home/pi/roms/'
lista_juegos=[]
gameCount=0
usb_path='usbTry/'
juegoDetectado=0
nuevos_juegos=[]
ventana_msg=0
#Variables Mednafen
ruta_mednafen ='/usr/games/mednafen'
ruta_roms_abs='/home/pi/roms/'

#Variables Controlador
boton_L=3
boton_U=5
boton_R=7
boton_Sel=8
boton_D=10
boton_LS=11
boton_Start=12
boton_B=13
boton_A=15
boton_RS=16
boton_Y=18
boton_X=19
boton_Ex=22
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(boton_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_U,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_Sel,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_D,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_LS,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_Start,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_B,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_A,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_RS,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_Y,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_X,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_Ex,GPIO.IN,pull_up_down=GPIO.PUD_UP)

estado_anterior=0
estado_actual=0

wait_event=threading.Event()

# Funcion para calcular el hash de un archivo
def calcular_hash(nombre_archivo):
    sha256 = hashlib.sha256() 
    #Apertura de archivo a evaluar
    with open(nombre_archivo, 'rb') as archivo:
        while True:
            #Lectura por bloques del archivo
            bloque = archivo.read(8192)
            if not bloque: #Si no hay lectura se termina el ciclo
                break
            #Se agrega los datos del bloque al calculo de hash
            sha256.update(bloque)
    return sha256.hexdigest() #Se retorna el valor hash calculado en cadena hexadecimal
#Se obtiene el hash de cada rom ya cargada y se compara con la rom del posible nuevo juego
def compare_roms(archivo_1):
    global lista_juegos
    global nuevos_juegos
    global juegoDetectado
    hash_archivo_1 = calcular_hash(usb_path+archivo_1)
    for archivo_2 in lista_juegos:
        hash_archivo_2 = calcular_hash('/home/pi/roms/'+archivo_2)
        if hash_archivo_1 == hash_archivo_2:    #Si el hash de por lo menos un juego ya cargado coincide, se determina que hay repeticion y se omite el juego
            print("Juego repetido")
            return
    juegoDetectado=1
    #Si no se coincide ningun hash se agrega el nuevo juego
    print(f"Se ha encontrado un nuevo juego: {archivo_1}")
    lista_juegos.append(archivo_1)
    shutil.copy(usb_path+archivo_1, ruta_roms)
    print("Valor new_game ",juegoDetectado)
    nuevos_juegos.append(archivo_1)
        
#Secuencia de listado de juegos contenidos en USB conectada: Se listan todos los archivos en memoria
def upload_games():
    global lista_juegos
    extensiones=['.nes','.gba','.sfc']
    # Lista todos los archivos en la carpeta
    archivos_en_carpeta = os.listdir(usb_path)
    for archivo in archivos_en_carpeta:
        if archivo.endswith(tuple(extensiones)):   #extrae aquellos con las extensiones dadas
            compare_roms(archivo)
    actualizar_lista()
def close_window(event):
    global ventana_msg
    ventana_msg.destroy()

#Se imprime el listado de juegos por upload_games
def print_list_games():
    global nuevos_juegos
    global ventana_msg
    global root
    global runMednafen
    mensaje="\n".join(nuevos_juegos)
    #Creacion de ventana auxiliar
    ventana_msg=tk.Tk()
    ventana_msg.title("Nuevos juegos adquiridos")
    ventana_msg.resizable(False,False)
    ancho_pantalla=480
    alto_pantalla=640
    ventana_msg.geometry(f"{ancho_pantalla}x{alto_pantalla}")
    
    ventana_msg.attributes('-fullscreen', True)  # Establece la ventana en pantalla completa
    # Cambiar el fondo de la ventana a azul oscuro
    ventana_msg.configure(bg="#1f497d")
    # Enlazar la tecla escape a cerrar ventana
    ventana_msg.bind("<Return>", close_window)
    
    label_title = tk.Label(ventana_msg, text="Nuevos juegos adquiridos", font=("Arial", 24, "bold"), padx=25, pady=15,bg="#C1BFFF")
    label_title.place(x=0, y=0)  # Ajuste posicional

    control_continue = tk.Label(ventana_msg, text="Presione START para continuar", font=("Arial", 11),padx=25, pady=5,bg="#C1BFFF")
    control_continue.place(x=0, y=root.winfo_screenheight()-30)  # Ajuste posicional
    #frame para contener lista
    list_frame=tk.Frame(ventana_msg)
    list_frame.pack(expand=True)
    
    #Creacion de listado con parametros dados
    lista=tk.Listbox(list_frame,width=40,height=10,font=("Arial",12),bg="blue",fg="white",selectbackground="blue",selectforeground="white",highlightthickness=0,activestyle="none",selectmode=tk.SINGLE)
    lista.pack(expand=True)
    for elemento in nuevos_juegos:
        lista.insert(tk.END,elemento) #Se agrega a la lista cada elemento de nuevos_juegos
    list_frame.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
    
    ventana_msg.mainloop()
    
#Obtencion de punto de montaje de una USB. path indica la ruta donde se detecto la nueva conexion, ej. /dev/sda. Retorna el punto de montaje ej. /media/pi/usb    
def get_mount_point(path):
	args = ["findmnt", "-unl", "-S", path]
	cp = sp.run(args, capture_output=True, text=True)
	out = cp.stdout.split(" ")[0]
	return out
#Detección constante de nuevas conexiones de USB, de detectarse se llama a la extracción de nuevos juegos detectados y de encontrarlos se imprime el listado de juegos agregados
def detection_usb():
    global usb_path
    global juegoDetectado
    global nuevos_juegos
    global runMednafen
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem="block")
    for device in iter(monitor.poll,None):
        if device.action=='add' and 'ID_FS_TYPE' in device:
          if 'usb' in device.get('ID_BUS'):
            print("USB conectado")
            nomDispo=device.device_node
            sleep(1)
            usb_path=get_mount_point(nomDispo)+'/'
            print("Dispositivo:",nomDispo)
            print("Ruta:",usb_path)
            upload_games()
            print("Valor new_game (usb)",juegoDetectado)
            if juegoDetectado==1:
                print("Nuevos juegos agregados: ",nuevos_juegos)
                #Meintras Mednafen ejecute no se imprime la lista de nuevos juegos, una vez concluido ya se procede a imprimir
                while runMednafen==1:
                    sleep(1)
                print("Procede a imprimir lista")
                print_list_games()
                #Reinicio de nuevos juegos agregados
                juegoDetectado=0
                nuevos_juegos=[]
#Manejo de items de pagina actual. Segun el item "actualmente" seleccionado se imprime un bloque de juegos u otros
def actualizar_lista():
    global frame
    # Limpiar la lista actual
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Determinar la p�gina actual
    page = selected_index // items_per_page
    start_index = page * items_per_page
    
    # Mostrar los elementos siguientes en el arreglo
    for i in range(start_index, min(start_index + items_per_page, len(lista_juegos))):
        juego = lista_juegos[i]
        # Crear un frame para cada elemento del men�
        menu_item_frame = tk.Frame(frame, bg="#1f497d")
        menu_item_frame.pack(fill=tk.X)  # Llenar horizontalmente el espacio disponible
        #Estructura para determinar la imagen portada del juego. Al no poder obtenerla, asignamos el logo de la consola a la que pertenece
        if "nes" in juego:
            img = Image.open(f"images/nes.png").resize((120, 180))
        elif "sfc" in juego:
            img = Image.open(f"images/snes.png").resize((120, 180))
        else:   #Caso GameBoy Advance
            img = Image.open(f"images/gba.png").resize((120, 180))
        img = ImageTk.PhotoImage(img)
        #Cuando se encuentra seleccionada se resalta cambiando el fondo a blanco
        if i == selected_index:
            img_label = tk.Label(menu_item_frame, image=img, bg="white")
            # Etiqueta para el texto
            text_label = tk.Label(menu_item_frame, text=lista_juegos[i], padx=10, pady=15, bg="white")
        else:
            img_label = tk.Label(menu_item_frame, image=img, bg="#1f497d")
            # Etiqueta para el texto
            text_label = tk.Label(menu_item_frame, text=lista_juegos[i], padx=10, pady=15, bg="#1f497d")

        # Etiqueta para la imagen
        
        img_label.image = img  # Para evitar que la imagen sea eliminada por el recolector de basura
        img_label.pack(side=tk.LEFT)
        text_label.pack(side=tk.LEFT)


# Funci�n para mover la selecci�n hacia arriba
def move_up(event):
    global selected_index
    if selected_index > 0:
        selected_index -= 1
        actualizar_lista()
        # Verificar si la selecci�n est� fuera de la lista actual y ajustar la p�gina
        if selected_index < start_index:
            move_page("up")

# Funci�n para mover la selecci�n hacia abajo
def move_down(event):
    global selected_index
    if selected_index < len(lista_juegos) - 1:
        selected_index += 1
        actualizar_lista()
        # Verificar si la selecci�n est� fuera de la lista actual y ajustar la p�gina
        if selected_index >= start_index + items_per_page:
            move_page("down")

# Funci�n para mover la p�gina hacia arriba o hacia abajo
def move_page(direction):
    global start_index
    if direction == "up" and start_index > 0:
        start_index -= items_per_page
        actualizar_lista()
    elif direction == "down" and start_index + items_per_page < len(lista_juegos):
        start_index += items_per_page
        actualizar_lista()

#Lista las ROMS precargadas al inicio del programa
def load_start_roms():
    global lista_juegos
    # Lista todos los archivos en la carpeta
    archivos_en_carpeta = os.listdir(ruta_roms)
    #Lectura de roms NES
    archivos_nes = [archivo for archivo in archivos_en_carpeta if archivo.endswith('.nes')]
    for rom in archivos_nes:
        #Opcion de depuracion
        print(f"Juego: {rom} (funcion de carga)")
        lista_juegos.append(rom)
    #Lectura de roms SNES
    archivos_snes = [archivo for archivo in archivos_en_carpeta if archivo.endswith('.sfc')]
    for rom in archivos_snes:
        #Opcion de depuracion
        print(f"Juego: {rom} (funcion de carga)")
        lista_juegos.append(rom)
    #Lectura de roms GBA
    archivos_gba = [archivo for archivo in archivos_en_carpeta if archivo.endswith('.gba')]
    for rom in archivos_gba:
        #Opcion de depuracion
        print(f"Juego: {rom} (funcion de carga)")
        lista_juegos.append(rom)
#Manejo de funciones de acción (A, B, X, Y, left shoulder, right shoulder)
def manejo_control_accion():
    try:
        while True:
            #Gestion Boton Left-Shoulder LS
            estado_actual=GPIO.input(boton_LS)  
            if estado_actual==GPIO.LOW:
                keyboard.press(16)#tecla Q
                sleep(0.2)
                keyboard.release(16)
            #Gestion Boton B
            estado_actual=GPIO.input(boton_B)
            if estado_actual==GPIO.LOW:
                keyboard.press(48)#tecla espacio
                sleep(0.2)
                keyboard.release(48)
            #Gestion Boton A
            estado_actual=GPIO.input(boton_A) #Se lee el estado actual del boton asociado a A
            if estado_actual==GPIO.LOW: #Si se encuentra en bajo significa que se pulso el boton
                keyboard.press(30)  #emula la pulsación de la tecla A de teclado
                sleep(0.2)
                keyboard.release(30)   #se libera la pulsación
            #Gestion Boton Right-Shoulder RS
            estado_actual=GPIO.input(boton_RS)
            if estado_actual==GPIO.LOW:
                keyboard.press(18)#tecla E
                sleep(0.2)
                keyboard.release(18)
            #Gestion Boton Y
            estado_actual=GPIO.input(boton_Y)
            if estado_actual==GPIO.LOW:
                keyboard.press(21)
                sleep(0.2)
                keyboard.release(21)
            #Gestion Boton X
            estado_actual=GPIO.input(boton_X)
            if estado_actual==GPIO.LOW:
                keyboard.press(45)
                sleep(0.2)
                keyboard.release(45)
            
            sleep(0.01)
    except:
        pass
#Manejo de funciones de movimiento y especiales(start, select y exit)
def manejo_control_movimiento():
    while True:
        #print("Entro manejador")
        #Gestion Boton Exit
        estado_actual=GPIO.input(boton_Ex)  #Se lee estado actual del boton asiciado a Exit
        if estado_actual==GPIO.LOW: #Si está en estado bajo se pulso el boton
            keyboard.press(1)   #Emula el pulso de la tecla Escape
            sleep(0.2)
            keyboard.release(1)
        #Gestion Boton Start
        estado_actual=GPIO.input(boton_Start)
        if estado_actual==GPIO.LOW:
            keyboard.press(28)#tecla espacio
            sleep(0.2)
            keyboard.release(28)
        #Gestion Boton Select
        estado_actual=GPIO.input(boton_Sel)
        if estado_actual==GPIO.LOW:
            keyboard.press(57)#tecla espacio
            sleep(0.2)
            keyboard.release(57)
        #Gestion Boton Left
        estado_actual=GPIO.input(boton_L)
        if estado_actual==GPIO.LOW:
            keyboard.press(105)#tecla left
            sleep(0.2)
            keyboard.release(105)
        #Gestion Boton Up
        estado_actual=GPIO.input(boton_U)
        if estado_actual==GPIO.LOW:
            keyboard.press(103)#tecla up
            sleep(0.2)
            keyboard.release(103)
        #Gestion Boton Right
        estado_actual=GPIO.input(boton_R)
        if estado_actual==GPIO.LOW:
            keyboard.press(106)#tecla right
            sleep(0.2)
            keyboard.release(106)
        #Gestion Boton Down
        estado_actual=GPIO.input(boton_D)
        if estado_actual==GPIO.LOW:
            keyboard.press(108)#tecla down
            sleep(0.2)
            keyboard.release(108)       
        sleep(0.01)

# Funci�n para seleccionar un elemento
def select_item(event):
    global runMednafen
    juego=lista_juegos[selected_index]
    print("Elemento seleccionado:", juego)
    #comando='mednafen "'+ruta_roms_abs+juego+'"' 
    comando='sudo '+ruta_mednafen+' "'+ruta_roms_abs+juego+'"' 
    #comando=ruta_mednafen+' -video.fs 1 "'+ruta_roms_abs+ruta_roms+juego+'"'
    print("Comando final: ",comando)
    #hilo = threading.Thread(target=ejecutar_mednafen,args=(comando,))
    #hilo.start()
    runMednafen=1
    proceso=sp.run(comando,shell=True)
    try:
        proceso.wait()
    except:
        print("Prueba de alcance mednafen")
    runMednafen=0
    print("Valor runMednafen:",runMednafen)

def cerrar_debug(event):
    global root
    #root.quit()
    wait_event.clear()
    root.destroy()

#Emulación de teclado virtual por matchbox-keyboard. Se evita el uso de teclado físico para emplear el gamepad
def teclado_virtual():
    comando='sudo /usr/bin/matchbox-keyboard'
    proceso=sp.run(comando,shell=True)
    try:
        proceso.wait()
    except:
        print("Fin teclado virtual")
def menu():
    global root
    global frame
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Menu de Consola")
    # Cambiar el fondo de la ventana a azul oscuro
    root.configure(bg="#1f497d")
    root.resizable(False,False)
    ancho_pantalla=root.winfo_screenwidth()
    alto_pantalla=root.winfo_screenheight()
    root.geometry(f"{ancho_pantalla}x{alto_pantalla}")
    root.overrideredirect(True)
    root.overrideredirect(False)
    root.attributes('-fullscreen', True)  # Establece la ventana en pantalla completa
    # Crear el marco para la lista de objetos
    frame = tk.Frame(root)
    frame.pack()

    # Etiqueta "Seleccione un juego" en la esquina superior derecha
    label_title = tk.Label(root, text="Seleccione un juego", font=("Arial", 24, "bold"), padx=25, pady=15,bg="#C1BFFF")
    label_title.place(x=0, y=0)  # Ajuste posicional

    # Etiquetas de Controles de men� en la esquina inferior derecha
    control_menu_move = tk.Label(root, text="▲ Elemento anterior \t\t▼ Siguiente elemento  ", font=("Arial", 11),padx=25, pady=5,bg="#C1BFFF")
    control_menu_move.place(x=0, y=root.winfo_screenheight()-60)  # Ajuste posicional
    control_menu_move = tk.Label(root, text="START Seleccionar \t\tPWOF Apagar Consola", font=("Arial", 11),padx=25, pady=5,bg="#C1BFFF")
    control_menu_move.place(x=0, y=root.winfo_screenheight()-30)  # Ajuste posicional

    #Indicador "Conecte USB"
    # Etiquetas de Controles de men� en la esquina inferior derecha
    usb_label = tk.Label(root, text="Inserte USB para carga de ROMS... ", font=("Arial", 11,"italic","bold"),padx=25, pady=5,bg="#C1BFFF")
    usb_label.place(x=root.winfo_screenwidth()-280, y=root.winfo_screenheight()-30)  # Ajuste posicional

    # Enlazar las teclas de flecha hacia arriba y hacia abajo para el desplazamiento entre elementos
    root.bind("<Up>", move_up)
    root.bind("<Down>", move_down)

    # Enlazar la tecla "Enter" para seleccionar un elemento
    root.bind("<Return>", select_item)
    # Enlazar la tecla escape a cerrar ventana (modo debugger)
    #root.bind("<Escape>", cerrar_debug)
    #carga de roms inicial
    load_start_roms()

    # Mostrar la lista inicial
    actualizar_lista()
    #repVid.join()
    # Ejecutar la ventana
    is_fullscreen=root.attributes('-fullscreen')
    if is_fullscreen==False:
        root.attributes('-fullscreen',True)
    root.mainloop()


#Reproduccion de animacion inicial del logo de la consola. Uso de librería VLC
def reproduce_logo():
    ruta_logo= '/home/pi/RetroPlayLogo.mp4'
    # Inicializar VLC
    sleep(1)
    instancia = vlc.Instance('--no-xlib')
    # Crear reproductor
    reproductor = instancia.media_player_new()
    # Cargar el video
    medio = instancia.media_new(ruta_logo)
    reproductor.set_media(medio)
    # Reproducir el video
    reproductor.play()
    sleep(4)
    reproductor.stop()
try:
    repImg = threading.Thread(target=reproduce_logo)
    repImg.start()
    wait_event.set()
    teclado = threading.Thread(target=teclado_virtual)
    teclado.start()
    hilo1 = threading.Thread(target=manejo_control_movimiento)
    hilo1.start()
    hilo2 = threading.Thread(target=manejo_control_accion)
    hilo2.start()
    detectorUSB = threading.Thread(target=detection_usb)
    detectorUSB.start()
    menu()
except:
    pass
