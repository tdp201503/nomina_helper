class Empleado:
    def __init__(self, id, nombre, salario, cargo):
        self.id = id
        self.nombre = nombre
        self.salario = float(salario)
        self.cargo = cargo


class Deduccion:
    def __init__(self, salud_empleado, pension_empleado, aporte_fondo_solidaridad):
        self.salud_empleado = float(salud_empleado)
        self.pension_empleado = float(pension_empleado)
        self.aporte_fondo_solidaridad = float(aporte_fondo_solidaridad)

    def total(self):
        return self.salud_empleado + self.pension_empleado + self.aporte_fondo_solidaridad


class SeguridadSocial:
    def __init__(self, salud_empresa, pension_empresa, arl):
        self.salud_empresa = float(salud_empresa)
        self.pension_empresa = float(pension_empresa)
        self.arl = float(arl)

    def total(self):
        return self.salud_empresa + self.pension_empresa + self.arl


class AporteParafiscal:
    def __init__(self, sena, icbf, cajas):
        self.sena = float(sena)
        self.icbf = float(icbf)
        self.cajas = float(cajas)

    def total(self):
        return self.sena + self.icbf + self.cajas


class PrestacionSocial:
    def __init__(self, cesantias, interes_cesantias, prima_servicios, vacaciones):
        self.cesantias = float(cesantias)
        self.interes_cesantias = float(interes_cesantias)
        self.prima_servicios = float(prima_servicios)
        self.vacaciones = float(vacaciones)

    def total(self):
        return self.cesantias + self.interes_cesantias + self.prima_servicios + self.vacaciones


class Apropiacion:
    def __init__(self, seguridad_social, aporte_parafiscal, prestacion_social):
        self.seguridad_social = seguridad_social
        self.aporte_parafiscal = aporte_parafiscal
        self.prestacion_social = prestacion_social

    def total(self):
        return self.seguridad_social.total() + self.aporte_parafiscal.total() + self.prestacion_social.total()


class NominaEmpleado:
    def __init__(self, apropiacion, deduccion, valor_auxilio_transporte):
        self.apropiacion = apropiacion
        self.deduccion = deduccion
        self.valor_auxilio_transporte = valor_auxilio_transporte


class LiquidacionEmpleado:
    def __init__(self, empleado, nomina_empleado):
        self.empleado = empleado
        self.nomina_empleado = nomina_empleado
        self.salario_neto = empleado.salario - nomina_empleado.deduccion.total() + nomina_empleado.valor_auxilio_transporte
        self.costo_empresa = empleado.salario + nomina_empleado.apropiacion.total() + nomina_empleado.valor_auxilio_transporte
