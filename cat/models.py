from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Sum


def nth_separator(n, text):
    data = [text[i:i + n] for i in range(0, len(text), n)]
    return ' '.join(data)


class Archivo(models.Model):
    file = models.FileField(upload_to='archivos/')


class Tarjeta(models.Model):
    TABLE_HEADERS = [
        {
            'display': 'Owner',
            'name': 'owner_name',
        }, {
            'display': 'RFC',
            'name': 'rfc'
        }, {
            'display': 'Numero',
            'name': 'numero'
        }, {
            'display': 'Banco',
            'name': 'banco'
        }, {
            'display': 'Balance',
            'name': 'balance'
        },
    ]
    owner = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)
    rfc = models.CharField(max_length=15, null=True, blank=False)
    numero = models.CharField(max_length=16)
    banco = models.CharField(max_length=25)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=15)

    def actions(self):
        actions = []
        if self.movimientos_disponibles().exists():
            actions.append({
                'name': 'refresh',
                'class': 'fa fa-refresh',
                'button_class': 'btn btn-info'
            })
        else:
            actions.append({
                'name': 'delete',
                'class': 'fa fa-times',
                'button_class': 'btn btn-danger'
            })
        return actions

    def __str__(self):
        return '{}|{}|{}'.format(self.numero[-4:], self.banco, self.balance)

    def get_tarjeta_display(self):
        return nth_separator(4, self.numero)

    def define_balance(self):
        ingresos = Movimiento.objects.filter(tipo=Movimiento.INGRESO).aggregate(total=Sum('cantidad'))['total']
        egresos = Movimiento.objects.filter(tipo=Movimiento.EGRESO).aggregate(total=Sum('cantidad'))['total']
        self.balance = (ingresos or 0) - (egresos or 0)
        self.save()

    def pagos_disponibles(self):
        return self.pagos_pendientes.exclude(estatus=PagoPendiente.PAGADO)

    def movimientos_disponibles(self):
        return self.movimiento_set.all().order_by('-fecha')


class Movimiento(models.Model):
    TABLE_HEADERS = [
        {
            'display': 'Tipo',
            'name': 'get_tipo_display',
        }, {
            'display': 'Monto a pagar',
            'name': 'cantidad_original'
        }, {
            'display': 'Moneda',
            'name': 'moneda_display'
        }, {
            'display': 'Monto pagado',
            'name': 'cantidad'
        }, {
            'display': 'Concepto',
            'name': 'concepto'
        }, {
            'display': 'Adjuntos',
            'name': 'adjunto',
            'type': 'modal'
        },
    ]
    INGRESO = 0
    EGRESO = 1

    TIPOS_MOVIMIENTO = (
        (INGRESO, 'Ingreso'),
        (EGRESO, 'Egreso'),
    )

    abono_pendiente = models.ForeignKey('cat.AbonoPendiente', on_delete=models.SET_NULL, null=True, blank=True)
    moneda = models.ForeignKey('cat.Moneda', on_delete=models.SET_NULL, null=True, blank=False)
    cantidad_original = models.DecimalField(default=0, decimal_places=2, max_digits=15, verbose_name='Monto a pagar')
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, null=False, blank=False)
    cantidad = models.DecimalField(default=0, decimal_places=2, max_digits=15, verbose_name='Monto pagado')
    tipo = models.SmallIntegerField(choices=TIPOS_MOVIMIENTO, default=INGRESO)
    adjunto = models.ForeignKey('cat.Archivo', null=True, blank=True, on_delete=models.SET_NULL)
    concepto = models.CharField(max_length=250, null=True, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def actions(self):
        acciones = [{
            'name': 'refresh',
            'class': 'fa fa-refresh',
            'button_class': 'btn btn-info',
        }]
        return acciones

    def define_cantidad(self):
        mxn = Moneda.objects.get(nombre_corto__iexact='mxn')
        try:
            conversion = Conversion.objects.get(moneda_origen=self.moneda, moneda_objetivo=mxn)
            cantidad = conversion.perform_conversion(self.cantidad_original)
        except Conversion.DoesNotExist:
            try:
                conversion = Conversion.objects.get(moneda_origen=mxn, moneda_objetivo=self.moneda)
                cantidad = conversion.perform_conversion_inverse(self.cantidad_original)
            except Conversion.DoesNotExist:
                cantidad = self.cantidad_original

        self.cantidad = cantidad

    def save(self, *args, **kwargs):
        self.define_cantidad()
        super(Movimiento, self).save(*args, **kwargs)
        self.tarjeta.define_balance()
        return self


class PagoPendiente(models.Model):
    TABLE_HEADERS = [{
        'display': 'Monto a pagar',
        'name': 'cantidad_original'
    }, {
        'display': 'Moneda',
        'name': 'moneda_display'
    }, {
        'display': 'Concepto',
        'name': 'concepto'
    }, {
        'display': 'Automatico',
        'name': 'pago_automatico'
    }, {
        'display': 'Estatus',
        'name': 'get_estatus_display',
    },
    ]
    PENDIENTE = 0
    PAGADO = 1
    PROGRAMADO = 2

    ESTADOS = (
        (PENDIENTE, 'Pendiente'),
        (PAGADO, 'Pagado'),
        (PROGRAMADO, 'Programado'),
    )

    def actions(self):
        actions = [{
            'name': 'pagar',
            'class': 'fa fa-credit-card',
            'button_class': 'btn btn-success',
            'type': 'modal',
        }]
        return actions

    moneda = models.ForeignKey('cat.Moneda', on_delete=models.SET_NULL, null=True, blank=False)
    cantidad_original = models.DecimalField(default=0, decimal_places=2, max_digits=15, verbose_name='Monto a pagar')
    estatus = models.SmallIntegerField(choices=ESTADOS, default=PENDIENTE)
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, null=False, blank=False,
                                related_name='pagos_pendientes')
    concepto = models.CharField(max_length=250, null=True, blank=False)
    programacion = models.CharField(max_length=10)
    pago_automatico = models.BooleanField(default=False)
    periodicidad = models.CharField(max_length=5)
    pago_unico = models.BooleanField(default=False)

    @property
    def cantidad(self):
        mxn = Moneda.objects.get(nombre_corto__iexact='mxn')
        try:
            conversion = Conversion.objects.get(moneda_origen=self.moneda, moneda_objetivo=mxn)
            cantidad = conversion.perform_conversion(self.cantidad_original)
        except Conversion.DoesNotExist:
            try:
                conversion = Conversion.objects.get(moneda_origen=mxn, moneda_objetivo=self.moneda)
                cantidad = conversion.perform_conversion_inverse(self.cantidad_original)
            except Conversion.DoesNotExist:
                cantidad = self.cantidad_original

        return cantidad

    def pagar(self):
        movimiento = Movimiento(
            tarjeta=self.tarjeta,
            cantidad_original=self.cantidad_original,
            moneda=self.moneda,
            concepto=self.concepto,
            tipo=Movimiento.EGRESO
        )
        return movimiento


