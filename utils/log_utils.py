import sys


class LogUtils:
    def __init__(self, nombre_archivo_errores, nombre_archivo_registro):
        self.nombre_archivo_errores = nombre_archivo_errores
        self.nombre_archivo_registro = nombre_archivo_registro

    # Funcion que crear un archivo con el nombre especificado. Devuelve True si fue exitoso o False en caso de error.
    def crear_archivo(self, nombre_archivo):
        try:
            archivo = open(nombre_archivo, 'w')
            archivo.close()
        except IOError:
            self.guardar_error("Error creando archivo " + nombre_archivo + "!");
            return False

        return True

    # Funcion que lee las lineas de un archivo de texto y las devuelve en una lista.
    def leer_lineas_archivo(self, nombre_archivo):
        lineas = ()
        try:
            archivo = open(nombre_archivo, 'r')
            lineas = archivo.readlines()
            archivo.close()
        except IOError:
            self.guardar_error("Error leyendo archivo " + nombre_archivo + "!")

        return lineas

    # Funcion que guarda al final del archivo definido la linea especificada. Devuelve True si fue exitoso o False en caso de error.
    def escribir_linea_archivo(self, nombre_archivo, linea_a_escribir):
        try:
            archivo = open(nombre_archivo, 'a')
            archivo.write(linea_a_escribir)
            archivo.close()
        except IOError:
            self.guardar_error("Error escribiendo linea " + linea_a_escribir + " en archivo " + nombre_archivo + "!")
            return False

        return True

    # Funcion que guarda un mensaje de error en el archivo errores.txt
    def guardar_error(self, mensaje_error):
        self.escribir_linea_archivo(self.nombre_archivo_errores, "\n" + mensaje_error + "\n")

    # Funcion que guarda un registro de operacion en el archivo log.txt
    def guardar_log(self, mensaje_registro):
        self.escribir_linea_archivo(self.nombre_archivo_registro, "\n" + mensaje_registro + "\n")
