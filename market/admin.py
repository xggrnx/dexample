from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Price, Country, Product, Domain


class PriceInline(admin.TabularInline):
    model = Price
    fields = ['quantity', 'cost']
    extra = 1


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    model = Country
    fields = ['name', 'code', 'language_locale', 'currency_code']


@admin.register(Product)
class ProductAdmin(TabbedTranslationAdmin):
    model = Product
    group_fieldsets = True
    fields = ['ext_id',
              'country',
              'name',
              'description',
              'short_description',
              'image',
              'packaging',
              'shelf_life',
              'storage_conditions',
              'ingredients',
              'using']

    inlines = [PriceInline, ]
    list_filter = ['country']
    search_fields = ['ext_id']


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    model = Domain
    fields = ('country', 'domain')
    ordering = ('domain',)

