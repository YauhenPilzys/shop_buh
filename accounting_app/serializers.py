from rest_framework import serializers
from .models import Client, Product, Provider, Group, Invoice, Bank, Expense, Stock, Price_change, Income, Expense_item, \
    Retail


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    bank = BankSerializer()
    class Meta:
        model = Client
        fields = '__all__'


class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ClientDetailSerializer(serializers.ModelSerializer):
    bank = BankSerializer()

    class Meta:
        model = Client
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'



class InvoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'



class BankCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = '__all__'


class ProviderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'



class ProviderDetailSerializer(serializers.ModelSerializer):
    bank = BankSerializer()
    class Meta:
        model = Provider
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    providers = ProviderSerializer()

    class Meta:
        model = Invoice
        fields = '__all__'





class ExpenseSerializer(serializers.ModelSerializer):
    clients = ClientSerializer()
    class Meta:
        model = Expense
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
   # product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    product = ProductSerializer()
    class Meta:
        model = Stock
        fields = '__all__'



class StockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'





class StockDetailSerializer(serializers.ModelSerializer):
    #Вывод всех продуктов в GET запросе
    product = ProductSerializer()
    #invoice = InvoiceSerializer()

    class Meta:
        model = Stock
        fields = '__all__'


class Price_changeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price_change
        fields = '__all__'



class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = '__all__'




class IncomeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'





class IncomeDetailSerializer(serializers.ModelSerializer):
    #Вывод всех продуктов в GET запросе
    product = ProductSerializer()
    invoice = InvoiceSerializer()

    class Meta:
        model = Income
        fields = '__all__'


class Expense_itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense_item
        fields = '__all__'





class RetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retail
        fields = '__all__'







