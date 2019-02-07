from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf.urls import url

from config import settings
from market import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^products/?$', views.ProductListView.as_view(), name='products'),
    url(r'^product/(?P<pk>\d+)$', views.ProductDetailView.as_view(), name='product'),
    url(r'^cart/?$', views.cart, name='cart'),
    url(r'^checkout/?$', views.checkout, name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)