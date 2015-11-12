class ConfiguracionNomina():
    def __init__(self, nombre_archivo_errores, nombre_archivo_registro, nombre_archivo_liquidacion,
                 numero_minimo_lineas, smlv, auxilio_transporte, tope_auxilio_transporte, tope_fondo_solidaridad,
                 porcentaje_fondo_solidaridad, porcentaje_arl):
        self.nombre_archivo_errores = nombre_archivo_errores
        self.nombre_archivo_registro = nombre_archivo_registro
        self.nombre_archivo_liquidacion = nombre_archivo_liquidacion
        self.numero_minimo_lineas = numero_minimo_lineas
        self.smlv = smlv
        self.auxilio_transporte = auxilio_transporte
        self.tope_auxilio_transporte = tope_auxilio_transporte
        self.tope_fondo_solidaridad = tope_fondo_solidaridad
        self.porcentaje_fondo_solidaridad = porcentaje_fondo_solidaridad
        self.porcentaje_arl = porcentaje_arl
