
#!/bin/bash
# Ruta del archivo de bloqueo
LOCKFILE="/tmp/ejecucion.lock"
LOCKFD=99

# Función para crear el archivo de bloqueo
lock() {
  eval "exec $LOCKFD>$LOCKFILE"
  flock -n $LOCKFD \
    && return 0 \
    || return 1
}

# Función para eliminar el archivo de bloqueo
unlock() {
  eval "exec $LOCKFD>&-"
  rm -f $LOCKFILE
}

# Intentar crear el archivo de bloqueo
if ! lock; then
  echo "Otro proceso está en ejecución. Saliendo..." >> /home/cdatos/recoleccn_datos/recoleccion_CDMX/registro_de_ejecuciones.log
  exit 1
fi

# Asegurar que el archivo de bloqueo se elimine incluso si el script se cancela
trap "unlock" EXIT

# Añadir rutas adicionales al PATH
export PATH="/usr/local/bin:/usr/bin:/bin:/home/cdatos/recoleccion_datos/recoleccion_CDMX/datos/bin:$PATH"

# Activar el entorno virtual usando la ruta completa
source /home/cdatos/recoleccion_datos/recoleccion_CDMX/datos/bin/activate

# Crear directorio con la fecha actual
DATE_DIR=$(date +'%d-%m-%y')
OUTPUT_DIR="/home/cdatos/recoleccion_datos/recoleccion_CDMX/datos_depurados/$DATE_DIR"
mkdir -p $OUTPUT_DIR

# Ejecutar el script Python usando la ruta completa y pasar el directorio de salida como argumento
/home/cdatos/recoleccion_datos/recoleccion_Iztapalapa/datos/bin/python3 /home/cdatos/recoleccion_datos/recoleccion_CDMX/main.py $OUTPUT_DIR >> /home/cdatos/recoleccion_datos/recoleccion_CDMX/registro_de_ejecuciones.log 2>&1

# Registrar la hora de ejecución
echo "main.py ejecutado el día $(date +'%d-%m-%y a las %H:%M')" >> /home/cdatos/recoleccion_datos/recoleccionCDMX/registro_de_ejecuciones.log

# Eliminar el archivo de bloqueo al finalizar
unlock
