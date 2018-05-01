from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

from visualize.views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url('^admin/', admin.site.urls),
    url('', include('visualize.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
