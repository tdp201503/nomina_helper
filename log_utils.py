import sys
import file_utils

class LogUtils():

	def __init__(self, nombre_archivo_errores, nombre_archivo_registro):
		self.nombre_archivo_errores = nombre_archivo_errores
		self.nombre_archivo_registro = nombre_archivo_registro

	# Funcion que guarda al final del archivo definido la linea especificada. Devuelve True si fue exitoso o False en caso de error.
	def escribir_linea_archivo(nombre_archivo, linea_a_escribir):	
		try:
			archivo = open(nombre_archivo, 'a')
			archivo.write(linea_a_escribir)
			archivo.close()
		except IOError:
			self.guardar_error("Error escribiendo linea " + linea_a_escribir + " en archivo " + nombre_archivo + "!")
			return False
			
		return True
		
	# Funcion que guarda un mensaje de error en el archivo errores.txt
	def guardar_error(mensaje_error):
		self.escribir_linea_archivo(self.nombre_archivo_errores, "\n" + mensaje_error + "\n")
		
	# Funcion que guarda un registro de operacion en el archivo log.txt
	def guardar_log(mensaje_registro):
		self.escribir_linea_archivo(self.nombre_archivo_registro, "\n" + mensaje_registro + "\n")
		
	
		
		