from django.conf.urls import url
from .models import ImageModel
from .forms import ImageForm
from .views import Upload, ViewText
from django.conf import settings
from django.conf.urls.static import static

app_name = 'TestAPI'

urlpatterns = [
    url(r'^$', Upload.as_view(), name='upload'),
    url(r'^view/$', ViewText.as_view(), name='view'),
]

# for development purpose only
# django dev. server will serve static files using below urlpatterns.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)