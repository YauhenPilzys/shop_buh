from rest_framework import viewsets, filters, mixins, status
from rest_framework.views import APIView

from .models import Product, Client, Provider, Group, Invoice, Bank, Expense, Stock, Price_change
from .paginations import *
from .serializers import ProductSerializer, ClientSerializer, ProviderSerializer, GroupSerializer, InvoiceSerializer, \
    BankSerializer, ExpenseSerializer, StockSerializer, Price_changeSerializer, InvoiceCreateSerializer, \
    BankCreateSerializer, ClientCreateSerializer, ClientDetailSerializer, ProviderCreateSerializer, \
    ProviderDetailSerializer, StockCreateSerializer, StockDetailSerializer

from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import *
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.db.models.functions import Lower




class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all().order_by('-id')
    serializer_class = ProviderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['provider_name']
    pagination_class = APIListPagination


    def get_serializer_class(self):
        if self.action == 'create':
            return ProviderCreateSerializer  #сериализатор для POST-запросов
        return ProviderDetailSerializer

#Если в накладой есть поставщик - TRUE, иначе FALSEь
    @action(detail=True, methods=['GET'])
    def check_invoice(self, request, pk=None):
        providers = self.get_object()
        invoice_exists = providers.invoice_set.exists()
        return Response({'exists': invoice_exists})



class ProviderListView(generics.ListAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-id')
    serializer_class = InvoiceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['invoice_number', 'provider_name']
    pagination_class = APIListPagination



    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InvoiceCreateSerializer
        return InvoiceSerializer





class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['client_name']
    pagination_class = APIListPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return ClientCreateSerializer  #сериализатор для POST-запросов
        return ClientDetailSerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['product_name']
    pagination_class = APIListPagination



class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['group_name']
    pagination_class = APIListPagination



class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all().order_by('-id')
    serializer_class = BankSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['bank_name']
    pagination_class = APIListPagination





class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-id')
    serializer_class = ExpenseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['']
    pagination_class = APIListPagination


class StockViewSet(viewsets.ModelViewSet):

    queryset = Stock.objects.all().order_by('-id')
    serializer_class = StockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['product.product_name']
    pagination_class = APIListPagination


    def get_serializer_class(self):
        if self.action == 'create':
            return StockCreateSerializer  #сериализатор для POST-запросов
        return StockDetailSerializer

    @action(detail=False, methods=['GET'])
    def available_products(self, request):
        #Получаем список товаров на складе с количеством больше 0
        available_products =Stock.objects.filter(product_quantity__gt=0)
        serializer = StockSerializer(available_products, many=True)
        return Response(serializer.data)


class Price_changeViewSet(viewsets.ModelViewSet):
    queryset = Price_change.objects.all().order_by('-id')
    serializer_class = Price_changeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['']
    pagination_class = APIListPagination