class Moneda(models.Model):
    nombre = models.CharField(max_length=20)
    nombre_corto = models.CharField(max_length=5)

    def __str__(self):
        return self.nombre_corto


class Conversion(models.Model):
    moneda_origen = models.ForeignKey(Moneda, on_delete=models.CASCADE, related_name='conversiones_origen')
    moneda_objetivo = models.ForeignKey(Moneda, on_delete=models.CASCADE, related_name='conversiones_objetivo')
    factor = models.DecimalField(decimal_places=10, max_digits=15)

    def perform_conversion(self, cantidad_original):
        return cantidad_original * self.factor

    def perform_conversion_inverse(self, cantidad_original):
        return cantidad_original / self.factor

    class Meta:
        unique_together = ['moneda_objetivo', 'moneda_origen']


class AbonoPendiente(models.Model):
    TABLE_HEADERS = [{
        'display': 'Monto a pagar',
        'name': 'cantidad_original'
    }, {
        'display': 'Moneda',
        'name': 'moneda_display'
    }, {
        'display': 'Concepto',
        'name': 'concepto'
    }, {
        'display': 'Automatico',
        'name': 'pago_automatico'
    }, {
        'display': 'Estatus',
        'name': 'get_estatus_display',
    },
    ]
    PENDIENTE = 0
    PAGADO = 1
    PROGRAMADO = 2

    ESTADOS = (
        (PENDIENTE, 'Pendiente'),
        (PAGADO, 'Pagado'),
        (PROGRAMADO, 'Programado'),
    )

    def actions(self):
        pass

    moneda = models.ForeignKey('cat.Moneda', on_delete=models.SET_NULL, null=True, blank=False)
    cantidad_original = models.DecimalField(default=0, decimal_places=2, max_digits=15, verbose_name='Monto a pagar')
    estatus = models.SmallIntegerField(choices=ESTADOS, default=PENDIENTE)
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, null=False, blank=False,
                                related_name='abonos_pendientes')
    concepto = models.CharField(max_length=250, null=True, blank=False)
    programacion = models.CharField(max_length=10)
    pago_automatico = models.BooleanField(default=False)
    periodicidad = models.CharField(max_length=5)
    pago_unico = models.BooleanField(default=False)
    parcializable = models.BooleanField(default=False)
