from collections import Set
from django.views.generic import DetailView

from shop.models.product import Product, get_price
from tecdoc.models import PartAnalog, get_part_analogs, clean_number, Part


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = context['product']
        try:
            group_id = self.request.user.groups.all()[0].id
        except Exception:
            group_id = None
        product.price = get_price(product, group_id)
        product.default_price = get_price(product)
        part_analogs = PartAnalog.objects.filter(search_number=clean_number(product.sku))
        product.title = Part.objects.filter(sku=product.sku, supplier__title=product.brand)[0].designation
        parts = set()
        sku = []
        for pa in part_analogs:
            parts.add(pa.part)
            sku.append(pa.part.sku)
        products = Product.objects.filter(sku__in=sku)

        for part in parts:
            brand_name = part.supplier.title
            # sku = part.sku
            for prod in products:
                if clean_number(part.sku) == clean_number(prod.sku) and brand_name == prod.brand:
                    part.price = get_price(prod, group_id)
                    part.product_id = prod.id
                    part.quantity = prod.get_quantity()
            if not hasattr(part, 'price'):
                part.price = -1

        parts = sorted(parts, key=lambda part: part.price, reverse=True)
        # product.name = parts[0].title
        context['part_analogs'] = parts
        return context
