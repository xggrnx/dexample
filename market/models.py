from django.db import models
from django.http.request import split_domain_port


class Price(models.Model):
    product = models.ForeignKey('Product', verbose_name='Товар',
                                related_name='price_product')
    quantity = models.PositiveIntegerField(verbose_name='Количество товара', null=False, blank=False)
    cost = models.DecimalField(verbose_name='Стоимость товара', max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Сетка цен'
        verbose_name_plural = 'Сетки цен'
        ordering = ['quantity']


class Country(models.Model):
    name = models.CharField(verbose_name='Название страны', max_length=128, null=False)
    code = models.CharField(verbose_name='Код страны', max_length=8, null=False)
    language_locale = models.CharField(verbose_name='Код языка', max_length=16, null=False)
    currency_code = models.CharField(verbose_name='Код валюты', max_length=8, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['name']


class Product(models.Model):
    country = models.ForeignKey('Country', verbose_name='Страна', related_name='products_country')
    ext_id = models.CharField(verbose_name='Внешний ключ', max_length=128, null=False)
    name = models.CharField(verbose_name='Название', max_length=256, null=True, blank=False)
    description = models.TextField(verbose_name='Полное описание', null=True, blank=False)
    short_description = models.TextField(verbose_name='Короткое описание', null=True, blank=False)
    image = models.ImageField(verbose_name='Изображение', null=True, blank=False)
    packaging = models.CharField(verbose_name='Упаковка', max_length=256, null=True, blank=False)
    shelf_life = models.CharField(verbose_name='Срок годности', max_length=256, null=True, blank=False)
    storage_conditions = models.CharField(verbose_name='Условия хранения', max_length=256, null=True, blank=False)
    ingredients = models.CharField(verbose_name='Состав', max_length=256, null=True, blank=False)
    using = models.CharField(verbose_name='Применение', max_length=256, null=True, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


DOMAINS_CACHE = {}


class DomainManager(models.Manager):
    use_in_migrations = True

    def _get_domain_by_id(self, domain_id):
        if domain_id not in DOMAINS_CACHE:
            domain = self.get(pk=domain_id)
            DOMAINS_CACHE[domain_id] = domain
        return DOMAINS_CACHE[domain_id]

    def _get_domain_by_request(self, request):
        host = request.get_host()
        try:
            if host not in DOMAINS_CACHE:
                DOMAINS_CACHE[host] = self.get(domain__iexact=host)
            return DOMAINS_CACHE[host]
        except Domain.DoesNotExist:
            domain, port = split_domain_port(host)
            if domain not in DOMAINS_CACHE:
                DOMAINS_CACHE[domain] = self.get(domain__iexact=domain)
            return DOMAINS_CACHE[domain]

    def get_current(self, request=None, domain_id=None):
        if domain_id:
            return self._get_domain_by_id(domain_id)
        elif request:
            return self._get_domain_by_request(request)

    def clear_cache(self):
        global DOMAINS_CACHE
        DOMAINS_CACHE = {}

    def get_by_natural_key(self, domain):
        return self.get(domain=domain)


class Domain(models.Model):
    country = models.ForeignKey('Country', verbose_name='Страна', related_name='domain_country', null=True, blank=False)
    domain = models.CharField(max_length=128)

    objects = DomainManager()

    def __str__(self):
        return self.domain

    class Meta:
        verbose_name = 'Домен'
        verbose_name_plural = 'Домены'

