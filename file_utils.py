import sys
import log_utils

class FileUtils():

	def __init__(self, log_utils):
		self.log_utils = log_utils

	# Funcion que crear un archivo con el nombre especificado. Devuelve True si fue exitoso o False en caso de error.
	def crear_archivo(nombre_archivo):
		try:
			archivo = open(nombre_archivo, 'w')
			archivo.close()
		except:
			self.log_utils.guardar_error("Error creando archivo " + nombre_archivo + "!");
			return False
			
		return True

	# Funcion que lee las lineas de un archivo de texto y las devuelve en una lista.
	def leer_lineas_archivo(nombre_archivo):
		lineas = ()
		try:
			archivo = open(nombre_archivo, 'r')
			lineas = archivo.readlines()
			archivo.close()
		except IOError:
			self.log_utils.guardar_error("Error leyendo archivo " + nombre_archivo + "!")
			
		return lineas 