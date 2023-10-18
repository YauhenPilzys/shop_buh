from django.db.models import Q
from rest_framework import viewsets, filters, mixins, status
from rest_framework.views import APIView
from .paginations import *
from .serializers import ProductSerializer, ClientSerializer, ProviderSerializer, GroupSerializer, InvoiceSerializer, \
    BankSerializer, ExpenseSerializer, StockSerializer, Price_changeSerializer, InvoiceCreateSerializer, \
    ClientCreateSerializer, ClientDetailSerializer, ProviderCreateSerializer, \
    ProviderDetailSerializer, StockCreateSerializer, StockDetailSerializer, IncomeSerializer, IncomeCreateSerializer, \
    IncomeDetailSerializer, Expense_itemSerializer, RetailSerializer, ExpenseCreateSerializer, ExpenseDetailSerializer, \
    Expense_itemCreateSerializer, Expense_itemDetailSerializer, RetailCreateSerializer, RetailDetailSerializer, \
    Price_changeCreateSerializer, Price_changeDetailSerializer, ContractCreateSerializer, \
    ContractDetailSerializer, ContractSerializer

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
    search_fields = ['provider_name'] #?search
    pagination_class = APIListPagination


    def get_serializer_class(self):
        if self.action == 'create':
            return ProviderCreateSerializer  #сериализатор для POST-запросов
        return ProviderDetailSerializer

#Еслли в накладой есть поставщик - TRUE, иначе FALSE  (/api/providers/5/check_invoice)
    @action(detail=True, methods=['GET'])
    def check_invoice(self, request, pk=None):
        providers = self.get_object()
        invoice_exists = providers.invoice_set.exists()
        return Response({'exists': invoice_exists})

    #Поиск поставшика по букве в независимости от регистра и сортировка 5 по ID (api/providers/search_by_name/?name=)
    @action(detail=False, methods=['GET'])
    def search_by_name(self, request):
        query = request.query_params.get('name', '')

        #Делаем пагинацию
        paginator = PageNumberPagination()

        # Получаем количество записей на странице из параметра запроса, по умолчанию 5
        page_size = int(request.query_params.get('page_size', 5))
        paginator.page_size = page_size

        if not query:
            providers = Provider.objects.all()  # Возвращает все записи, если 'name' не задан
        else:
            providers = Provider.objects.filter(provider_name__iregex=query).order_by('-id')

        # Применяем пагинацию к результатам
        paginated_providers = paginator.paginate_queryset(providers, request)

        serializer = ProviderSerializer(paginated_providers, many=True)
        return paginator.get_paginated_response(serializer.data)







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



    # Поиск invoice по invoice_number в независимости от регистра и сортировка 5 по ID (api/invoices/search_by_name/?name=)
    @action(detail=False, methods=['GET'])
    def search_by_name(self, request):
        query = request.query_params.get('name', '')

        # Делаем пагинацию
        paginator = PageNumberPagination()

        # Получаем количество записей на странице из параметра запроса, по умолчанию 5
        page_size = int(request.query_params.get('page_size', 5))
        paginator.page_size = page_size

        if not query:
            invoices = Invoice.objects.all()  # Возвращает все записи, если 'name' не задан
        else:
            invoices = Invoice.objects.filter(invoice_number__iregex=query).order_by('-id')

        # Применяем пагинацию к результатам
        paginated_invoices = paginator.paginate_queryset(invoices, request)

        serializer = InvoiceSerializer(paginated_invoices, many=True)
        return paginator.get_paginated_response(serializer.data)





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

    # Поиск клиента по букве в независимости от регистра и сортировка 5 по ID (api/clients/search_by_name/?name=)
    @action(detail=False, methods=['GET'])
    def search_by_name(self, request):
        query = request.query_params.get('name', '')

        # Делаем пагинацию
        paginator = PageNumberPagination()

        # Получаем количество записей на странице из параметра запроса, по умолчанию 5
        page_size = int(request.query_params.get('page_size', 5))
        paginator.page_size = page_size

        if not query:
            clients = Client.objects.all()  # Возвращает все записи, если 'name' не задан
        else:
            clients = Client.objects.filter(client_name__iregex=query).order_by('-id')

        # Применяем пагинацию к результатам
        paginated_clients = paginator.paginate_queryset(clients, request)

        serializer = ClientSerializer(paginated_clients, many=True)
        return paginator.get_paginated_response(serializer.data)






