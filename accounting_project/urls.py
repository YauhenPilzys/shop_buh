"""
URL configuration for accounting_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers

from accounting_app import views
from accounting_app.views import *



schema_view = get_schema_view(
    openapi.Info(
        title="API for SHOP",
        default_version='v1',
        description="Your API Description",

        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'providers', ProviderViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'banks', BankViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'prices_change', Price_changeViewSet)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),



]

