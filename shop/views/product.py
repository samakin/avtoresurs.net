from collections import Set
from django.views.generic import DetailView

from shop.models.product import Product
from tecdoc.models import PartAnalog, get_part_analogs, clean_number


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)

        product = context['product']
        part_analogs = PartAnalog.objects.filter(search_number=clean_number(product.cross_sku))

        parts = set()
        sku = []
        for pa in part_analogs:
            parts.add(pa.part)
            sku.append(pa.part.sku)
        products = Product.objects.filter(sku__in=sku)

        for part in parts:
            brand_name_small = part.supplier.title.lower()
            sku_small = part.sku.lower()
            for product in products:
                if sku_small == product.sku and brand_name_small == product.manufacturer:
                    part.price = product.get_price()
                    part.product_id = product.id
                    part.quantity = product.get_quantity()
            if not hasattr(part, 'price'):
                part.price = -1

        parts = sorted(parts, key=lambda part: part.price, reverse=True)

        context['part_analogs'] = parts
        return context
