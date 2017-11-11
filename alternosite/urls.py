from django.conf.urls import url
from alternosite.views import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

from alternosite.views.views import ProductLikeAPIToggle, AddAlternative

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.loginuser, name='login'),
    url(r'^logout/$', views.logoutuser, name='logout'),
    url(r'^register/$', views.registeruser, name='register'),
    url(r'^product/(?P<id>[\w-]+)/', views.detailProduct, name='product_detail'),
    url(r'^api/product_list/', views.ProductAutocompleteList.as_view(), name='product_list_api'),
    url(r'^account', views.account, name='account'),
    url(r'^category/', views.category, name='category'),
    url(r'^product_line/(?P<id>[\w-]+)/', views.product_line, name='product_line'),
    url(r'^change_details', views.change_details, name='change_details'),

    # API URLS
    url(r'^api/(?P<product>[\w-]+)/like/$', ProductLikeAPIToggle.as_view(), name='like-api-toggle'),
    url(r'^api/add_alternative/$', AddAlternative.as_view(), name='add-alt-api'),
    url(r'^api/pop_list/(?P<sub_id>[\w-]+)/$', views.PopularItemsList.as_view(), name='pop-list-api'),
]

# media urls
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