class ProductViewSet(viewsets.ModelViewSet):  #справочник
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['product_name']  #?search=AAAA
    pagination_class = APIListPagination



    # Поиск товара по букве в независимости от регистра и сортировка 5 по ID (api/products/search_by_name/?name=)
    @action(detail=False, methods=['GET'])
    def search_by_name(self, request):
        query = request.query_params.get('name', '')

        # Делаем пагинацию
        paginator = PageNumberPagination()

        # Получаем количество записей на странице из параметра запроса, по умолчанию 5
        page_size = int(request.query_params.get('page_size', 5))
        paginator.page_size = page_size

        if not query:
            products = Product.objects.all()  # Возвращает все записи, если 'name' не задан
        else:
            products = Product.objects.filter(product_name__iregex=query).order_by('-id')

        # Применяем пагинацию к результатам
        paginated_products = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)




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


    def get_queryset(self):   #Поиск прихода по id_накладной (?invoice_id=2)
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

    # Поиск банка по букве в независимости от регистра и сортировка 5 по ID (api/banks/search_by_name/?name=)
    @action(detail=False, methods=['GET'])
    def search_by_name(self, request):
        query = request.query_params.get('name', '')

        # Делаем пагинацию
        paginator = PageNumberPagination()

        # Получаем количество записей на странице из параметра запроса, по умолчанию 5
        page_size = int(request.query_params.get('page_size', 5))
        paginator.page_size = page_size

        if not query:
            banks = Bank.objects.all()  # Возвращает все записи, если 'name' не задан
        else:
            banks = Bank.objects.filter(bank_name__iregex=query).order_by('-id')

        # Применяем пагинацию к результатам
        paginated_banks = paginator.paginate_queryset(banks, request)

        serializer = BankSerializer(paginated_banks, many=True)
        return paginator.get_paginated_response(serializer.data)





