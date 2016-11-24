from django.conf.urls import url

from tecdoc.views.carmodel import CarModelView
from tecdoc.views.section import SectionList
from tecdoc.views.manufacturer import ManufacturerList, ManufacturerView

urlpatterns = [
    url(r'^$', ManufacturerList.as_view(), name='manufacturers'),
    url(r'^(?P<mnf_id>\d+)/$', ManufacturerView.as_view(), name='manufacturer'),
    url(r'^(?P<mnf_id>\d+)/(?P<model_id>\d+)/$', CarModelView.as_view(), name='model'),
    url(r'^(?P<mnf_id>\d+)/(?P<model_id>\d+)/(?P<type_id>\d+)/$', SectionList.as_view(), name='tree'),
    # url(r'^(?P<mnf_id>\d+)/(?P<model_id>\d+)/(?P<type_id>\d+)/(?P<section_id>\d+)/$', PartList.as_view(),
    #     name='parts-catalog'),
]
