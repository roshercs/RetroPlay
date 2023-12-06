#!/bin/bash


# Actualizacion del sistema
sudo apt-get -y update
sudo apt-get -y full-upgrade

# Ruta base donde se creará la carpeta RetroPlay
base_dir="/home/pi"

# Verificar si la carpeta RetroPlay ya existe
retroplay_dir="$base_dir/RetroPlay"
if [ ! -d "$retroplay_dir" ]; then
    # Si la carpeta RetroPlay no existe, la crea
    mkdir "$retroplay_dir"
    echo "Carpeta RetroPlay creada."
fi

# Crear carpetas 'images' y 'rom' dentro de carpeta home
images_dir="$base_dir/images"
rom_dir="$base_dir/rom"
if [ ! -d "$images_dir" ]; then
    # Si la carpeta 'images' no existe, la crea dentro de RetroPlay
    mkdir "$images_dir"
    echo "Carpeta 'images' creada dentro de RetroPlay."
fi

if [ ! -d "$rom_dir" ]; then
    # Si la carpeta 'rom' no existe, la crea dentro de RetroPlay
    mkdir "$rom_dir"
    echo "Carpeta 'rom' creada dentro de RetroPlay."
fi

# Paquetes a instalar
packages=("python3-venv" "python-rpi.gpio" "matchbox-keyboard" "mednafen")
for package in "${packages[@]}"; do
    if ! dpkg -s "$package" &> /dev/null; then
        echo "Instalando $package..."
        sudo apt-get update
        sudo apt-get install -y "$package"
        echo "$package instalado correctamente."
    else
        echo "$package ya está instalado."
    fi
done

# Crear entorno virtual RetroPlay
retroplay_env="$retroplay_dir"
if [ ! -d "$retroplay_env" ]; then
    echo "Creando entorno virtual RetroPlay..."
    python3 -m venv "$retroplay_env"
    echo "Entorno virtual RetroPlay creado en $retroplay_env."
    
else
    echo "El entorno virtual RetroPlay ya existe en $retroplay_env."
fi
# Activar el entorno virtual
echo "Activando entorno virtual RetroPlay..."
source "$retroplay_env/bin/activate"
echo "Entorno virtual RetroPlay activado."

# Copiar RetroPlay.py al entorno virtual RetroPlay
gitDir="$base_dir/gitCopy"
if [ -f "$gitDir/RetroPlay.py" ]; then
    # Si el archivo RetroPlay.py ya existe en el directorio actual
    cp "$gitDir/RetroPlay.py" "$retroplay_env/"
    echo "Archivo RetroPlay.py copiado al entorno virtual RetroPlay."
else
    echo "No se pudo copiar codigo fuente, se pide la copia manual"
fi

# Copiar imágenes al directorio /home/pi/images
src_images_dir="$gitDir/src/images"
home_images_dir="$base_dir/images"
if [ -d "$src_images_dir" ]; then
    echo "Copiando imágenes desde $src_images_dir a $home_images_dir..."
    cp -r "$src_images_dir"/* "$home_images_dir/"
    echo "Imágenes copiadas exitosamente a $home_images_dir."
else
    echo "El directorio $src_images_dir no existe. No se han copiado imágenes."
fi

# Activar el entorno virtual RetroPlay
echo "Activando entorno virtual RetroPlay..."
source "$retroplay_env/bin/activate"
echo "Entorno virtual RetroPlay activado."

# Instalar bibliotecas necesarias con pip en el entorno virtual
libraries=("python-vlc" "pillow" "keyboard" "pyudev")
for lib in "${libraries[@]}"; do
    if python -c "import $lib" &> /dev/null; then
        echo "$lib ya está instalado en el entorno virtual RetroPlay."
    else
        echo "Instalando $lib en el entorno virtual RetroPlay..."
        pip install "$lib"
        echo "$lib instalado correctamente en el entorno virtual RetroPlay."
    fi
done

autostart_dir="$base_dir/.config/autostart"
if [ ! -d "$autostart_dir" ]; then
    echo "Creando directorio autostart en /home/pi/.config..."
    mkdir -p "$autostart_dir"
    echo "Directorio autostart creado en /home/pi/.config."
else
    echo "El directorio autostart ya existe en /home/pi/.config."
fi
# Copiar el archivo inicio.desktop desde /home/pi/gitCopy a /home/pi/.config/autostart
inicio_desktop="/home/pi/.config/autostart/inicio.desktop"
if [ ! -f "$inicio_desktop" ]; then
    echo "Copiando inicio.desktop a $autostart_dir..."
    cp "$gitDir/src/inicio.desktop" "$autostart_dir/"
    echo "Archivo inicio.desktop copiado correctamente a $autostart_dir."
else
    echo "El archivo inicio.desktop ya existe en $autostart_dir."
fi




echo "Estructura de carpetas creada y paquetes instalados exitosamente en RetroPlay."