class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-id')
    serializer_class = ExpenseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['']
    pagination_class = APIListPagination

    # Поиск банка по букве в независимости от регистра и сортировка 5 по ID (api/banks/search_by_name/?name=)
    def get_serializer_class(self):
        if self.action == 'create':
            return ExpenseCreateSerializer  #сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
        return ExpenseDetailSerializer

    # Поиск expense по expense_number букве в независимости от регистра и сортировка 5 по ID (api/expenses/search_by_name/?name=)
    @action(detail=False, methods=['GET'])
    def search_by_name(self, request):
        query = request.query_params.get('name', '')

        # Делаем пагинацию
        paginator = PageNumberPagination()

        # Получаем количество записей на странице из параметра запроса, по умолчанию 5
        page_size = int(request.query_params.get('page_size', 5))
        paginator.page_size = page_size

        if not query:
            expenses = Expense.objects.all()  # Возвращает все записи, если 'name' не задан
        else:
            expenses = Expense.objects.filter(expense_number__iregex=query).order_by('-id')

        # Применяем пагинацию к результатам
        paginated_expenses = paginator.paginate_queryset(expenses, request)

        serializer = ExpenseSerializer(paginated_expenses, many=True)
        return paginator.get_paginated_response(serializer.data)









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






    def get_queryset(self): #Поиск расхода по id_накладной расхода (api/expenses_item/?expense_id=1)
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

    # Замена строк где есть одинаковые параметры ввода и обновление последневведенных
    @receiver(pre_save, sender=Stock)
    def update_stock(sender, instance, **kwargs):
        # Проверяем, существует ли запись с такими же product_id, product_country, product_price, product_vendor
        existing_stock = Stock.objects.filter(product_id=instance.product_id,
                                              product_country=instance.product_country,
                                              product_price=instance.product_price,
                                              product_vendor=instance.product_vendor).exclude(
            id=instance.id).order_by('-id').first()

        if existing_stock:
            # Обновляем значения полей в соответствии с требованиями
            instance.expense_allowance = existing_stock.expense_allowance
            instance.product_reserve = existing_stock.product_reserve
            instance.product_vat = existing_stock.product_vat
            instance.product_barcode = existing_stock.product_barcode
            instance.product_price_provider = existing_stock.product_price_provider  #цена с надбавкой
            instance.expense_full_price = str(float(existing_stock.expense_full_price) + float(instance.expense_full_price)) #общая цена с ндс
            instance.product_quantity = str(int(existing_stock.product_quantity) + int(instance.product_quantity))

            # Если это не создание новой записи и не PATCH запрос, обновляем количество записи
            if not kwargs.get('update_fields'):
                instance.product_quantity

                if existing_stock.id != instance.id:
                    existing_stock.delete()



















    def get_serializer_class(self):
        if self.action == 'create':
            return StockCreateSerializer  #сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
        return StockDetailSerializer

    #Поиск на складе товара по его ID (GET /api/stocks/search_by_product_id/?product_id=2)
    @action(detail=False, methods=['GET'])
    def search_by_product_id(self, request):
        product_id = request.query_params.get('product_id')

        if not product_id:
            return Response({"message": "Не указан ID товара"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            stock = Stock.objects.filter(product__id=product_id)  #filter- выводит два одинаковых ID товара, get - один товар
        except Stock.DoesNotExist:
            return Response({"response": "false"}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(stock, many=True) #filter- выводит два одинковых ID , get - один товар(удаляем many=TRUE)
        return Response(serializer.data)

    # Поиск на складе по названию товара по любой букве без учета регистра (api/stocks/search_by_name/?name=а)
    # Поиск по названию без учета регистра - iregex, если по любой букве - icontains
    @action(detail=False, methods=['GET'])
    def search_by_name(self, request):
        search_query = request.query_params.get('name', '')

        if not search_query:
            # Если запрос пуст, возвращает все строки
            stock = Stock.objects.all()
        else:
            # Поле, связанное с моделью Product для поиска по названию без учета регистра
            products = Product.objects.filter(product_name__iregex=search_query)
            stock = Stock.objects.filter(product__in=products)

        stock = stock.order_by('-product')[:5] #Упорядочиваем результаты по продукту в убывающем порядке

        if stock:
            serializer = StockSerializer(stock, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Товары не найдены'}, status=status.HTTP_404_NOT_FOUND)



    #Поиск на складе по точному количеству товара (api/stocks/search_by_quantity/?quantity=0)
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
            return Price_changeCreateSerializer  #сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
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


    def get_queryset(self): #Поиск договоров по номеру договора (api/contracts/?contract_number=123)
        contract_number = self.request.query_params.get('contract_number')
        if contract_number:
            return Contract.objects.filter(contract_number=contract_number)
        return super().get_queryset()



   #Поиск по двум параметрам где номер контракта по цифре все данные,или есть пустой запрос то весь список выдает (api/contracts/search_by_client_and_number/?client_id=4&contract_number=1234)
    @action(detail=False, methods=['GET'])
    def search_by_client_and_number(self, request):
        client_id = request.query_params.get('client_id')
        contract_number = request.query_params.get('contract_number')

        if not client_id:
            return Response({"message": "Не указан параметр client_id"}, status=status.HTTP_400_BAD_REQUEST)

        contracts = Contract.objects.filter(client_id=client_id)

        if contract_number:
            contracts = contracts.filter(contract_number__icontains=contract_number)

        #Сортируем записи по дате создания в обратном порядке в количестве 5 записей
        contracts = contracts.order_by('-contract_number')[:5]

        serializer = self.get_serializer(contracts, many=True)
        return Response(serializer.data)






