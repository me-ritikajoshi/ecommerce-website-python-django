from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('products/', include(('product.urls', 'product'), namespace='product')),
    path('', include(('userspage.urls', 'userspage'), namespace='userspage')),
    path('admin/', include(('adminpage.urls', 'adminpage'), namespace='adminpage')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
