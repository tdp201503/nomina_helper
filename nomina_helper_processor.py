"""
NominaHelper v3.0
Programa para calcular la nomina de una empresa. Lee los nombres y salarios desde un archivo de texto
que se suministra como argumento de linea de comandos, por ejemplo, nombres.txt. Al final guarda la liquidacion
en el archivo liquidacion.txt, el registro de errores en errores.txt y el registro de operacion en log.txt.
A partir de la version 3, Nomina Helper es el nuevo nombre, cambia de EasyNomina. Tambien a partir de esta version
el programa cuenta con interfaz grafica de usuario (GUI) desarrollada en PyQt4.

Desarrollado por Juan Sebastian Lopez Villa
Octubre 15 de 2015
Valores de porcentajes para liquidacion de nomina tomados de http://www.gerencie.com/liquidacion-de-la-nomina.html.
"""

# Importar libreria sys para manejo de argumentos de linea de comandos
import sys
# Importar las clases del modelo de NominaHelper.
from modelo.nomina import *
from utils.log_utils import *


class NominaHelperProcessor:
    def __init__(self, configuracion_nomina):
        self.configuracion_nomina = configuracion_nomina
        self.log_utils = LogUtils(self.configuracion_nomina.nombre_archivo_errores,
                                  self.configuracion_nomina.nombre_archivo_registro)

    def validar_linea(self, linea_por_validar, numero_linea):
        array_respuesta = [0 for x in range(3)]

        # Separar la linea por el simbolo (token) *
        arreglo_campos = linea_por_validar.split("*")

        # Validar la estructura de cada linea.
        # Validacion 4 (Va4)
        if len(arreglo_campos) != 2:
            self.log_utils.guardar_error("La linea " + str(numero_linea) + " no cumple con la estructura requerida! Revisarla!")
            array_respuesta[0] = False
            return array_respuesta

        nombre_por_validar = arreglo_campos[0]

        arreglo_nombre = nombre_por_validar.split(" ")

        # Validar el numero de palabras del nombre
        # Validacion 5 (Va5)
        if len(arreglo_nombre) < 2 or len(arreglo_nombre) > 5:
            self.log_utils.guardar_error(
                "El nombre " + arreglo_campos[0] + " no cumple con la longitud requerida! Revisar linea numero " + str(
                    numero_linea) + " de archivo de nomina.")
            array_respuesta[0] = False
            return array_respuesta

        array_respuesta[1] = arreglo_nombre

        # Validar que el salario sea de tipo numerico
        # Validacion 6 (Va6)
        try:
            salario_base = int(arreglo_campos[1])
            array_respuesta[2] = salario_base
        except ValueError:
            self.log_utils.guardar_error("El valor de salario " + arreglo_campos[
                1] + " no puede convertirse a entero! Revisar linea numero " + str(
                numero_linea) + " de archivo de nomina.")
            array_respuesta[0] = False
            return array_respuesta

        array_respuesta[0] = True
        return array_respuesta

    # Funcion que finaliza el programa y guarda el respectivo mensaje de terminacion en el archivo errores.txt
    def terminar_programa(self, mensaje_terminacion):
        self.log_utils.guardar_error(mensaje_terminacion)
        self.log_utils.guardar_log("Programa terminado por error... Verificar archivo errores.txt para mas detalles.")

        # Terminar el programa
        sys.exit()

    def validar_archivo_nomina(self, nombre_archivo_nomina):
        if not nombre_archivo_nomina.endswith(".txt"):
            self.terminar_programa("El archivo de nomina no tiene extension .txt!")

        self.log_utils.guardar_log("Extension de archivo de nomina OK")

        # Variable que almacena las lineas del archivo, su contenido como tal.
        lineas_archivo_nomina = tuple(self.log_utils.leer_lineas_archivo(nombre_archivo_nomina))

        # Variable que almacena el numero de lineas del archivo
        numero_lineas_nomina = len(lineas_archivo_nomina)

        self.log_utils.guardar_log("Archivo de nomina leido OK")

        # Validar que el archivo tenga el minimo numero de lineas.
        # Validacion 3 (Va3)
        if numero_lineas_nomina < self.configuracion_nomina.numero_minimo_lineas:
            self.terminar_programa("El archivo de nomina debe contener como minimo " +
                                   str(self.configuracion_nomina.numero_minimo_lineas) + " lineas!")

    def calcular_auxilio_transporte(self, salario_base):
        if salario_base <= self.configuracion_nomina.tope_auxilio_transporte:
            self.log_utils.guardar_log("Empleado con derecho a auxilio de transporte ...")
            return self.configuracion_nomina.auxilio_transporte
        else:
            return 0

    def calcular_fondo_solidaridad(self, salario_base):
        if salario_base >= self.configuracion_nomina.tope_fondo_solidaridad:
            self.log_utils.guardar_log("Empleado paga fondo solidaridad pensional ...")
            return self.configuracion_nomina.porcentaje_fondo_solidaridad * salario_base
        else:
            return 0

    def calcular_seguridad_social(self, salario_base):
        # ----- Seguridad Social ----- #
        # Porcentaje aporte de salud realizado por la empresa 8.5%
        self.log_utils.guardar_log("Calculando aporte salud empresa ...")
        aporte_salud_empresa = 0.085 * salario_base

        # Porcentaje aporte de salud realizado por la empresa 12%
        self.log_utils.guardar_log("Calculando aporte pension empresa ...")
        aporte_pension_empresa = 0.12 * salario_base

        # Porcentaje aporte de riesgos laborales realizado por la empresa.
        self.log_utils.guardar_log("Calculando aporte ARL con porcentaje " +
                                   ("%.3f" % self.configuracion_nomina.porcentaje_arl) + " ...")

        aporte_arl_empresa = self.configuracion_nomina.porcentaje_arl * salario_base

        return SeguridadSocial(aporte_salud_empresa, aporte_pension_empresa, aporte_arl_empresa)

    def calcular_aportes_parafiscales(self, salario_base):
        # ----- Aportes Parafiscales ----- #
        # Porcentaje aporte parafiscal para SENA realizado por la empresa 2%
        self.log_utils.guardar_log("Calculando aporte parafiscales sena ...")
        aporte_parafiscales_sena = 0.02 * salario_base

        # Porcentaje aporte parafiscal para ICBF realizado por la empresa 3%
        self.log_utils.guardar_log("Calculando aporte parafiscales ICBF ...")
        aporte_parafiscales_icbf = 0.03 * salario_base

        # Porcentaje aporte parafiscal para Cajas de Compensacion realizado por la empresa 4%
        self.log_utils.guardar_log("Calculando aporte parafiscales cajas de compensacion ...")
        aporte_parafiscales_cajas = 0.04 * salario_base

        return AporteParafiscal(aporte_parafiscales_sena, aporte_parafiscales_icbf, aporte_parafiscales_cajas)

    def calcular_prestaciones_sociales(self, salario_base, auxilio_transporte_efectivo):
        # ----- Prestaciones Sociales ----- #
        # Porcentaje aporte cesantias realizado por la empresa 8.33%. Se debe tener en cuenta el auxilio de transporte.
        self.log_utils.guardar_log("Calculando aporte cesantias ...")
        aporte_cesantias = 0.0833 * (salario_base + auxilio_transporte_efectivo)

        # Porcentaje aporte intereses sobre cesantias realizado por la empresa 1%
        self.log_utils.guardar_log("Calculando aporte intereses sobre cesantias ...")
        aporte_intereses_cesantias = 0.01 * aporte_cesantias

        # Porcentaje aporte prima de servicios realizado por la empresa 8.33%.
        # Se debe tener en cuenta el auxilio de transporte.
        self.log_utils.guardar_log("Calculando aporte prima de servicios ...")
        aporte_prima = 0.0833 * (salario_base + auxilio_transporte_efectivo)

        # Porcentaje aporte vacaciones realizado por la empresa 4.17%
        self.log_utils.guardar_log("Calculando aporte vacaciones ...")
        aporte_vacaciones = 0.0833 * salario_base

        return PrestacionSocial(aporte_cesantias, aporte_intereses_cesantias, aporte_prima, aporte_vacaciones)

    def calcular_apropiaciones(self, salario_base, auxilio_transporte_efectivo):
        seguridad_social = self.calcular_seguridad_social(salario_base)
        aportes_parafiscales = self.calcular_aportes_parafiscales(salario_base)
        prestaciones_sociales = self.calcular_prestaciones_sociales(salario_base, auxilio_transporte_efectivo)

        return Apropiacion(seguridad_social, aportes_parafiscales, prestaciones_sociales)

    def calcular_deducciones(self, salario_base):
        # Porcentaje aporte de salud realizado por el empleado 4%
        self.log_utils.guardar_log("Calculando aporte salud empleado ...")
        aporte_salud_empleado = 0.04 * salario_base

        self.log_utils.guardar_log("Calculando aporte fondo de solidaridad pensional ...")
        aporte_fondo_solidaridad = self.calcular_fondo_solidaridad(salario_base)

        # Porcentaje aporte de salud realizado por el empleado 4%
        self.log_utils.guardar_log("Calculando aporte pension empleado ...")
        aporte_pension_empleado = 0.04 * salario_base

        return Deduccion(aporte_salud_empleado, aporte_pension_empleado, aporte_fondo_solidaridad)

    def calcular_nomina(self, empleado):
        auxilio_transporte_efectivo = self.calcular_auxilio_transporte(empleado.salario)
        apropiaciones = self.calcular_apropiaciones(empleado.salario, auxilio_transporte_efectivo)
        deducciones = self.calcular_deducciones(empleado.salario)

        return NominaEmpleado(apropiaciones,deducciones, auxilio_transporte_efectivo)

    def guardar_liquidacion_nomina(self, liquidaciones_empleados, nombre_archivo_liquidacion):
        self.log_utils.guardar_log("Creando archivo " + nombre_archivo_liquidacion + " ...")
        self.log_utils.crear_archivo(nombre_archivo_liquidacion)

        # Ciclo 3 para guardar liquidacion en archivo liquidacion.txt.
        self.log_utils.guardar_log("Guardando liquidacion...")
        for liquidacion_empleado in liquidaciones_empleados:
            contenido_linea = (
                liquidacion_empleado.empleado.id, # Id empleado
                liquidacion_empleado.empleado.nombre, # Nombre empleado
                liquidacion_empleado.empleado.cargo, # Cargo empleado
                int(liquidacion_empleado.empleado.salario), # Salario base
                liquidacion_empleado.nomina_empleado.valor_auxilio_transporte, # Aporte auxilio de transporte efectivo.
                liquidacion_empleado.nomina_empleado.apropiacion.prestacion_social.cesantias, # Aporte cesantias
                liquidacion_empleado.nomina_empleado.apropiacion.prestacion_social.interes_cesantias, # Aporte intereses sobre cesantias
                liquidacion_empleado.nomina_empleado.apropiacion.prestacion_social.prima_servicios, # Aporte prima
                liquidacion_empleado.nomina_empleado.apropiacion.prestacion_social.vacaciones, # Aporte vacaciones
                liquidacion_empleado.nomina_empleado.apropiacion.seguridad_social.arl, # Aporte arl
                liquidacion_empleado.nomina_empleado.apropiacion.seguridad_social.salud_empresa, # Aporte salud empresa
                liquidacion_empleado.nomina_empleado.apropiacion.seguridad_social.pension_empresa, # Aporte pension empresa
                liquidacion_empleado.nomina_empleado.apropiacion.aporte_parafiscal.sena, # Aporte SENA
                liquidacion_empleado.nomina_empleado.apropiacion.aporte_parafiscal.icbf, # Aporte ICBF
                liquidacion_empleado.nomina_empleado.apropiacion.aporte_parafiscal.cajas, # Aporte Cajas de Compensacion
                liquidacion_empleado.nomina_empleado.deduccion.salud_empleado, # Aporte salud empleado
                liquidacion_empleado.nomina_empleado.deduccion.pension_empleado, # Aporte pension empleado
                liquidacion_empleado.nomina_empleado.deduccion.aporte_fondo_solidaridad, # Aporte fondo de solidaridad
                liquidacion_empleado.salario_neto, # Salario neto para el empleado
                liquidacion_empleado.costo_empresa # Costo total para la empresa
            )

            formato_linea = "Id: %d " \
                            "Nombre: %s " \
                            "Cargo: %s" \
                            "Salario base: %.2f " \
                            "Auxilio de Transporte: %.2f " \
                            "Apropiaciones -> " \
                            "Prestaciones Sociales - " \
                            "Cesantias: %.2f " \
                            "Intereses sobre cesantias: %.2f " \
                            "Prima: %.2f " \
                            "Vacaciones: %.2f " \
                            "Seguridad Social - " \
                            "ARL: %.2f " \
                            "Salud empresa: %.2f " \
                            "Pension empresa: %.2f " \
                            "Parafiscales - " \
                            "SENA: %.2f " \
                            "ICBF: %.2f " \
                            "Cajas: %.2f " \
                            "Deducciones -> " \
                            "Salud empleado: %.2f " \
                            "Pension empleado: %.2f " \
                            "Fondo de solidaridad: %.2f " \
                            "-- Salario neto empleado --> : %.2f " \
                            "-- Costo total empresa --> : %.2f " \
                            "\n"

            self.log_utils.escribir_linea_archivo(nombre_archivo_liquidacion, formato_linea % contenido_linea)
        self.log_utils.guardar_log("Liquidacion guardada...")