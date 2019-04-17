from django.conf import settings
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.core.files.storage import FileSystemStorage






urlpatterns = [
    path('home/', views.home, name="home"),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('logged_home/',views.logged_home,name="logged_home"),
    path('logged_contact/',views.logged_contact,name='logged_contact'),
    path('logged_about/',views.logged_about,name='logged_about'),
    # path('upload/',views.upload,name='upload'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)