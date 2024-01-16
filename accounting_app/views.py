import functools
from decimal import Decimal

from django.db import transaction
from django.db.models import Q, Sum, F, ExpressionWrapper, Max, When
from django.db.models import Sum, Max, F, Case, When, DecimalField
from django.forms import DecimalField
from rest_framework import viewsets, filters
from django.http import Http404, HttpResponse
from sqlparse.sql import Case

from .paginations import *
from rest_framework.decorators import action
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.db.models.functions import Coalesce, Cast
from django.db.models import Sum, F, Func, DecimalField
from django.utils import timezone


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all().order_by('-id')
    serializer_class = ProviderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['provider_name'] #?search
    pagination_class = APIListPagination
    permission_classes = [IsAuthenticated]


    def get_serializer_class(self):          #сериализатор для POST и PATCH-запросов (GET показывает весь список, POST оставляет ID ключа другой таблицы)
        if self.request.method == 'POST':
            return ProviderCreateSerializer
        elif self.request.method == 'PATCH':
            return ProviderCreateSerializer
        return ProviderSerializer



    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return ProviderCreateSerializer  #сериализатор для POST-запросов
    #     return ProviderDetailSerializer

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
            providers = Provider.objects.all().order_by('-id')  # Возвращает все записи, если 'name' не задан
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
    permission_classes = [IsAuthenticated]




    def get_serializer_class(self):          #сериализатор для POST и PATCH-запросов (GET показывает весь список, POST оставляет ID ключа другой таблицы)
        if self.request.method == 'POST':
            return InvoiceCreateSerializer
        elif self.request.method == 'PATCH':
            return InvoiceCreateSerializer
        return InvoiceSerializer




    #Поиск с даты по дату по двум параметрам + пагинация  (http://127.0.0.1:8000/api/invoices/?date=min (max))
    def get_queryset(self):
        queryset = super().get_queryset()

        # Получаем параметр order_by из запроса
        order_by = self.request.query_params.get('date', None)

        # Сортируем записи в зависимости от параметра order_by
        if order_by == 'min':
            # Если указан date=min, сортируем по возрастанию
            queryset = queryset.order_by('product_date')
        elif order_by == 'max':
            # Если указан date=max, сортируем по убыванию
            queryset = queryset.order_by('-product_date')

        return queryset



    #Поиск в инвосе по provider_name (/invoices/search_by_provider_name/?name=)
    @action(detail=False, methods=['GET'])
    def search_by_provider_name(self, request):
        query = request.query_params.get('name', '')

        # Делаем пагинацию
        paginator = PageNumberPagination()

        # Получаем количество записей на странице из параметра запроса, по умолчанию 5
        page_size = int(request.query_params.get('page_size', 5))
        paginator.page_size = page_size

        if not query:
            invoices = Invoice.objects.all().order_by('-id')  # Возвращает все записи, если 'name' не задан
        else:
            invoices = Invoice.objects.filter(providers__provider_name__iregex=query).order_by('-id')

        # Применяем пагинацию к результатам
        paginated_invoices = paginator.paginate_queryset(invoices, request)

        serializer = InvoiceSerializer(paginated_invoices, many=True)
        return paginator.get_paginated_response(serializer.data)





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
            invoices = Invoice.objects.all().order_by('-id')  # Возвращает все записи, если 'name' не задан
        else:
            invoices = Invoice.objects.filter(invoice_number__iregex=query).order_by('-id')

        # Применяем пагинацию к результатам
        paginated_invoices = paginator.paginate_queryset(invoices, request)

        serializer = InvoiceSerializer(paginated_invoices, many=True)
        return paginator.get_paginated_response(serializer.data)



    # Поиск по параметрам : 1) даты с по, 2) дата с по + поставщик
    # api/invoices/filter_by_invoice/?start_date=2023-01-01&end_date=2023-12-31&provider_id=10
    @action(detail=False, methods=['get'])
    def filter_by_invoice(self, request):
        queryset = self.get_queryset()

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        provider_id = request.query_params.get('provider_id')

        if start_date:
            queryset = queryset.filter(product_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(product_date__lte=end_date)

        if provider_id:
            queryset = queryset.filter(providers_id__id=provider_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



    #Запрос про сумму по каждому поставщику за дату (http://127.0.0.1:8000/api/invoices/search_by_date_sum/?date=13.01.2024)
    @action(detail=False, methods=['GET'])
    def search_by_date_sum(self, request):
        date_str = self.request.query_params.get('date', None)

        if not date_str:
            return Response({'error': 'Please provide a valid date in the query parameters.'}, status=400)

        try:
            date = timezone.datetime.strptime(date_str, '%d.%m.%Y').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Please use DD.MM.YYYY.'}, status=400)

        result = (
            Provider.objects
            .annotate(
                total_price=Sum(
                    'invoice__product_price',
                    filter=Q(invoice__product_date__lte=date)
                ),
                last_product_date=Max('invoice__product_date')
            )
            .filter(
                Q(total_price__gt=0) |
                Q(last_product_date=date)
            )
            .values('id', 'provider_name', 'total_price', 'last_product_date')
        )

        response_data = []

        for entry in result:
            provider_id = entry['id']

            # Get the invoices for the current provider within the specified date range
            invoices = Invoice.objects.filter(providers_id=provider_id)

            # Преобразование CharField в числа и суммирование для продуктов в диапазоне введенной даты
            total_product_price = sum(
                float(invoice.product_price) if invoice.product_price and invoice.product_date <= date else 0
                for invoice in invoices
            )

            response_data.append({'provider_id': provider_id, 'provider_name': entry['provider_name'],
                                  'product_price': total_product_price})

        return Response(response_data)



    #запрос с даты по дату + поставщик+ сумма до этой даты (http://127.0.0.1:8000/api/invoices/search_by_date_sum_provider/?date=13.01.2024&provider_id=1)

    @action(detail=False, methods=['GET'])
    def search_by_date_sum_provider(self, request):
        date_str = self.request.query_params.get('date', None)
        provider_id = self.request.query_params.get('provider_id', None)

        if not date_str:
            return Response({'error': 'Please provide a valid date in the query parameters.'}, status=400)

        try:
            date = timezone.datetime.strptime(date_str, '%d.%m.%Y').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Please use DD.MM.YYYY.'}, status=400)

        # Получаем сумму для каждого поставщика по всем записям
        result = (
            Provider.objects
            .annotate(
                total_price=Sum('invoice__product_price'),
                last_product_date=Max('invoice__product_date')
            )
            .filter(
                Q(total_price__gt=0) |
                Q(last_product_date=date)
            )
        )

        if provider_id:
            result = result.filter(id=provider_id)

        response_data = []

        for entry in result.values('id', 'provider_name', 'total_price', 'last_product_date'):
            provider_id = entry['id']

            # Получаем сумму для текущего поставщика только до введенной даты
            invoices = Invoice.objects.filter(providers_id=provider_id, product_date__lt=date)

            total_product_price = sum(
                Decimal(invoice.product_price) if invoice.product_price else Decimal('0.0')
                for invoice in invoices
            )

            response_data.append({
                'provider_id': provider_id,
                'provider_name': entry['provider_name'],
                'product_price': total_product_price
            })

        return Response(response_data)


    #С даты по дату выводит цену поставщика и дату
    #http://127.0.0.1:8000/api/invoices/search_by_date_provider/?start_date=11.01.2024&end_date=20.01.2024&provider_id=1

    @action(detail=False, methods=['GET'])
    def search_by_date_provider(self, request):
        start_date_str = self.request.query_params.get('start_date', None)
        end_date_str = self.request.query_params.get('end_date', None)
        provider_id = self.request.query_params.get('provider_id', None)

        if not start_date_str or not end_date_str:
            return Response({'error': 'Please provide valid start_date and end_date in the query parameters.'},
                            status=400)

        try:
            start_date = timezone.datetime.strptime(start_date_str, '%d.%m.%Y').date()
            end_date = timezone.datetime.strptime(end_date_str, '%d.%m.%Y').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Please use DD.MM.YYYY.'}, status=400)

        # Запрос для получения записей для каждого поставщика в заданном диапазоне дат
        result = (
            Provider.objects
            .filter(invoice__product_date__range=(start_date, end_date))
            .distinct()
            .values('id', 'provider_name')
        )

        if provider_id:
            result = result.filter(id=provider_id)

        response_data = []

        for entry in result:
            current_provider_id = entry['id']

            # Получаем записи для текущего поставщика в указанном диапазоне дат
            invoices = Invoice.objects.filter(
                providers_id=current_provider_id,
                product_date__range=(start_date, end_date)
            )

            # Создаем список записей для текущего поставщика
            invoices_data = [
                {
                    'product_date': invoice.product_date,
                    'product_price': Decimal(invoice.product_price) if invoice.product_price else None
                }
                for invoice in invoices
            ]

            response_data.append({
                'provider_id': current_provider_id,
                'provider_name': entry['provider_name'],
                'invoices': invoices_data
            })

        return Response(response_data)





class ClientViewSet(viewsets.ModelViewSet):  #справочник
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['client_name']
    pagination_class = APIListPagination
    permission_classes = [IsAuthenticated]


    def get_serializer_class(self):          #сериализатор для POST и PATCH-запросов (GET показывает весь список, POST оставляет ID ключа другой таблицы)
        if self.request.method == 'POST':
            return ClientCreateSerializer
        elif self.request.method == 'PATCH':
            return ClientCreateSerializer
        return ClientSerializer

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return ClientCreateSerializer  #сериализатор для POST-запросов
    #     return ClientDetailSerializer

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
            clients = Client.objects.all().order_by('-id')  # Возвращает все записи, если 'name' не задан
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
    permission_classes = [IsAuthenticated]





    # Поиск товара по букве в независимости от регистра и сортировка 5 по ID (api/products/search_by_name/?name=)
    @action(detail=False, methods=['GET'])
    def search_by_name(self, request):
        query = request.query_params.get('name', '')

        # Делаем пагинацию
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Установите желаемый размер страницы

        if query:
            # Если запрос не пустой, разбиваем его на слова
            words = query.split()

            # Формируем Q объекты для каждого слова
            queries = [Q(product_name__iregex=word) for word in words]

            # Используем functools.reduce для объединения Q объектов с оператором 'и'
            combined_query = functools.reduce(lambda x, y: x & y, queries)

            # Фильтруем товары по объединенному запросу
            products = Product.objects.filter(combined_query).order_by('-id')
        else:
            # Если запрос пустой, выводим все записи
            products = Product.objects.all().order_by('-id')

        # Применяем пагинацию к результатам
        paginated_products = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(paginated_products, many=True)

        # Вручную создаем ответ, включая информацию о пагинации
        response_data = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)



class GroupViewSet(viewsets.ModelViewSet): #справочник
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['group_name']   #?search=AAAA
    pagination_class = APIListPagination
    permission_classes = [IsAuthenticated]




class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter]
    search_fields = [] #?search=AAAA
    pagination_class = APIListPagination
    permission_classes = [IsAuthenticated]



    def get_serializer_class(
            self):  # сериализатор для POST и PACT-запросов (GET показывает весь список, POST оставляет ID ключа другой таблицы)
        if self.request.method == 'POST':
            return IncomeCreateSerializer
        elif self.request.method == 'PATCH':
            return IncomeCreateSerializer
        return IncomeSerializer


    # работает неверно выдает всю строку
    # def get_queryset(self):   #Поиск по stock_id и invoice_id (api/incomes/?invoice_id=655&?stock_id=1344)
    #     invoice_id = self.request.query_params.get('invoice_id')
    #     stock_id = self.request.query_params.get('stock_id')
    #
    #     queryset = Income.objects.all()
    #
    #     if invoice_id:
    #         queryset = queryset.filter(invoice_id=invoice_id)
    #
    #     if stock_id:
    #         queryset = queryset.filter(stock__id=stock_id)
    #
    #     return queryset




    # Поиск с даты по дату по двум параметрам + пагинация  (http://127.0.0.1:8000/api/incomes/?date=min (max))?
    def get_queryset(self):
        queryset = super().get_queryset()

        # Получаем параметр order_by из запроса
        order_by = self.request.query_params.get('date', None)

        # Сортируем записи в зависимости от параметра order_by
        if order_by == 'min':
            # Если указан date=min, сортируем по возрастанию
            queryset = queryset.order_by('invoice__product_date')
        elif order_by == 'max':
            # Если указан date=max, сортируем по убыванию
            queryset = queryset.order_by('-invoice__product_date')

        return queryset




     # Поиск получить где параметрами будут : 1) даты с по, 2) дата с по + поставщик, 3) дата с по + товар, 4)дата с по + поставщик + товар
     # (incomes/filter_by_income/?start_date=2023-01-01&end_date=2023-12-31&providers_id=2&product_id=1)
    @action(detail=False, methods=['get'])
    def filter_by_income(self, request):
        queryset = self.get_queryset()

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        provider_id = request.query_params.get('providers_id')
        product_id = request.query_params.get('product_id')

        filters = Q()

        if start_date and end_date:
            filters &= Q(invoice__product_date__range=(start_date, end_date))
        elif start_date:
            filters &= Q(invoice__product_date__gte=start_date)
        elif end_date:
            filters &= Q(invoice__product_date__lte=end_date)

        if provider_id:
            filters &= Q(invoice__providers_id=provider_id)

        if product_id:
            filters &= Q(product_id=product_id)

        queryset = queryset.filter(filters)

        serializer = IncomeSerializer(queryset, many=True)
        return Response(serializer.data)




    #Поиск income по invoice_id от даты и по дату (api/incomes/filter_by_date_and_invoice/?invoice_id=476&start_date=2023-11-01&end_date=2023-12-31)
    @action(detail=False, methods=['GET'])
    def filter_by_date_and_invoice(self, request):
        queryset = self.get_queryset()

        # Получаем количество записей на странице из параметра запроса, по умолчанию 5
        page_size = int(request.query_params.get('page_size', 5))

        invoice_id = request.query_params.get('invoice_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if invoice_id:
            queryset = queryset.filter(invoice__id=invoice_id)

        if start_date:
            queryset = queryset.filter(invoice__product_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(invoice__product_date__lte=end_date)

        # Делаем пагинацию
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)




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
    permission_classes = [IsAuthenticated]



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
            banks = Bank.objects.all().order_by('-id')  # Возвращает все записи, если 'name' не задан
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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(
            self):  # сериализатор для POST и PATCH-запросов (GET показывает весь список, POST оставляет ID ключа другой таблицы)
        if self.request.method == 'POST':
            return ExpenseCreateSerializer
        elif self.request.method == 'PATCH':
            return ExpenseCreateSerializer
        return ExpenseSerializer

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return ExpenseCreateSerializer  #сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
    #     return ExpenseDetailSerializer



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
            expenses = Expense.objects.all().order_by('-id')  # Возвращает все записи, если 'name' не задан
        else:
            expenses = Expense.objects.filter(expense_number__iregex=query).order_by('-id')

        # Применяем пагинацию к результатам
        paginated_expenses = paginator.paginate_queryset(expenses, request)

        serializer = ExpenseSerializer(paginated_expenses, many=True)
        return paginator.get_paginated_response(serializer.data)



    # Поиск по параметрам : 1) даты с по, 2) дата с по + поставщик
    # expenses/filter_by_expense/?start_date=2023-01-01&end_date=2023-12-31&provider_id=10
    @action(detail=False, methods=['get'])
    def filter_by_expense(self, request):
        queryset = self.get_queryset()

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        provider_id = request.query_params.get('provider_id')


        if start_date:
            queryset = queryset.filter(expense_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(expense_date__lte=end_date)

        if provider_id:
            queryset = queryset.filter(provider__id=provider_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



      #поиск по поставщику и сумма expense_sum

    # Запрос про сумму по каждому поставщику за дату (http://127.0.0.1:8000/api/expenses/search_by_date_sum/?date=13.01.2024)
    @action(detail=False, methods=['GET'])
    def search_by_date_sum(self, request):
        date_str = self.request.query_params.get('date', None)

        if not date_str:
            return Response({'error': 'Please provide a valid date in the query parameters.'}, status=400)

        try:
            date = timezone.datetime.strptime(date_str, '%d.%m.%Y').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Please use DD.MM.YYYY.'}, status=400)

        result = (
            Provider.objects
            .annotate(
                total_price=Sum(
                    'expense__expense_sum',
                    filter=Q(expense__expense_date__lte=date)
                ),
                last_expense_date=Max('expense__expense_date')
            )
            .filter(
                Q(total_price__gt=0) |
                Q(last_expense_date=date)
            )
            .values('id', 'provider_name', 'total_price', 'last_expense_date')
        )

        response_data = []

        for entry in result:
            provider_id = entry['id']

            # Get the expenses for the current provider within the specified date range
            expenses = Expense.objects.filter(provider_id=provider_id, expense_date__lte=date)

            # Convert CharField to numbers and sum for expenses in the specified date range
            total_expense_sum = sum(
                float(expense.expense_sum) if expense.expense_sum else 0
                for expense in expenses
            )

            response_data.append({
                'provider_id': provider_id,
                'provider_name': entry['provider_name'],
                'expense_sum': total_expense_sum
            })

        return Response(response_data)

    #запрос с даты по дату + поставщик+ сумма до этой даты
    #(http://127.0.0.1:8000/api/expenses/search_by_date_sum_provider/?date=13.01.2024&provider_id=1)
    @action(detail=False, methods=['GET'])
    def search_by_date_sum_provider(self, request):
        date_str = self.request.query_params.get('date', None)
        provider_id = self.request.query_params.get('provider_id', None)

        if not date_str:
            return Response({'error': 'Please provide a valid date in the query parameters.'}, status=400)

        try:
            date = timezone.datetime.strptime(date_str, '%d.%m.%Y').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Please use DD.MM.YYYY.'}, status=400)

        # Получаем сумму для каждого поставщика по всем записям
        result = (
            Provider.objects
            .annotate(
                total_price=Sum('expense__expense_sum'),
                last_expense_date=Max('expense__expense_date')
            )
            .filter(
                Q(total_price__gt=0) |
                Q(last_expense_date=date)
            )
        )

        if provider_id:
            result = result.filter(id=provider_id)

        response_data = []

        for entry in result.values('id', 'provider_name', 'total_price', 'last_expense_date'):
            provider_id = entry['id']

            # Получаем сумму для текущего поставщика только до введенной даты
            expenses = Expense.objects.filter(provider_id=provider_id, expense_date__lt=date)

            total_expense_sum = sum(
                Decimal(expense.expense_sum) if expense.expense_sum else Decimal('0.0')
                for expense in expenses
            )

            response_data.append({
                'provider_id': provider_id,
                'provider_name': entry['provider_name'],
                'expense_sum': total_expense_sum
            })

        return Response(response_data)

    # С даты по дату выводит цену поставщика и дату
    # http://127.0.0.1:8000/api/expenses/search_by_date_provider/?start_date=11.01.2024&end_date=20.01.2024&provider_id=1

    @action(detail=False, methods=['GET'])
    def search_by_date_provider(self, request):
        start_date_str = self.request.query_params.get('start_date', None)
        end_date_str = self.request.query_params.get('end_date', None)
        provider_id = self.request.query_params.get('provider_id', None)

        if not start_date_str or not end_date_str:
            return Response({'error': 'Please provide valid start_date and end_date in the query parameters.'},
                            status=400)

        try:
            start_date = timezone.datetime.strptime(start_date_str, '%d.%m.%Y').date()
            end_date = timezone.datetime.strptime(end_date_str, '%d.%m.%Y').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Please use DD.MM.YYYY.'}, status=400)

        # Запрос для получения записей для каждого поставщика в заданном диапазоне дат
        result = (
            Provider.objects
            .filter(expense__expense_date__range=(start_date, end_date))
            .distinct()
            .values('id', 'provider_name')
        )

        if provider_id:
            result = result.filter(id=provider_id)

        response_data = []

        for entry in result:
            current_provider_id = entry['id']

            # Получаем записи для текущего поставщика в указанном диапазоне дат
            expenses = Expense.objects.filter(
                provider_id=current_provider_id,
                expense_date__range=(start_date, end_date)
            )

            # Создаем список записей для текущего поставщика
            expense_data = [
                {
                    'expense_date': expense.expense_date,
                    'expense_sum': Decimal(expense.expense_sum) if expense.expense_sum else None
                }
                for expense in expenses
            ]

            response_data.append({
                'provider_id': current_provider_id,
                'provider_name': entry['provider_name'],
                'expenses': expense_data
            })

        return Response(response_data)





   
class Expense_itemViewSet(viewsets.ModelViewSet):
    queryset = Expense_item.objects.all().order_by('-id')
    serializer_class = Expense_itemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['']
    pagination_class = APIListPagination
    permission_classes = [IsAuthenticated]







    def get_serializer_class(self):
        if self.action == 'create':
            return Expense_itemCreateSerializer  #сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
        return Expense_itemDetailSerializer



    # def get_queryset(self): #Поиск расхода по id_накладной расхода (api/expenses_item/?expense_id=1)
    #     expense_id = self.request.query_params.get('expense_id')
    #     if expense_id:
    #         return Expense_item.objects.filter(expense_id=expense_id)
    #     return super().get_queryset()

    def list(self, request, *args, **kwargs): #Поиск расхода по id_накладной расхода (api/expenses_item/?expense_id=1 без пагинации)
        expense_id = request.query_params.get('expense_id')

        if expense_id:
            queryset = Expense_item.objects.filter(expense_id=expense_id)
        else:
            queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



    #Поиск по параметрам : 1) даты с по, 2) дата с по + поставщик, 3) дата с по + товар, 4)дата с по + клиент + товар
    # filter_by_expense_item/?start_date=2023-01-01&end_date=2023-12-31&provider_id=10&product_id=94
    @action(detail=False, methods=['get'])
    def filter_by_expense_item(self, request):
        queryset = self.get_queryset()

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        provider_id = request.query_params.get('provider_id')
        product_id = request.query_params.get('product_id')

        if start_date:
            queryset = queryset.filter(expense__expense_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(expense__expense_date__lte=end_date)

        if provider_id:
            queryset = queryset.filter(expense__provider__id=provider_id)

        if product_id:
            queryset = queryset.filter(product__id=product_id)

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
    """ Объединение записей """

    def post(self, request, prod_id):
        try:
            prod = Stock.objects.get(pk=prod_id)
        except Stock.DoesNotExist:
            raise Http404("Товар не существует")

        with transaction.atomic():
            # Находим все записи с заданными параметрами товаров
            existing_stocks = Stock.objects.filter(
                product_id=prod.product_id,
                product_price=prod.product_price,
                product_country=prod.product_country,
                product_vendor=prod.product_vendor
            ).exclude(product_barcode="").order_by('id')

            if existing_stocks:
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

                    # Проверяем количество товара
                    if total_product_quantity == 0:
                        # Если количество равно 0, сохраняем значение stock
                        last_deleted_stock = stocks_to_merge.first().id

                        # Удаляем все объединенные записи, кроме последней
                        stocks_to_merge.exclude(id=last_deleted_stock).delete()

                        # Удаление из модели Income связанных записей с удаленными Stock
                        Income.objects.filter(stock=last_deleted_stock).delete()
                    else:
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
                        Income.objects.filter(stock__in=stocks_to_merge).update(stock_id=new_stock.id)

                        # Удаляем все объединенные записи, кроме новой
                        stocks_to_merge.exclude(id=new_stock.id).delete()

                        # Возвращаем информацию о новой записи и объединенных записях
                        merged_stocks_info = {
                            "new_stock": {"id": new_stock.id},
                            "merged_stocks": [{"id": stock.id} for stock in stocks_to_merge]
                        }
                        return Response(merged_stocks_info)

                    return Response({})


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all().order_by('-id')
    serializer_class = StockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__product_name', 'product__id']  #?search=AAAA (имя товара / ID товара)
    pagination_class = APIListPagination
    permission_classes = [IsAuthenticated]

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




    #Поиск с даты по дату + товар (filter_by_stock/?start_date=2023-01-01&end_date=2023-12-31&product_id=84)
    @action(detail=False, methods=['get'])
    def filter_by_stock(self, request):
        queryset = self.get_queryset()

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        product_id = request.query_params.get('product_id')

        if start_date:
            queryset = queryset.filter(income__invoice__product_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(income__invoice__product_date__lte=end_date)

        if product_id:
            queryset = queryset.filter(product_id=product_id)


        serializer = StockSerializer(queryset, many=True)
        return Response(serializer.data)






    # Замена строк где есть одинаковые параметры ввода и обновление последневведенных + замена id обновленного stock в таблицу income
    #@receiver(pre_save, sender=Stock) - это выше в отдельной функции class UpdateStock(APIView):



    # Поиск товаров от одного до пяти слов и артикула. Список всех товаров связанных с первым словом +  список всех товаров с вторым словом и так далее
    #(/api/stocks/filter_by_keyword/?query=рамка+дом+артикул+страна в числовом значении)

    @action(detail=False, methods=['GET'])
    def filter_by_keyword(self, request):
        query = request.query_params.get('query', '')
        country_filter = request.query_params.get('country', '')

        queryset = Stock.objects.all().order_by('-id')

        if query or country_filter:
            keywords = query.split()
            product_name_query = Q()

            for keyword in keywords:
                product_name_query |= Q(product__product_name__icontains=keyword)

            results = queryset.filter(
                product_name_query |
                Q(product_vendor__icontains=query) |
                Q(product_country__icontains=query)
            )

            if country_filter:
                results = results.filter(product_country__icontains=country_filter)
        else:
            # Both query and country_filter are empty, return all rows
            results = queryset

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ContractCreateSerializer  #сериализатор для POST-запросов (GET показывает весь список, POST оставляет ID)
        return ContractDetailSerializer


    def get_queryset(self): #Поиск договоров по номеру договора (api/contracts/?contract_number=123)
        contract_number = self.request.query_params.get('contract_number')
        if contract_number:
            return Contract.objects.filter(contract_number=contract_number)
        return super().get_queryset()



   #Поиск по двум параметрам где номер контракта по цифре все данные,или есть пустой запрос то весь список выдает (api/contracts/search_by_client_and_number/?provider_id=4&contract_number=1234)
    @action(detail=False, methods=['GET'])
    def search_by_client_and_number(self, request):
        provider_id = request.query_params.get('provider_id')
        contract_number = request.query_params.get('contract_number')

        if not provider_id:
            return Response({"message": "Не указан параметр provider_id"}, status=status.HTTP_400_BAD_REQUEST)

        contracts = Contract.objects.filter(provider_id=provider_id)

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
    permission_classes = [IsAuthenticated]

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












