class Empleado():
	def __init__(self, id, nombre, salario, cargo):
		self.id = id
		self.nombre = nombre
		self.salario = salario
		self.cargo = cargo

class Deduccion():
	def __init__(self, salud_empleado, pension_empleado, aporte_fondo_solidaridad):
		self.salud_empleado = salud_empleado
		self.pension_empleado = pension_empleado
		self.aporte_fondo_solidaridad = aporte_fondo_solidaridad

class SeguridadSocial():
	def __init__(self, salud_empresa, pension_empresa, arl):
		self.salud_empresa = salud_empresa
		self.pension_empresa = pension_empresa
		self.arl = arl

class AporteParafiscal():
	def __init__(self, sena, icbf, cajas):
		self.sena = sena
		self.icbf = icbf
		self.cajas = cajas

class PrestacionSocial():
	def __init__(self, cesantias, interes_cesantias, prima_servicios, vacaciones):
		self.cesantias = cesantias
		self.interes_cesantias = interes_cesantias
		self.prima_servicios = prima_servicios
		self.vacaciones = vacaciones
		
class Apropiacion():
	def __init__(self, seguridad_social, aporte_parafiscal, prestacion_social):
		self.seguridad_social = seguridad_social
		self.aporte_parafiscal = aporte_parafiscal
		self.prestacion_social = prestacion_social
		
class NominaEmpleado():
	def __init__(self, apropiacion, deduccion, valor_auxilio_transporte):
		self.apropiacion = apropiacion
		self.deduccion = deduccion
		self.valor_auxilio_transporte = valor_auxilio_transporte
		
class LiquidacionEmpleado():
	def __init__(self, empleado, nomina_empleado):
		self.empleado = empleado
		self.nomina_empleado = nomina_empleado

	def salario_neto():
		pass
		
	def costo_empresa():
		pass