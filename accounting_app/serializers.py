from rest_framework import serializers
from .models import Client, Product, Provider, Group, Invoice, Bank, Expense, Stock, Price_change


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Stock
        fields = '__all__'


class StockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class StockDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    invoice = InvoiceSerializer()

    class Meta:
        model = Stock
        fields = '__all__'


class Price_changeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price_change
        fields = '__all__'






