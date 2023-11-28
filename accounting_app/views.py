from sqlite3 import IntegrityError
from django.http import JsonResponse, Http404

from django.db import transaction
from django.db.models import Q, ExpressionWrapper
from django.db.models import F, CharField, Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import F, ExpressionWrapper, DecimalField, IntegerField, Value
from django.db.models.functions import Cast
from django.db.models import F, Sum, Min
from datetime import datetime
from rest_framework import viewsets, filters, mixins, status
from rest_framework.views import APIView
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.core.exceptions import ObjectDoesNotExist


from .paginations import *
from .serializers import ProductSerializer, ClientSerializer, ProviderSerializer, GroupSerializer, InvoiceSerializer, \
    BankSerializer, ExpenseSerializer, StockSerializer, Price_changeSerializer, InvoiceCreateSerializer, \
    ClientCreateSerializer, ClientDetailSerializer, ProviderCreateSerializer, \
    ProviderDetailSerializer, StockCreateSerializer, StockDetailSerializer, IncomeSerializer, IncomeCreateSerializer, \
    IncomeDetailSerializer, Expense_itemSerializer, RetailSerializer, ExpenseCreateSerializer, ExpenseDetailSerializer, \
    Expense_itemCreateSerializer, Expense_itemDetailSerializer, RetailCreateSerializer, RetailDetailSerializer, \
    Price_changeCreateSerializer, Price_changeDetailSerializer, ContractCreateSerializer, \
    ContractDetailSerializer, ContractSerializer, CountrySerializer

