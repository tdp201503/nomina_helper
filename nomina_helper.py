from PyQt4 import QtGui, QtCore
from nomina_helper_gui import Ui_MainWindow
from modelo.nomina import *
from nomina_helper_processor import NominaHelperProcessor


class NominaHelper(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, configuracion_por_defecto):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.configuracion_nomina = configuracion_por_defecto
        self.processor = NominaHelperProcessor(configuracion_por_defecto)
        self.empleados = []
        self.nominas_empleados = []

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

        self.tabla_empleados.setRowCount(len(self.empleados))

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

        for empleado in self.empleados:
            self.nominas_empleados.append(self.processor.calcular_nomina(empleado))

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

    def empleado_seleccionado(self, selected, deselected):
        cur_index = selected.indexes()[0]
        cur_row = cur_index.row()

        print "cur_row = " + str(cur_row)
        print "Selected: " + self.empleados[cur_row].nombre + " - Id: " + str(self.empleados[cur_row].id)

        self.actualizar_tabla_apropiaciones(self.empleados[cur_row])

    # Funcion que se encarga de cargar archivo
    def guardar_liquidacion(self):
        ruta_liquidacion = QtGui.QFileDialog.getSaveFileName(self, 'Guardar archivo de liquidacion', '.',
                                                             "Archivos de liquidacion (*.liq)")
        print "Ruta para guardar liquidacion: " + ruta_liquidacion