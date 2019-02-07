from modeltranslation.translator import translator, TranslationOptions

from market.models import Product


class ProductTranslationOptions(TranslationOptions):
    fields = ('name',
              'description',
              'short_description',
              'image',
              'packaging',
              'shelf_life',
              'storage_conditions',
              'ingredients',
              'using'
              )


translator.register(Product, ProductTranslationOptions)
