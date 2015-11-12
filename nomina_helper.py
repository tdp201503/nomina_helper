from PyQt4 import QtGui, QtCore
from nomina_helper_gui import Ui_MainWindow

class NominaHelper(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self, configuracion_por_defecto):
		super(self.__class__, self).__init__()
		self.setupUi(self)
		self.configuracion_nomina = configuracion_por_defecto
		
		# Conexion de signals & slots
		#self.boton_cargar_archivo.clicked.connect(self.cargar_archivo)
		self.connect(self.boton_cargar_archivo, QtCore.SIGNAL("clicked()"), self.cargar_archivo)
		self.boton_guardar_liquidacion.clicked.connect(self.guardar_liquidacion)
		self.boton_calcular_nomina.clicked.connect(self.calcular_nomina)
		self.boton_abrir.clicked.connect(self.saludar)
		
		encabezados_tabla_empleados = QtCore.QStringList()
		encabezados_tabla_empleados << "Nombre" << "Salario" << "Cargo"
		
		self.tabla_empleados.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tabla_empleados.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.tabla_empleados.setColumnCount(3)
		self.tabla_empleados.setColumnWidth(0, 250)
		self.tabla_empleados.setColumnWidth(1, 120)
		self.tabla_empleados.setColumnWidth(2, 200)
		self.tabla_empleados.setHorizontalHeaderLabels(encabezados_tabla_empleados)
		
		self.tabla_empleados.selectionModel().selectionChanged.connect(self.empleado_seleccionado)
		#self.connect(self.tabla_empleados.selectionModel(), QtCore.SIGNAL("selectionChanged()"), self.empleado_seleccionado)
		
		encabezados_tabla_apropiaciones = QtCore.QStringList()
		encabezados_tabla_apropiaciones << "Apropiacion" << "Valor"
		
		self.tabla_apropiaciones.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tabla_apropiaciones.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.tabla_apropiaciones.setColumnCount(2)
		self.tabla_apropiaciones.verticalHeader().setVisible(False)
		self.tabla_apropiaciones.setHorizontalHeaderLabels(encabezados_tabla_apropiaciones)
		
		encabezados_tabla_deducciones = QtCore.QStringList()
		encabezados_tabla_deducciones << "Deduccion" << "Valor"
		
		self.tabla_deducciones.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tabla_deducciones.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.tabla_deducciones.setColumnCount(2)
		self.tabla_deducciones.verticalHeader().setVisible(False)
		self.tabla_deducciones.setHorizontalHeaderLabels(encabezados_tabla_deducciones)
		
		encabezados_tabla_liquidacion = QtCore.QStringList()
		encabezados_tabla_liquidacion << "Elemento" << "Valor"
		
		self.tabla_liquidacion.setSelectionMode(QtGui.QTableView.SingleSelection)
		self.tabla_liquidacion.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.tabla_liquidacion.setColumnCount(2)
		self.tabla_liquidacion.verticalHeader().setVisible(False)
		self.tabla_liquidacion.setHorizontalHeaderLabels(encabezados_tabla_liquidacion)
	
	# Funcion que se encarga de cargar archivo
	def cargar_archivo(self):
		ruta_nomina = QtGui.QFileDialog.getOpenFileName(self, 'Cargar archivo de nomina','.', "Archivos de nomina (*.txt);;Archivo de imagen (*.png *.jpg *.gif *.jpeg)")
		self.ruta_archivo_nomina.setText(ruta_nomina)
		
		archivo_nomina = open(ruta_nomina, 'r')	
		self.empleados = archivo_nomina.readlines()
		
		print "Leyendo empleados ..."
		
		n_empleados = len(self.empleados)
		self.tabla_empleados.setRowCount(n_empleados)
		
		for i in range(n_empleados):
			# Eliminar el \n al final
			empleado = self.empleados[i].strip()
			#print "Leyendo empleado " + str(i) + ": " + empleado
			campos_empleado = empleado.split("*")
			
			item_nombre = QtGui.QTableWidgetItem(campos_empleado[0])
			item_nombre.setTextAlignment(QtCore.Qt.AlignLeft)
			self.tabla_empleados.setItem(i, 0, item_nombre)
			
			item_salario = QtGui.QTableWidgetItem(campos_empleado[1])
			item_salario.setTextAlignment(QtCore.Qt.AlignRight)
			self.tabla_empleados.setItem(i, 1, item_salario)
			
			item_cargo = QtGui.QTableWidgetItem(campos_empleado[2])
			item_cargo.setTextAlignment(QtCore.Qt.AlignHCenter)
			self.tabla_empleados.setItem(i, 2, item_cargo)
		
		self.tabla_empleados.resizeColumnsToContents()
		self.tabla_empleados.horizontalHeader().setStretchLastSection(True)
	
	def calcular_nomina(self):
		print "Calculando nomina..."
		
	def empleado_seleccionado(self, selected, deselected):
		cur_index = selected.indexes()[0]
		cur_row = cur_index.row()
		
		print "cur_row = " + str(cur_row)
		print "Selected: " + self.empleados[cur_row]
		
		empleado = self.empleados[cur_row].strip()
		campos_empleado = empleado.split("*")
		
		self.tabla_apropiaciones.setRowCount(10)
		
		self.tabla_apropiaciones.setItem(0, 0, QtGui.QTableWidgetItem("SS - Salud Empresa"))
		item_ss_salud_empresa = QtGui.QTableWidgetItem(str(cur_row))
		item_ss_salud_empresa.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
		self.tabla_apropiaciones.setItem(0, 1, item_ss_salud_empresa)
		
		self.tabla_apropiaciones.setItem(1, 0, QtGui.QTableWidgetItem("SS - Pension Empresa"))
		item_ss_pension_empresa = QtGui.QTableWidgetItem(str(cur_row))
		item_ss_pension_empresa.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
		self.tabla_apropiaciones.setItem(1, 1, item_ss_pension_empresa)
		
		self.tabla_apropiaciones.setItem(2, 0, QtGui.QTableWidgetItem("SS - ARL"))
		item_ss_arl = QtGui.QTableWidgetItem(str(cur_row))
		item_ss_arl.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
		self.tabla_apropiaciones.setItem(2, 1, item_ss_arl)
		
		self.tabla_apropiaciones.setItem(3, 0, QtGui.QTableWidgetItem("AP - Sena"))
		item_ap_sena = QtGui.QTableWidgetItem(str(cur_row))
		item_ap_sena.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
		self.tabla_apropiaciones.setItem(3, 1, item_ap_sena)
		
		self.tabla_apropiaciones.setItem(4, 0, QtGui.QTableWidgetItem("AP - ICBF"))
		item_ap_icbf = QtGui.QTableWidgetItem(str(cur_row))
		item_ap_icbf.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
		self.tabla_apropiaciones.setItem(4, 1, item_ap_icbf)
		
		self.tabla_apropiaciones.setItem(5, 0, QtGui.QTableWidgetItem("AP - Cajas"))
		item_ap_cajas = QtGui.QTableWidgetItem(str(cur_row))
		item_ap_cajas.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
		self.tabla_apropiaciones.setItem(5, 1, item_ap_cajas)
		
		self.tabla_apropiaciones.setItem(6, 0, QtGui.QTableWidgetItem("PS - Cesantias"))
		item_ps_cesantias = QtGui.QTableWidgetItem(str(cur_row))
		item_ps_cesantias.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
		self.tabla_apropiaciones.setItem(6, 1, item_ps_cesantias)
		
		self.tabla_apropiaciones.setItem(7, 0, QtGui.QTableWidgetItem("PS - Intereses"))
		item_ps_intereses = QtGui.QTableWidgetItem(str(cur_row))
		item_ps_intereses.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
		self.tabla_apropiaciones.setItem(7, 1, item_ps_intereses)
		
		self.tabla_apropiaciones.setItem(8, 0, QtGui.QTableWidgetItem("PS - Vacaciones"))
		item_ps_vacaciones = QtGui.QTableWidgetItem(str(cur_row))
		item_ps_vacaciones.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
		self.tabla_apropiaciones.setItem(8, 1, item_ps_vacaciones)
		
		self.tabla_apropiaciones.setItem(9, 0, QtGui.QTableWidgetItem("PS - Prima"))
		item_ps_prima = QtGui.QTableWidgetItem(str(cur_row))
		item_ps_prima.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
		self.tabla_apropiaciones.setItem(9, 1, item_ps_prima)
		
		self.tabla_apropiaciones.resizeColumnsToContents()
		self.tabla_apropiaciones.horizontalHeader().setStretchLastSection(True)
		
	# Funcion que se encarga de cargar archivo
	def guardar_liquidacion(self):
		ruta_liquidacion = QtGui.QFileDialog.getSaveFileName(self, 'Guardar archivo de liquidacion','.', "Archivos de liquidacion (*.liq)")
		print "Ruta para guardar liquidacion: " + ruta_liquidacion
		
	def saludar(self):
		text,ok = QtGui.QInputDialog.getText(self, 'Dialogo Entrada', 'Ingrese su nombre:')
		
		if ok:
			self.mensaje_progreso.setText("Hola " + str(text) + "!")