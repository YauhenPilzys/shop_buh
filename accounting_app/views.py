from rest_framework import viewsets, filters, mixins, status
from rest_framework.views import APIView
from .paginations import *
from .serializers import ProductSerializer, ClientSerializer, ProviderSerializer, GroupSerializer, InvoiceSerializer, \
    BankSerializer, ExpenseSerializer, StockSerializer, Price_changeSerializer, InvoiceCreateSerializer, \
    ClientCreateSerializer, ClientDetailSerializer, ProviderCreateSerializer, \
    ProviderDetailSerializer, StockCreateSerializer, StockDetailSerializer, IncomeSerializer, IncomeCreateSerializer, \
    IncomeDetailSerializer, Expense_itemSerializer, RetailSerializer, ExpenseCreateSerializer, ExpenseDetailSerializer, \
    Expense_itemCreateSerializer, Expense_itemDetailSerializer, RetailCreateSerializer, RetailDetailSerializer, \
    Price_changeCreateSerializer, Price_changeDetailSerializer, ContractSerializer, ContractCreateSerializer, \
    ContractDetailSerializer

from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import *
from rest_framework.decorators import action
from rest_framework.response import Response





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

#Если в накладой есть поставщик - TRUE, иначе FALSE
    @action(detail=True, methods=['GET'])
    def check_invoice(self, request, pk=None):
        providers = self.get_object()
        invoice_exists = providers.invoice_set.exists()
        return Response({'exists': invoice_exists})






class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-id')
    serializer_class = InvoiceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['invoice_number', 'provider__provider_name']
    pagination_class = APIListPagination



    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InvoiceCreateSerializer
        return InvoiceSerializer





class ClientViewSet(viewsets.ModelViewSet):  #справочник
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['client_name']
    pagination_class = APIListPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return ClientCreateSerializer  #сериализатор для POST-запросов
        return ClientDetailSerializer



class ProductViewSet(viewsets.ModelViewSet):  #справочник
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['product_name']  #?search=AAAA
    pagination_class = APIListPagination




class GroupViewSet(viewsets.ModelViewSet): #справочник
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['group_name']   #?search=AAAA
    pagination_class = APIListPagination


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all().order_by('-id')
    serializer_class = IncomeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['invoice_id']
    pagination_class = APIListPagination


    def get_serializer_class(self):
        if self.action == 'create':
            return IncomeCreateSerializer  #сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
        return IncomeDetailSerializer


    def get_queryset(self):   #добавили поиск прихода по id_накладной (?invoice_id=2)
        invoice_id = self.request.query_params.get('invoice_id')
        if invoice_id:
            return Income.objects.filter(invoice_id=invoice_id)
        return super().get_queryset()



class BankViewSet(viewsets.ModelViewSet): #справочник
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


    def get_serializer_class(self):
        if self.action == 'create':
            return ExpenseCreateSerializer  #сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
        return ExpenseDetailSerializer



class Expense_itemViewSet(viewsets.ModelViewSet):
    queryset = Expense_item.objects.all().order_by('-id')
    serializer_class = Expense_itemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['']
    pagination_class = APIListPagination


    def get_serializer_class(self):
        if self.action == 'create':
            return Expense_itemCreateSerializer  #сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
        return Expense_itemDetailSerializer



    def get_queryset(self): #добавили поиск расхода по id_накладной расхода (api/expenses_item/?expense_id=1)
        expense_id = self.request.query_params.get('expense_id')
        if expense_id:
            return Expense_item.objects.filter(expense_id=expense_id)
        return super().get_queryset()


class StockViewSet(viewsets.ModelViewSet):

    queryset = Stock.objects.all().order_by('-id')
    serializer_class = StockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__product_name', 'product__id']  #?search=AAAA (имя товара / ID товара)
    pagination_class = APIListPagination



    def get_serializer_class(self):
        if self.action == 'create':
            return StockCreateSerializer  #сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
        return StockDetailSerializer

    #сделать ссылку поиска на складе товара по его ID (GET /api/stocks/search_by_product_id/?product_id=2)
    @action(detail=False, methods=['GET'])
    def search_by_product_id(self, request):
        product_id = request.query_params.get('product_id')

        if not product_id:
            return Response({"message": "Не указан ID товара"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            stock = Stock.objects.get(product__id=product_id)
        except Stock.DoesNotExist:
            return Response({"message": "Товар не найден на складе"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(stock)
        return Response(serializer.data)

    #сделать ссылку поиска на складе по названию товара по любой букве (api/stocks/search_product_by_letter/?letter=I)
    @action(detail=False, methods=['GET'])
    def search_product_by_letter(self, request):
        # Получаем значение GET-параметра 'letter'
        letter = request.GET.get('letter', '').strip()

        # Проверяем, что буква передана
        if not letter:
            return Response({'error': 'Буква не введена'})

        # Ищем товары в складе, чьи названия содержат переданную букву
        stock = Stock.objects.filter(product__product_name__icontains=letter)

        # Сериализуем найденные записи и возвращаем результат
        serializer = StockSerializer(stock, many=True)
        return Response(serializer.data)

    # сделать ссылку поиска на складе по точному количеству товара (api/stocks/search_by_quantity/?quantity=0)
    @action(detail=False, methods=['GET'])
    def search_by_quantity(self, request):
        quantity = request.query_params.get('quantity')

        if quantity is not None:
            try:
                quantity = int(quantity)
                products_with_exact_quantity = Stock.objects.filter(product_quantity=quantity)
                serializer = StockSerializer(products_with_exact_quantity, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Некорректно введено количество товара. Укажите целое число'}, status=400)









class Price_changeViewSet(viewsets.ModelViewSet):
    queryset = Price_change.objects.all().order_by('-id')
    serializer_class = Price_changeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['']
    pagination_class = APIListPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return Price_changeCreateSerializer  # сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
        return Price_changeDetailSerializer





class RetailViewSet(viewsets.ModelViewSet):
    queryset = Retail.objects.all().order_by('-id')
    serializer_class = RetailSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['']
    pagination_class = APIListPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return RetailCreateSerializer  #сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
        return RetailDetailSerializer



class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all().order_by('-id')
    serializer_class = ContractSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['client__id']    #?search=1
    pagination_class = APIListPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return ContractCreateSerializer  #сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
        return ContractDetailSerializer


    def get_queryset(self): #добавили поиск договоров по номеру договора (api/contracts/?contract_number=123)
        contract_number = self.request.query_params.get('contract_number')
        if contract_number:
            return Contract.objects.filter(contract_number=contract_number)
        return super().get_queryset()