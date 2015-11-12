import time

from PyQt4 import QtGui, QtCore
from nomina_helper_gui import Ui_MainWindow
from modelo.nomina import *
from modelo.configuracion_nomina import ConfiguracionNomina
from nomina_helper_processor import NominaHelperProcessor


class NominaHelper(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, configuracion_por_defecto):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.configuracion_por_defecto = configuracion_por_defecto
        self.configuracion_nomina = configuracion_por_defecto

        self.nombre_archivo_errores.setText(configuracion_por_defecto.nombre_archivo_errores)
        self.nombre_archivo_registro.setText(configuracion_por_defecto.nombre_archivo_registro)
        self.nombre_archivo_liquidacion.setText(configuracion_por_defecto.nombre_archivo_liquidacion)
        self.numero_minimo_lineas.setText(str(configuracion_por_defecto.numero_minimo_lineas))
        self.smlv.setText(str(configuracion_por_defecto.smlv))
        self.auxilio_transporte.setText(str(configuracion_por_defecto.auxilio_transporte))
        self.tope_auxilio_transporte.setText(str(configuracion_por_defecto.tope_auxilio_transporte))
        self.tope_fondo_solidaridad.setText(str(configuracion_por_defecto.tope_fondo_solidaridad))
        self.porcentaje_fondo_solidaridad.setText(str(configuracion_por_defecto.porcentaje_fondo_solidaridad))
        self.porcentaje_arl.setText(str(configuracion_por_defecto.porcentaje_arl))

        self.processor = NominaHelperProcessor(configuracion_por_defecto)
        self.empleados = []
        self.nominas_empleados = []
        self.liquidaciones_empleados = []

        self.sleep_barra = 0.0
        self.step_barra = 0.0

        self.tabla_empleados_inicializada = False
        self.tabla_apropiaciones_inicializada = False
        self.tabla_deducciones_inicializada = False
        self.tabla_liquidacion_inicializada = False

        self.nomina_calculada = False

        # Conexion de signals & slots
        self.boton_cargar_archivo.clicked.connect(self.cargar_archivo)
        self.boton_calcular_nomina.clicked.connect(self.calcular_nomina)
        self.boton_guardar_liquidacion.clicked.connect(self.guardar_liquidacion)
        self.tabla_empleados.selectionModel().selectionChanged.connect(self.empleado_seleccionado)
        #self.connect(self.tabla_empleados.selectionModel(), QtCore.SIGNAL("selectionChanged()"), self.empleado_seleccionado)

        self.connect(self.smlv, QtCore.SIGNAL("editingFinished()"), self.actualizar_topes)
        self.boton_aplicar_cambios.clicked.connect(self.aplicar_cambios_configuracion)
        self.boton_cargar_valores_defecto.clicked.connect(self.cargar_configuracion_por_defecto)

    def actualizar_topes(self):
        nuevo_smlv = float(self.smlv.text())
        nuevo_tope_auxilio_transporte = 2 * nuevo_smlv
        nuevo_tope_fondo_solidaridad = 4 * nuevo_smlv

        self.configuracion_nomina.tope_auxilio_transporte

        self.tope_auxilio_transporte.setText(str(nuevo_tope_auxilio_transporte))
        self.tope_fondo_solidaridad.setText(str(nuevo_tope_fondo_solidaridad))

    def aplicar_cambios_configuracion(self):
        nueva_configuracion = ConfiguracionNomina(
            self.nombre_archivo_errores.text(),  # Nombre archivo de errores
            self.nombre_archivo_registro.text(),  # Nombre archivo de registro de operacion del programa
            self.nombre_archivo_liquidacion.text(),  # Nombre archivo que contendra la liquidacion de la nomina
            int(self.numero_minimo_lineas.text()),  # Numero minimo de lineas para archivo de nomina
            float(self.smlv.text()),  # Salario Minimo Legal Vigente (SMLV) 2015
            float(self.auxilio_transporte.text()),  # Auxilio de Transporte 2015
            float(self.tope_auxilio_transporte.text()),  # El auxilio de transporte solo se da si gana igual o menor a 2 SMLV
            float(self.tope_fondo_solidaridad.text()),  # Quienes ganes igual o mas de 4 SMLV contribuyen 1% al fondo de solidaridad pensional
            float(self.porcentaje_fondo_solidaridad.text()),  # Porcentaje de deducccion de aporte al fondo de solidaridad pensional.
            float(self.porcentaje_arl.text())  # Porcentaje Administracion de Riesgos Laborales. Modifcar porcentaje segun el tipo de riesgo definido en: https://www.positiva.gov.co/ARL/Paginas/default.aspx
        )
        self.configuracion_nomina = nueva_configuracion
        self.processor = NominaHelperProcessor(nueva_configuracion)

    def cargar_configuracion_por_defecto(self):
        self.configuracion_nomina = self.configuracion_por_defecto
        self.processor = NominaHelperProcessor(self.configuracion_por_defecto)

        self.nombre_archivo_errores.setText(self.configuracion_por_defecto.nombre_archivo_errores)
        self.nombre_archivo_registro.setText(self.configuracion_por_defecto.nombre_archivo_registro)
        self.nombre_archivo_liquidacion.setText(self.configuracion_por_defecto.nombre_archivo_liquidacion)
        self.numero_minimo_lineas.setText(str(self.configuracion_por_defecto.numero_minimo_lineas))
        self.smlv.setText(str(self.configuracion_por_defecto.smlv))
        self.auxilio_transporte.setText(str(self.configuracion_por_defecto.auxilio_transporte))
        self.tope_auxilio_transporte.setText(str(self.configuracion_por_defecto.tope_auxilio_transporte))
        self.tope_fondo_solidaridad.setText(str(self.configuracion_por_defecto.tope_fondo_solidaridad))
        self.porcentaje_fondo_solidaridad.setText(str(self.configuracion_por_defecto.porcentaje_fondo_solidaridad))
        self.porcentaje_arl.setText(str(self.configuracion_por_defecto.porcentaje_arl))

    def iniciar_barra_progreso(self, mensaje, n_steps, sleep_barra):
        self.sleep_barra = sleep_barra
        self.barra_progreso.setEnabled(True)
        self.mensaje_progreso.setText(mensaje)
        self.barra_progreso.reset()
        self.step_barra = float(100.0/n_steps)

    def finalizar_barra_progreso(self, mensaje):
        self.barra_progreso.setEnabled(False)
        self.mensaje_progreso.setText(mensaje)

    def avanzar_barra_progreso(self, valor):
        time.sleep(self.sleep_barra)
        self.barra_progreso.setValue(valor * self.step_barra)

    def cargar_empleados(self, ruta_nomina):
        archivo_nomina = open(ruta_nomina, 'r')
        lineas_archivo_nomina = archivo_nomina.readlines()

        print "Leyendo empleados ..."

        n_lineas_nomina = len(lineas_archivo_nomina)

        for i in range(n_lineas_nomina):
            # Eliminar el \n al final
            linea_empleado = lineas_archivo_nomina[i].strip()
            # print "Leyendo empleado " + str(i) + ": " + empleado
            campos_empleado = linea_empleado.split("*")

            self.empleados.append(Empleado(i, campos_empleado[0], int(campos_empleado[1]), campos_empleado[2]))

    def inicializar_tabla_empleados(self):
        encabezados_tabla_empleados = QtCore.QStringList()
        encabezados_tabla_empleados << "Nombre" << "Salario" << "Cargo"

        self.tabla_empleados.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.tabla_empleados.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tabla_empleados.setColumnCount(3)
        self.tabla_empleados.setColumnWidth(0, 250)
        self.tabla_empleados.setColumnWidth(1, 120)
        self.tabla_empleados.setColumnWidth(2, 200)
        self.tabla_empleados.setHorizontalHeaderLabels(encabezados_tabla_empleados)

    def actualizar_tabla_empleados(self):
        if not self.tabla_empleados_inicializada:
            self.inicializar_tabla_empleados();
            self.tabla_empleados_inicializada = True

        n_empleados = float(len(self.empleados))
        self.tabla_empleados.setRowCount(n_empleados)

        self.iniciar_barra_progreso("Actualizando tabla de empleados...", n_empleados, 0.1)

        for empleado in self.empleados:
            item_nombre = QtGui.QTableWidgetItem(empleado.nombre)
            item_nombre.setTextAlignment(QtCore.Qt.AlignLeft)
            self.tabla_empleados.setItem(empleado.id, 0, item_nombre)

            item_salario = QtGui.QTableWidgetItem(str(empleado.salario))
            item_salario.setTextAlignment(QtCore.Qt.AlignRight)
            self.tabla_empleados.setItem(empleado.id, 1, item_salario)

            item_cargo = QtGui.QTableWidgetItem(empleado.cargo)
            item_cargo.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tabla_empleados.setItem(empleado.id, 2, item_cargo)

            self.avanzar_barra_progreso(empleado.id+1)

        self.finalizar_barra_progreso("Tabla de empleados actualizada!")

        self.tabla_empleados.resizeColumnsToContents()
        self.tabla_empleados.horizontalHeader().setStretchLastSection(True)

    # Funcion que se encarga de cargar archivo
    def cargar_archivo(self):
        ruta_nomina = QtGui.QFileDialog.getOpenFileName(self, 'Cargar archivo de nomina', '.',
                                                        "Archivos de nomina (*.txt)")
        self.ruta_archivo_nomina.setText(ruta_nomina)

        self.cargar_empleados(ruta_nomina)
        self.actualizar_tabla_empleados()
        self.boton_calcular_nomina.setEnabled(True)

    def calcular_nomina(self):
        print "Calculando nomina..."

        self.nominas_empleados = []
        self.liquidaciones_empleados = []

        self.iniciar_barra_progreso("Calculando nomina para empleados...", len(self.empleados), 0)

        for empleado in self.empleados:
            nomina = self.processor.calcular_nomina(empleado)
            liquidacion = LiquidacionEmpleado(empleado, nomina)
            self.nominas_empleados.append(nomina)
            self.liquidaciones_empleados.append(liquidacion)
            self.avanzar_barra_progreso(empleado.id+1)

        self.finalizar_barra_progreso("Nomina calculada!")

        self.tabla_apropiaciones.setEnabled(True)
        self.tabla_deducciones.setEnabled(True)
        self.tabla_liquidacion.setEnabled(True)
        self.boton_guardar_liquidacion.setEnabled(True)

        self.nomina_calculada = True

    def inicializar_tabla_apropiaciones(self):
        encabezados_tabla_apropiaciones = QtCore.QStringList()
        encabezados_tabla_apropiaciones << "Apropiacion" << "Valor"

        self.tabla_apropiaciones.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.tabla_apropiaciones.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tabla_apropiaciones.setColumnCount(2)
        self.tabla_apropiaciones.verticalHeader().setVisible(False)
        self.tabla_apropiaciones.setHorizontalHeaderLabels(encabezados_tabla_apropiaciones)

        self.tabla_apropiaciones.setRowCount(10)
        self.tabla_apropiaciones.setItem(0, 0, QtGui.QTableWidgetItem("SS - Salud Empresa"))
        self.tabla_apropiaciones.setItem(1, 0, QtGui.QTableWidgetItem("SS - Pension Empresa"))
        self.tabla_apropiaciones.setItem(2, 0, QtGui.QTableWidgetItem("SS - ARL"))
        self.tabla_apropiaciones.setItem(3, 0, QtGui.QTableWidgetItem("AP - Sena"))
        self.tabla_apropiaciones.setItem(4, 0, QtGui.QTableWidgetItem("AP - ICBF"))
        self.tabla_apropiaciones.setItem(5, 0, QtGui.QTableWidgetItem("AP - Cajas"))
        self.tabla_apropiaciones.setItem(6, 0, QtGui.QTableWidgetItem("PS - Cesantias"))
        self.tabla_apropiaciones.setItem(7, 0, QtGui.QTableWidgetItem("PS - Intereses"))
        self.tabla_apropiaciones.setItem(8, 0, QtGui.QTableWidgetItem("PS - Vacaciones"))
        self.tabla_apropiaciones.setItem(9, 0, QtGui.QTableWidgetItem("PS - Prima"))

    def actualizar_tabla_apropiaciones(self, empleado):
        if not self.nomina_calculada:
            print "Calcular nomina primero!"
            return

        if not self.tabla_apropiaciones_inicializada:
            self.inicializar_tabla_apropiaciones();
            self.tabla_apropiaciones_inicializada = True

        apropiacion = self.nominas_empleados[empleado.id].apropiacion

        item_ss_salud_empresa = QtGui.QTableWidgetItem(str(apropiacion.seguridad_social.salud_empresa))
        item_ss_salud_empresa.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_apropiaciones.setItem(0, 1, item_ss_salud_empresa)

        item_ss_pension_empresa = QtGui.QTableWidgetItem(str(apropiacion.seguridad_social.pension_empresa))
        item_ss_pension_empresa.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_apropiaciones.setItem(1, 1, item_ss_pension_empresa)

        item_ss_arl = QtGui.QTableWidgetItem(str(apropiacion.seguridad_social.arl))
        item_ss_arl.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_apropiaciones.setItem(2, 1, item_ss_arl)

        item_ap_sena = QtGui.QTableWidgetItem(str(apropiacion.aporte_parafiscal.sena))
        item_ap_sena.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_apropiaciones.setItem(3, 1, item_ap_sena)

        item_ap_icbf = QtGui.QTableWidgetItem(str(apropiacion.aporte_parafiscal.icbf))
        item_ap_icbf.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_apropiaciones.setItem(4, 1, item_ap_icbf)

        item_ap_cajas = QtGui.QTableWidgetItem(str(apropiacion.aporte_parafiscal.cajas))
        item_ap_cajas.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_apropiaciones.setItem(5, 1, item_ap_cajas)

        item_ps_cesantias = QtGui.QTableWidgetItem(str(apropiacion.prestacion_social.cesantias))
        item_ps_cesantias.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_apropiaciones.setItem(6, 1, item_ps_cesantias)

        item_ps_intereses = QtGui.QTableWidgetItem(str(apropiacion.prestacion_social.interes_cesantias))
        item_ps_intereses.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_apropiaciones.setItem(7, 1, item_ps_intereses)

        item_ps_vacaciones = QtGui.QTableWidgetItem(str(apropiacion.prestacion_social.vacaciones))
        item_ps_vacaciones.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_apropiaciones.setItem(8, 1, item_ps_vacaciones)

        item_ps_prima = QtGui.QTableWidgetItem(str(apropiacion.prestacion_social.prima_servicios))
        item_ps_prima.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_apropiaciones.setItem(9, 1, item_ps_prima)

        self.tabla_apropiaciones.resizeColumnsToContents()
        self.tabla_apropiaciones.horizontalHeader().setStretchLastSection(True)

    def inicializar_tabla_deducciones(self):
        encabezados_tabla_deducciones = QtCore.QStringList()
        encabezados_tabla_deducciones << "Deduccion" << "Valor"

        self.tabla_deducciones.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.tabla_deducciones.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tabla_deducciones.setColumnCount(2)
        self.tabla_deducciones.verticalHeader().setVisible(False)
        self.tabla_deducciones.setHorizontalHeaderLabels(encabezados_tabla_deducciones)

        self.tabla_deducciones.setRowCount(3)
        self.tabla_deducciones.setItem(0, 0, QtGui.QTableWidgetItem("Salud Empleado"))
        self.tabla_deducciones.setItem(1, 0, QtGui.QTableWidgetItem("Pension Empleado"))
        self.tabla_deducciones.setItem(2, 0, QtGui.QTableWidgetItem("Fondo Solidaridad"))

    def actualizar_tabla_deducciones(self, empleado):
        if not self.nomina_calculada:
            print "Calcular nomina primero!"
            return

        if not self.tabla_deducciones_inicializada:
            self.inicializar_tabla_deducciones();
            self.tabla_deducciones_inicializada = True

        deduccion = self.nominas_empleados[empleado.id].deduccion

        item_salud_empleado = QtGui.QTableWidgetItem(str(deduccion.salud_empleado))
        item_salud_empleado.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_deducciones.setItem(0, 1, item_salud_empleado)

        item_pension_empleado = QtGui.QTableWidgetItem(str(deduccion.pension_empleado))
        item_pension_empleado.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_deducciones.setItem(1, 1, item_pension_empleado)

        item_fondo_solidaridad = QtGui.QTableWidgetItem(str(deduccion.aporte_fondo_solidaridad))
        item_fondo_solidaridad.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_deducciones.setItem(2, 1, item_fondo_solidaridad)

        self.tabla_deducciones.resizeColumnsToContents()
        self.tabla_deducciones.horizontalHeader().setStretchLastSection(True)

    def inicializar_tabla_liquidacion(self):
        encabezados_tabla_liquidacion = QtCore.QStringList()
        encabezados_tabla_liquidacion << "Detalle" << "Valor"

        self.tabla_liquidacion.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.tabla_liquidacion.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tabla_liquidacion.setColumnCount(2)
        self.tabla_liquidacion.verticalHeader().setVisible(False)
        self.tabla_liquidacion.setHorizontalHeaderLabels(encabezados_tabla_liquidacion)

        self.tabla_liquidacion.setRowCount(5)
        self.tabla_liquidacion.setItem(0, 0, QtGui.QTableWidgetItem("Total Apropiaciones"))
        self.tabla_liquidacion.setItem(1, 0, QtGui.QTableWidgetItem("Total Deducciones"))
        self.tabla_liquidacion.setItem(2, 0, QtGui.QTableWidgetItem("Auxilio de Transporte"))
        self.tabla_liquidacion.setItem(3, 0, QtGui.QTableWidgetItem("Salario Neto"))
        self.tabla_liquidacion.setItem(4, 0, QtGui.QTableWidgetItem("Costo Empresa"))

    def actualizar_tabla_liquidacion(self, empleado):
        if not self.nomina_calculada:
            print "Calcular nomina primero!"
            return

        if not self.tabla_liquidacion_inicializada:
            self.inicializar_tabla_liquidacion();
            self.tabla_liquidacion_inicializada = True

        liquidacion = self.liquidaciones_empleados[empleado.id]

        item_total_apropiaciones = QtGui.QTableWidgetItem(str(liquidacion.nomina_empleado.apropiacion.total()))
        item_total_apropiaciones.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_liquidacion.setItem(0, 1, item_total_apropiaciones)

        item_total_deducciones = QtGui.QTableWidgetItem(str(liquidacion.nomina_empleado.deduccion.total()))
        item_total_deducciones.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_liquidacion.setItem(1, 1, item_total_deducciones)

        item_auxilio_transporte = QtGui.QTableWidgetItem(str(liquidacion.nomina_empleado.valor_auxilio_transporte))
        item_auxilio_transporte.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_liquidacion.setItem(2, 1, item_auxilio_transporte)

        item_salario_neto = QtGui.QTableWidgetItem(str(liquidacion.salario_neto))
        item_salario_neto.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_liquidacion.setItem(3, 1, item_salario_neto)

        item_costo_empresa = QtGui.QTableWidgetItem(str(liquidacion.costo_empresa))
        item_costo_empresa.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_liquidacion.setItem(4, 1, item_costo_empresa)

        self.tabla_liquidacion.resizeColumnsToContents()
        self.tabla_liquidacion.horizontalHeader().setStretchLastSection(True)

    def empleado_seleccionado(self, selected, deselected):
        cur_index = selected.indexes()[0]
        cur_row = cur_index.row()

        #print "cur_row = " + str(cur_row)
        #print "Selected: " + self.empleados[cur_row].nombre + " - Id: " + str(self.empleados[cur_row].id)

        self.actualizar_tabla_apropiaciones(self.empleados[cur_row])
        self.actualizar_tabla_deducciones(self.empleados[cur_row])
        self.actualizar_tabla_liquidacion(self.empleados[cur_row])

    # Funcion que se encarga de cargar archivo
    def guardar_liquidacion(self):
        ruta_liquidacion = QtGui.QFileDialog.getSaveFileName(self, 'Guardar archivo de liquidacion', '.',
                                                             "Archivos de liquidacion (*.liq)")
        print "Ruta para guardar liquidacion: " + ruta_liquidacion

        self.iniciar_barra_progreso("Guardando liquidaciones ...", 2, 1)
        self.avanzar_barra_progreso(1)
        self.processor.guardar_liquidacion_nomina(self.liquidaciones_empleados, ruta_liquidacion)
        self.avanzar_barra_progreso(2)
        self.finalizar_barra_progreso("Liquidaciones guardadas!")