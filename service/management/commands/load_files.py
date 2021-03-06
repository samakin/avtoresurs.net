from io import BytesIO
from ftplib import FTP

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from avtoresurs_new.settings import HOST, USER, PASSWD
from shop.models.storage import Storage

from service.parser.bonus import BonusLoader
from service.parser.parser import get_filename

from service.parser.point import PointLoader
from service.parser.product import ProductLoader

filenames = ['Klients.csv', 'Priz.csv']

storages = Storage.objects.filter(active=True, active_file_upload=True)
for storage in storages:
    filenames.append(storage.file_name)

print(filenames)


class FtpFile:
    def __init__(self, host, user, passwd):
        self.ftp = FTP(host=host)
        self.ftp.set_pasv(True)
        self.ftp.login(user=user, passwd=passwd)

    def get_file(self, filename):
        new_file = get_filename(filename)
        file = BytesIO()
        print(filename)
        self.ftp.retrbinary('RETR %s' % filename, file.write)
        self.ftp.quit()
        file.seek(0)
        new_file_path = default_storage.save(new_file, ContentFile(file.read()))
        if filename == 'Klients.csv':
            try:
                point_loader = PointLoader(new_file_path)
                point_loader.parse_file()
                point_loader.load()
                point_loader.save_report()
                point_loader.send_email()
            except:
                pass
        elif filename == 'Priz.csv':
            try:
                bonus_loader = BonusLoader(new_file_path)
                bonus_loader.parse_file()
                bonus_loader.load()
                bonus_loader.save_report()
                bonus_loader.send_email()
            except:
                pass
        elif 'News_auto_' in filename:
            try:
                storage_index = filename[10:11]
                ProductLoader(new_file_path, storage_index, filename)
            except:
                pass


class Command(BaseCommand):
    help = 'Download files from FTP'

    def handle(self, *args, **options):
        for filename in filenames:
            try:
                ftp = FtpFile(host=HOST, user=USER, passwd=PASSWD)
                ftp.get_file(filename)
            except:
                pass

        self.stdout.write(self.style.SUCCESS('Successfully'))
