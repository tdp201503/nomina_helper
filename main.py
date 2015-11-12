from PyQt4 import QtGui
import sys
from nomina_helper import NominaHelper
from modelo.configuracion_nomina import ConfiguracionNomina


def main():
    app = QtGui.QApplication(sys.argv)

    # Constantes validas para el anio 2015
    smlv = int(644350)
    auxilio_transporte = int(74000)

    # Configuracion por defecto
    configuracion_por_defecto = ConfiguracionNomina(
        "errores.txt",  # Nombre archivo de errores
        "log.txt",  # Nombre archivo de registro de operacion del programa
        "liquidacion.liq",  # Nombre archivo que contendra la liquidacion de la nomina
        2,  # Numero minimo de lineas para archivo de nomina
        smlv,  # Salario Minimo Legal Vigente (SMLV) 2015
        auxilio_transporte,  # Auxilio de Transporte 2015
        2 * smlv,  # El auxilio de transporte solo se da si gana igual o menor a 2 SMLV
        4 * smlv,  # Quienes ganes igual o mas de 4 SMLV contribuyen 1% al fondo de solidaridad pensional
        0.01,  # Porcentaje de deducccion de aporte al fondo de solidaridad pensional.
        0.00522  # Porcentaje Administracion de Riesgos Laborales. Modifcar porcentaje segun el tipo de riesgo definido en: https://www.positiva.gov.co/ARL/Paginas/default.aspx
    )

    app_gui = NominaHelper(configuracion_por_defecto)
    app_gui.show()
    app.exec_()


if __name__ == "__main__":
    main()
