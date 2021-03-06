from distutils.command.clean import clean

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin

from shop.models.product import Product, clean_number, get_analogs, get_products, ProductTypes
from tecdoc.models import Part, Q, PartAnalog, PartCross, Supplier, PartProduct
import urllib.parse


class SearchView(TemplateView):
    template_name = 'shop/search_page.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data()
        query = self.request.GET['q']
        clean_query = clean_number(query)
        parts = Part.objects.filter(clean_part_number=clean_query)
        additional_products = Product.get_additional_products(sku=clean_query)
        context.update({
            'q': query,
            'parts': parts,
            'additional_products': additional_products
        })
        return context


class SearchDetailView(ListView):
    template_name = 'shop/search_detail_page.html'
    context_object_name = 'partproduct_list'

    def get_queryset(self):
        part_number = self.request.GET['part']
        clean_part_number = clean_number(part_number)

        brand = self.request.GET['brand']
        supplier = Supplier.objects.get(title=brand)

        analogs = get_analogs(clean_part_number=clean_part_number, supplier=supplier, user=self.request.user)
        if analogs:
            return analogs

        # if we are here, than we have not analogs, try to search directly in productss
        return get_products(supplier=supplier, clean_part_number=clean_part_number)

    def get_context_data(self, **kwargs):
        context = super(SearchDetailView, self).get_context_data()
        part_number = self.request.GET['part']
        brand = self.request.GET['brand']
        context['part_number'] = part_number
        context['brand'] = brand
        return context
