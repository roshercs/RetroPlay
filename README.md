# RetroPlay
Consola retro de entretenimineto capaz de emular juegos de las consolas NES, SNES y GameBoy Advanced (extensión de archivo '.nes', '.sfc' y '.gba'). Implementa un menú de selección por el cual el usuario podrá visualizar todos los juegos almacenados en sistema y podrá seleccionar el de su preferencia para jugar. El sistema implementa también un detector de conexión USB, donde al encontrarse una nueva conexión, analizará los archivos con las extensiones válidas, comparará su hash respecto al resto de juegos ya cargados y de no encontrarse repetición almacenará los nuevos juegos en el sistema de forma perpetua. El sistema emplea Meadnafen para la emulación directa de los juegos, mientras que el programa del proyecto se encargará de la instanciación de forma automática según el usuario seleccione.

Enlace a video demostrativo de ejecución: https://youtu.be/u4oxUGFrXT0

Enlace a repositorio Github: https://github.com/roshercs/RetroPlay.git

Requerimientos: Raspberry Pi OS with Desktop 64 bits, tarjeta Raspberry Pi 3 o superior (Raspberry Pi 4 recomendada)
Bibliotecas: python-vlc, python3-venv, pillow, RPi.GPIO, keyboard, matchbox-keyboard, pyudev, mednafen


Se asume que el usuario realiza la instalación base del sistema operativo Raspberry Pi OS. El repositorio presente permite la descarga e instalación automática del proyecto al emplear el comando pip install git+https://github.com/roshercs/RetroPlay.git
Instalacion automatizada del proyecto:
Para la instalación del proyecto de forma más automatizada, requerimos crear la carpeta gitCopy en la ruta /home/pi. Para ello empleamos el comando sudo mkdir /home/pi/gitCopy. Una vez creada la carpeta descargamos el directorio de github (se asume que la tarjeta ya cuenta con conexión a internet). Para descargar el repositorio se requiere instalar los comandos de git, por lo que primero requerimos actualisar apt-get con el comando sudo apt-get update. Con este actualizado ejecutamos el comando 

    apt-get install git

Para habilitar los comandos de gitHub. Con los paquetes instalados se clona el repertorio en la carpeta creada con el comando:

    git clone https://github.com/roshercs/RetroPlay.git /home/pi/gitCopy

Esto copia el contenido del repositorio dentro de nuestro sistema. Con los archivos descargados procedemos a ejectuar la instalación automática. Nos debemos posicionar en la carpeta gitCopy (cd /home/pi/gitCopy). Dentro de este escritorio habilitamos el modo super usuario con el comando sudo su. Se conceden los permisos permitentes a la instalación con el comando:

    chmod +x install.sh

Con los permisos concedidos, ejecutamos el comando para ejecutar:

    ./install.sh



---------------------------------------------------------------
Instalación manual del proyecto:

En caso de optar por una instalación manual del proyecto, se recomienda tener conociminetos previos del uso del sistema Raspberry Pi OS o cualquier otra distribución de linux para evitar errores de sistema.
Primeramente, al requerirse la instalación de distintos paquetes se ejecutan los comandos apt-get -update y apt-get upgrade. El primero actualizará el instalador de paquetes mientras que el segundo actualizará los paquetes preinstalados en el sistema. Podemos instalar mednafen con el comando apt-get install mednafen. Además, se instala (o actualiza) la paquetería para el control de los pines GPIO: sudo apt-get install python-rpi.gpio. Además de estos dos paquetes se instala la paquetería matchbox-keyboard (apt install matchbox-keyboard) que permitirá emular un teclado virtual para de este modo no requerir del uso de teclados físicos en la consola.

Para la instalación del resto de paquetes se requiere la creación de un entorno virtual con python. Para ello instalamos el paquete necesariocon  sudo apt-get install python3-venv
Para la ejecución de este proyecto se requiere la creación de tres carpetas: roms, images y RetroPlay. Para ello se requiere el acceso a superusuario (sudo su) y la creación de cada una con los siquientes comandos: mkdir /home/pi/roms mkdir /home/pi/images y mkdir /home/pi/RetroPlay. Con estos creados, nos posicionamos en la carpeta RetroPlay (cd /home/pi/RetroPlay) y se crea un entorno virtual en python con el comando python3 -m venv RetroPlay. Con el entorno creado, podemos activarlo con el comando source /home/pi/RetroPlay/bin/activate.

Con el entorno virtual activo procedemos a la instalación de las bibliotecas necesarias con el comando pip install biblioteca (python-vlc, pillow, keyboard y pyudev)

Se requiere además modificar la configuración de mednafen. Para ello accedemos al archivo de configuración con nano ~/.mednafen/mednafen.cfg, dentro del cual buscaremos la opción "video.fs" y pondremos su valor a 1 para habilitar la pantalla completa. Además, se busca la opción "sound.devie" y se cambia el valor default por hw:2 para habilitar la salida de audio por el puerto jack 3.5 donde se podrá conectar audífonos o bocinas para la salida del audio.

Para configurar la tarjeta Raspberry para ejecutarse desde el arranque al emulador se requiere de la creación de un archivo. Dentro de la carpeta /home/pi/.config creamos la carpeta autostart. En esta se crea el archivo inicio.desktop.  En el archivo creado ingresamos como primera línea [Desktop Entry] (respetando mayúsculas) y a partir de la segunda linea los comandos a ejecutar usando el parámetro Exec=. En nuestro caso, ya que requerimos inicializar el entorno virtual y ejecutar el archivo, tendríamos:

    [Desktop Entry]
    Exec=sudo su
    Exec=source /home/pi/RetroPlay/bin/activate
    Exec=cd RetroPlay
    Exec=python3  RetroPlay.py

Adicionalmente, se requiere hacer copia de las imágenes disponibles en la carpeta images dentro de /doc a la carpeta immages del sistema, esto permitirá poner carátulas a los juegos según la consola a la que pertenecen. En este punto podemos también copiar el set de roms iniciales a precargar en el sistema. De no hacerse se requerirá insertar una USB para la copia de los juegos inciiales.
Con estas configuraciones, solo requerimos copiar el código fuente RetroPlay.py en la carpeta /home/pi/RetroPlay con el comando cp RetroPlay.py /home/pi/RetroPlay. Para que este funcione, el código fuente debe estar ubicado en la carpeta /home/pi, en otro caso se requerirá ingresar la ruta completa del archivo. Se usa el comando cp en modo superusuario para permitir la copia dentro del entorno virtual, sin estos privilegios no se permite la modificación de la carpeta de entorno virtual directamente.
