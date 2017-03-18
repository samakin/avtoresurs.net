import datetime
import os
import threading

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.http import HttpResponseRedirect

# Create your views here.
from django.views.generic import TemplateView

from shop.models.product import clean_number, Product, ProductPrice
from tecdoc.models import PartAnalog


def add(data, interval, report_product, report_price):
    for idx, line in enumerate(data[interval[0]:interval[1]]):
        line_number = idx + interval[0] + 1
        # try:
        row = line.split(';')
        # print(row)
        # exit()
        part_analog = None
        brand = row[1]
        sku = row[0]
        quantity = row[2]
        prices = [row[3], row[4], row[5], row[6], row[7]]
        if not prices[4]:
            prices[4] = 0
        # print(prices)
        clean_sku = clean_number(sku)
        part_analog = PartAnalog.objects.filter(search_number=clean_sku)
        product, created = Product.objects.get_or_create(sku=sku, brand=brand)
        product.quantity = quantity
        product.save()

        product_price = ProductPrice(
            product=product,
            retail_price=prices[0],
            price_1=prices[1],
            price_2=prices[2],
            price_3=prices[3],
            price_4=prices[4]
        )
        # product_price, created = ProductPrice.objects.get_or_create(product=product)
        # product_price.retail_price = prices[0]
        # product_price.price_1 = prices[1]
        # product_price.price_2 = prices[2]
        # product_price.price_3 = prices[3]
        # product_price.price_4 = prices[4]
        # print(product_price)
        product_price.save()

        if not prices[0]:
            report_price.append('Строка № %s не указана цена товара. [%s]' % (line_number, line))
        if not part_analog:
            report_product.append(
                'Строка № %s не найдено соответсвие в TECDOC. [%s]' % (line_number, line.split()))
            # except:
            #     report_product.append('Строка № %s КРИТИЧЕСКАЯ ОШИБКА. [%s]' % (line_number, line.split()))


def get_intervals(interval, THREADS, end_idx):
    intervals = list()
    intervals.append([1, interval])
    for idx in range(1, THREADS + 1):
        intervals.append([interval * idx, interval * (idx + 1)])
    intervals[0][0] = 1
    intervals[THREADS - 1][1] = end_idx
    return intervals


class ProductLoader(TemplateView):
    template_name = 'service/load_product.html'

    # def get(self, request):
    #     pass

    def post(self, request):
        # file = 'NewsAuto2.csv'
        # with open(file, 'r', encoding='cp1251') as fin:
        #     data = fin.read().splitlines(True)
        # date = datetime.datetime.now()

        try:
            file = self.request.FILES['file']
        except KeyError as ke:
            return HttpResponseRedirect('/profile/point_load/')

        date = datetime.datetime.now()
        year = date.strftime('%Y')
        month = date.strftime('%m')

        filename = os.path.join('csv', 'auto', year, month, self.request.FILES['file'].name)
        path = default_storage.save(filename, ContentFile(file.read()))
        file.close()

        with open('media/' + path, 'r', encoding='cp1251') as fin:
            data = fin.read().splitlines(True)

        report_product_str = 'Прококол загрузки файла товаров от %s\r\n' % date
        report_product = list()
        report_price_str = 'Прококол загрузки цен от %s\r\n' % date
        report_price = list()

        # print(data[0:50])
        # exit()

        THREADS = 40
        list_len = len(data)
        interval = list_len // THREADS
        intervals = get_intervals(interval, THREADS, list_len)

        # print(intervals[0])
        # add(data, intervals[0], report_product, report_price)


        threads = list()
        for interval in intervals:
            thread = threading.Thread(target=add, args=(data, interval, report_product, report_price))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        error_file_path = os.path.join('reports', 'auto', date.strftime('%Y'), date.strftime('%m'), 'error_product.log')
        for item in report_product:
            report_product_str += '\r\n%s' % item
        default_storage.save(error_file_path, ContentFile(report_product_str))

        error_price_file_path = os.path.join('reports', 'auto', date.strftime('%Y'), date.strftime('%m'),
                                             'error_price.log')
        for item in report_price:
            report_price_str += '\r\n%s' % item
        default_storage.save(error_price_file_path, ContentFile(report_price_str))
        # with open(error_file_path, 'w+') as error_file:
        #     for item in report_product:
        #         error_file.write('\r\n%s' % item)

        # error_file_price_path = 'error_price.log'
        # with open(error_file_price_path, 'w+') as error_file_price:
        #     for item in report_price:
        #         error_file_price.write('\r\n%s' % item)

        return HttpResponse('OK')
