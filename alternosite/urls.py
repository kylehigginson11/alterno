from django.conf.urls import url
from alternosite.views import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

from alternosite.views.views import ProductLikeAPIToggle

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.loginuser, name='login'),
    url(r'^logout/$', views.logoutuser, name='logout'),
    url(r'^register/$', views.registeruser, name='register'),
    url(r'^product/(?P<id>[\w-]+)/', views.detailProduct, name='product_detail'),

    # API URLS
    url(r'^api/(?P<product>[\w-]+)/like/$', ProductLikeAPIToggle.as_view(), name='like-api-toggle'),
]

# media urls
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
