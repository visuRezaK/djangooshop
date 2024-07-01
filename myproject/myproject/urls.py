from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
#from shop.views import helloworld

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
   
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