from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import *
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models.signals import post_save
from decimal import Decimal





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




    def get_serializer_class(self):          #сериализатор для POST и PACT-запросов (GET показывает весь список, POST оставляет ID ключа другой таблицы)
        if self.request.method == 'POST':
            return InvoiceCreateSerializer
        elif self.request.method == 'PATCH':
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
    search_fields = ['invoice_id'] #?search=AAAA
    pagination_class = APIListPagination

    def get_serializer_class(
            self):  # сериализатор для POST и PACT-запросов (GET показывает весь список, POST оставляет ID ключа другой таблицы)
        if self.request.method == 'POST':
            return IncomeCreateSerializer
        elif self.request.method == 'PATCH':
            return IncomeCreateSerializer
        return IncomeSerializer




    def get_queryset(self):   #Поиск прихода по id_накладной (?invoice_id=2)
        invoice_id = self.request.query_params.get('invoice_id')
        if invoice_id:
            return Income.objects.filter(invoice_id=invoice_id)
        return super().get_queryset()




    #Поиск income по invoice_id от даты и по дату (api/incomes/filter_by_date_and_invoice/?invoice_id=476&start_date=2023-11-01&end_date=2023-12-31)
    @action(detail=False, methods=['GET'])
    def filter_by_date_and_invoice(self, request):
        queryset = self.get_queryset()

        invoice_id = request.query_params.get('invoice_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if invoice_id:
            queryset = queryset.filter(invoice__id=invoice_id)

        if start_date:
            queryset = queryset.filter(invoice__product_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(invoice__product_date__lte=end_date)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




    # Поиск income по product_name от даты и по дату (api/incomes/filter_by_date_and_product_name/?product_name=476&start_date=2023-11-01&end_date=2023-12-31)
    @action(detail=False, methods=['GET'])
    def filter_by_date_and_product_name(self, request):
        queryset = self.get_queryset()

        product_name = request.query_params.get('product_name')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if product_name:
            queryset = queryset.filter(product__product_name__iregex=product_name)

        if start_date:
            queryset = queryset.filter(invoice__product_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(invoice__product_date__lte=end_date)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)








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



    # Поиск expense_item по expense_id от даты и по дату (api/expenses_item/filter_by_date_and_expense/?expense_id=476&start_date=2023-11-01&end_date=2023-12-31)
    @action(detail=False, methods=['get'])
    def filter_by_date_and_expense(self, request):
        queryset = self.get_queryset()

        invoice_id = request.query_params.get('expense_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if invoice_id:
            queryset = queryset.filter(expense__id=invoice_id)

        if start_date:
            queryset = queryset.filter(expense__expense_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(expense__expense_date__lte=end_date)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



    # Поиск expense_item по product_name от даты и по дату (expenses_item/filter_by_date_and_product_name/?product_name=476&start_date=2023-11-01&end_date=2023-12-31)
    @action(detail=False, methods=['GET'])
    def filter_by_date_and_product_name(self, request):
        queryset = self.get_queryset()

        product_name = request.query_params.get('product_name')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if product_name:
            queryset = queryset.filter(product__product_name__iregex=product_name)

        if start_date:
            queryset = queryset.filter(expense__expense_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(expense__expense_date__lte=end_date)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




class UpdateStock(APIView):
    """ Объединение товаров с одинаковыми параметрами """
    #permission_classes = (IsAuthenticated,) - пользоваться залогеным только можно

    def post(self, request, prod_id):
        try:
            prod = Stock.objects.get(pk=prod_id)
        except Stock.DoesNotExist:
            raise Http404("Stock does not exist")
        # Используем транзакцию для обеспечения целостности данных
        with transaction.atomic():
            # Находим все записи с заданными параметрами товаров
            existing_stocks = Stock.objects.filter(
                product_id=prod.product_id,
                product_price=prod.product_price,
                product_country=prod.product_country,
                product_vendor=prod.product_vendor
            ).exclude(product_barcode="").order_by('id')

            if existing_stocks.count() > 1:
                # Проверяем, что не существует уже объединенной записи для данной группы товаров
                existing_merged_stock = Stock.objects.filter(
                    product_id=prod.product_id,
                    product_price=prod.product_price,
                    product_country=prod.product_country,
                    product_vendor=prod.product_vendor,
                    product_barcode__isnull=False
                ).exclude(id__in=existing_stocks).first()

                if not existing_merged_stock:
                    # Создаем список для объединения всех найденных записей
                    stocks_to_merge = existing_stocks

                    earliest_barcode = min(stock.product_barcode for stock in stocks_to_merge)

                    # Вычисляем суммы для объединения
                    total_expense_full_price = sum(float(stock.expense_full_price) for stock in stocks_to_merge)
                    total_product_quantity = sum(int(stock.product_quantity) for stock in stocks_to_merge)

                    # Создаем новую запись Stock с общими значениями
                    new_stock = Stock.objects.create(
                        product_id=prod.product_id,
                        product_price=prod.product_price,
                        product_country=prod.product_country,
                        product_vendor=prod.product_vendor,
                        product_reserve=prod.product_reserve,
                        product_price_provider=prod.product_price_provider,
                        expense_allowance=prod.expense_allowance,
                        product_vat=prod.product_vat,
                        product_barcode=earliest_barcode,
                        expense_full_price=str(total_expense_full_price),
                        product_quantity=str(total_product_quantity)
                    )

                    # Обновляем связанные записи в модели Income
                    Income.objects.filter(stock__in=stocks_to_merge).update(stock=new_stock)

                    # Удаляем все объединенные записи, кроме новой
                    stocks_to_merge.exclude(id=new_stock.id).delete()

        return Response()


class StockViewSet(viewsets.ModelViewSet):

    queryset = Stock.objects.all().order_by('-id')
    serializer_class = StockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__product_name', 'product__id']  #?search=AAAA (имя товара / ID товара)
    pagination_class = APIListPagination

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404:
            return Response([])  # Возвращаем пустой массив, если объект не найден по ID




    def get_serializer_class(self):
        if self.action == 'create':
            return StockCreateSerializer  #сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
        return StockDetailSerializer



    # Замена строк где есть одинаковые параметры ввода и обновление последневведенных + замена id обновленного stock в таблицу income
    #@receiver(pre_save, sender=Stock)



    # Поиск товаров от одного до пяти слов и артикула. Список всех товаров связанных с первым словом +  список всех товаров с вторым словом и так далее
    #(/api/stocks/filter_by_keyword/?query=рамка+дом+артикул в числовом значении)

    @action(detail=False, methods=['GET'])
    def filter_by_keyword(self, request):
        query = request.query_params.get('query', '')
        keywords = query.split()

        queryset = Stock.objects.all()
        results = queryset

        if len(keywords) == 1:
            single_keyword = keywords[0]
            # Поиск по одному слову в названии и артикулу товара
            results = results.filter(
                Q(product__product_name__iregex=single_keyword) |
                Q(product_vendor__iregex=single_keyword)
            )
        elif len(keywords) >= 2 and len(keywords) <= 5:
            # Поиск по 2-5 словам в названии и артикулу товара
            for keyword in keywords:
                results = results.filter(
                    Q(product__product_name__iregex=keyword) |
                    Q(product_vendor__iregex=keyword)
                )

        # Применяем пагинацию к записям
        self.pagination_class = APIListPagination
        page = self.paginate_queryset(results)
        if page is not None:
            serializer = StockSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StockSerializer(results, many=True)

        return Response({'results': serializer.data})



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





    # Поиск на складе товара по его ID (GET /api/stocks/search_by_product_id/?product_id=2)
    @action(detail=False, methods=['GET'])
    def search_by_product_id(self, request):
        product_id = request.query_params.get('product_id')

        if not product_id:
            return Response({"message": "Не указан ID товара"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            stock = Stock.objects.filter(
                product__id=product_id)  # filter-выводит два одинаковых ID товара, get - один товар
        except Stock.DoesNotExist:
            return Response({"response": "false"}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(stock,
                                         many=True)  # filter- выводит два одинковых ID , get - один товар(удаляем many=TRUE)
        return Response(serializer.data)


    # Поиск на складе по точному количеству товара (api/stocks/search_by_quantity/?quantity=0)
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
    search_fields = ['income__id'] #?search
    pagination_class = APIListPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return Price_changeCreateSerializer  #сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
        return Price_changeDetailSerializer

    @action(detail=False, methods=[
        'GET'])  # Поиск по номеру инвойса и название товара с учетом фильтров (api/prices_change/search_by_invoice_product/?invoice_number=1&product_name=асфа)
    def search_by_invoice_product(self, request):
        invoice_number = request.GET.get('invoice_number')
        product_name = request.GET.get('product_name')

        if invoice_number is not None:
            # Создаем фильтр для поиска по номеру инвойса
            invoice_filter = Q(invoice_number__iexact=invoice_number)

            # Создаем фильтр для поиска по названию товара (если указано)
            product_filter = Q()
            if product_name:
                # Переносим в нижний регистр и разделяем на слова
                product_name = product_name.lower()
                product_name_parts = product_name.split()

                # Создаем фильтра для поиска по названию товара (без учета регистра и частичное совпадение)
                for part in product_name_parts:
                    product_filter |= Q(product_name__iregex=part)

            # Искать и фильтровать записи в таблицах Invoice и Product
            invoices = Invoice.objects.filter(invoice_filter)
            products = Product.objects.filter(product_filter)

            # Если найдены соответствующие записи, вернуть их сериализованные данные
            if invoices.exists() and products.exists():
                invoice_serializer = InvoiceSerializer(invoices, many=True)
                product_serializer = ProductSerializer(products, many=True)
                return Response({
                    'invoices': invoice_serializer.data,
                    'products': product_serializer.data
                })
            else:
                return Response({'message': 'Записей не найдено.'}, status=404)
        else:
            # Если номер инвойса не указан, вернуть всю таблицу PriceChange
            price_changes = Price_change.objects.all()
            price_change_serializer = Price_changeSerializer(price_changes, many=True)
            return Response({'price_changes': price_change_serializer.data})


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





class CountryViewSet(viewsets.ModelViewSet):  #справочник
    queryset = Country.objects.all().order_by('-id')
    serializer_class = CountrySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['country_name']  #?search=AAAA
    pagination_class = APIListPagination

    # Поиск страны по букве в независимости от регистра и сортировка 5 по ID (api/countries/search_by_name/?name=)
    @action(detail=False, methods=['GET'])
    def search_by_name(self, request):
        query = request.query_params.get('name', '')

        # Делаем пагинацию
        paginator = PageNumberPagination()

        # Получаем количество записей на странице из параметра запроса, по умолчанию 5
        page_size = int(request.query_params.get('page_size', 5))
        paginator.page_size = page_size

        if not query:
            countries = Country.objects.all()  # Возвращает все записи, если 'name' не задан
        else:
            countries = Country.objects.filter(country_name__iregex=query).order_by('-id') #Поиск по имени по любой букве

        # Применяем пагинацию к результатам
        paginated_countries = paginator.paginate_queryset(countries, request)

        serializer = CountrySerializer(paginated_countries, many=True)
        return paginator.get_paginated_response(serializer.data)












