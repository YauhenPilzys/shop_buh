from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Client(models.Model):
    #Клиент справочник
    client_name = models.CharField("Название клиента", max_length=255, blank=False)
    client_phone = models.CharField("Номер телефона", max_length=15, blank=True, null=True)
    client_address = models.CharField("Адрес", max_length=255)
    client_unp = models.CharField("УНП", max_length=150)
    client_payment_code = models.CharField("Код платежа", max_length=255)
    bank = models.ForeignKey("Bank", on_delete=models.CASCADE, verbose_name="Банк")
    client_comment = models.TextField("Комментарий", blank=True, null=True)


    class Meta:
         verbose_name = "Клиент"
         verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.client_name





class Provider(models.Model):
    #Поставщик справочник
    provider_name = models.CharField("Название поставщика", max_length=255)
    provider_phone = models.CharField("Номер телефона", max_length=25)
    provider_address = models.CharField("Адрес", max_length=255)
    provider_unp = models.CharField("УНП", max_length=255)
    provider_payment_code = models.CharField("Код платежа", max_length=255)
    bank = models.ForeignKey("Bank", on_delete=models.CASCADE, verbose_name="Банк")
    provider_comment = models.TextField("Комментарий", blank=True, null=True)


    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return self.provider_name



class Product(models.Model):
    #Продукты(товар) справочник
    product_name = models.CharField("Название", max_length=255)
    product_group = models.ForeignKey("group", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Группа")
    product_unit = models.CharField("Единица измерения", max_length=10)





    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.product_name



class Group(models.Model):
    #Группы справочник
    group_name = models.CharField("Название группы", max_length=255)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.group_name



class Invoice(models.Model):
    #Накладная прихода
    providers = models.ForeignKey("Provider", on_delete=models.CASCADE, verbose_name="Поставщик")
    invoice_number = models.CharField("Номер накладной", max_length=100)
    product_date = models.DateField("Дата поступления ", blank=False)
    product_price = models.DecimalField("Цена по накладной", max_digits=10, decimal_places=2)
    product_price_nds = models.DecimalField("Цена с НДС", max_digits=10, decimal_places=2)


    class Meta:
        verbose_name = "Накладная"
        verbose_name_plural = "Накладные"

    def __str__(self):
        return f"id : {self.id} / накладная № #{self.invoice_number} "



class Income(models.Model):
    #Приход
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="Товар")
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, verbose_name="Накладная" )
    product_vendor_providers = models.CharField("Артикул товара поставщика ",max_length=100, blank=True, null=True )
    income_quantity = models.PositiveIntegerField("Количество", default=0)
    product_country = models.CharField("Страна товара", max_length=255)
    product_barcode = models.CharField("Штрихкод товара", max_length=255)
    income_purchase_price = models.DecimalField("Закупочная цена", max_digits=10, decimal_places=2)
    income_vat = models.PositiveIntegerField("НДС", default=0)
    total_price_income = models. DecimalField("Полная цена с ндс", max_digits=10, decimal_places=2)


    class Meta:
        verbose_name = "Приход"
        verbose_name_plural = "Приходы"

    def __str__(self):
        return f"Получили товар :{self.product} в количестве {self.income_quantity}  "





class Expense(models.Model):
    #Расход
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name="Клиент")
    expense_number = models.CharField("Номер по накладной", max_length=100)
    expense_price = models.DecimalField("Стоимость", max_digits=10, decimal_places=2)
    expense_price_allowance = models.DecimalField("Стоимость с надбавкой", max_digits=10, decimal_places=2)
    expense_vat = models.CharField("Сумма НДС ", max_length=100, blank=True, null=True)
    expense_date = models.DateField("Дата продажи",  blank=False)
    number_proxy = models.CharField("Номер доверенности", max_length=100, blank=True, null=True)
    date_proxy = models.DateField ("Дата доверенности", blank=True, null=True)     # могут быть пустые
    proxy_user = models.CharField("Кем выдана довереннось", max_length=100, blank=True, null=True)
    # expense_doc в ручную документы

    class Meta:
        verbose_name = "Расход"
        verbose_name_plural = "Расходы"

    def __str__(self):
        return f"Продано кому: {self.client}  "

class Expense_item(models.Model):
    #Расходная продажи
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="Товар")
    expense = models.ForeignKey('Expense', on_delete=models.CASCADE, verbose_name="Расходная накладная")
    product_vendor = models.CharField("Артикул товара", max_length=100)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Группа")
    price_provider = models.CharField("Цена поставщика", max_length=100)
    product_quantity = models.CharField("Количество товара для продажи", max_length=100)
    product_vat = models.CharField("НДС", max_length=20)
    product_extra = models.CharField("Надбавка", max_length=100)
    total_price_expense = models.CharField("Общая цена с НДС, надбавкой и количеством", max_length=100)
    product_country = models.CharField("Страна товара", max_length=100)
    product_barcode = models.CharField("Штрихкод товара", max_length=100)


    class Meta:

        verbose_name = "Расходная продажи"
        verbose_name_plural = "Расходная продажи"

    def __str__(self):
        return str(self.product)





class Retail(models.Model):
    #Розничная торговля
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="Товар")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name="Группа")
    product_vendor = models.CharField("Артикул товара", max_length=100)
    product_country = models.CharField("Страна товара", max_length=100)
    product_barcode = models.CharField("Штрихкод товара", max_length=100)
    product_vat = models.CharField("НДС", max_length=20)
    product_extra = models.CharField("Надбавка", max_length=100)
    product_quantity = models.CharField("Количество товара", max_length=100)
    total_price_vat = models.DecimalField("Общая цена с НДС", max_digits=10, decimal_places=2)
    full_price = models.DecimalField("Общая цена с ндс и надбавкой", max_digits=10, decimal_places=2)
    date_item = models.DateField("Дата выставления чека",  blank=False)
    #paymant оплата картой или наличными добавить


    class Meta:

        verbose_name = "Розничная торговля"
        verbose_name_plural = "Розничная торговля"

    def __str__(self):
        return str(self.product)




class Price_change(models.Model):
    #Изменение цены (корректировка)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="Товар")
    price_change_date = models.DateField("Дата изменения цены", blank=True)
    expense_sale_price = models.DecimalField("Старая цена со склада", max_digits=10, decimal_places=2)
    price_change_new = models.DecimalField("Новая цена", max_digits=10, decimal_places=2)

    class Meta:

        verbose_name = "Изменение цены"
        verbose_name_plural = "Изменение цены"

    def __str__(self):
        return str(self.product)





class Bank(models.Model):
    #Банк справочник
    bank_name = models.CharField("Название банка", max_length=255)
    bank_bik = models.CharField("БИК банка", max_length=25)


    class Meta:
        verbose_name = "Банк"
        verbose_name_plural = "Банки"

    def __str__(self):
        return self.bank_name


class Contract(models.Model):
    #Договор
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name="Клиент")
    contract_number = models.CharField("Номер договора", max_length=100)
    contract_date = models.DateField("Дата договора", blank=False)


    class Meta:
        verbose_name = "Договор"
        verbose_name_plural = "Договора"

    def __str__(self):
        return f"Номер договора: {self.contract_number} "



class Stock(models.Model):
    #Склад
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="Товар")
    product_quantity = models.CharField("Количество товара", max_length=255)
    product_country = models.CharField("Страна товара", max_length=255)
    product_vendor = models.CharField("Артикул товара", max_length=255)
    product_reserve = models.CharField("Резерв товара", max_length=255, blank=True, null=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name="Группа", blank=True, null=True)
    expense_allowance = models.DecimalField("Цена с надбавкой", max_digits=10, decimal_places=2)
    product_price = models.CharField("Общая цена без ндс", max_length=255)
    product_vat = models.CharField("НДС", max_length=255)
    expense_full_price = models.CharField("Общая цена с ндс", max_length=100, null=True, blank=True)
    product_barcode = models.CharField("Штрихкод", max_length=255)



    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склад"

    def __str__(self):
        return f" id {self.id} - {self.product} - количество {self.product_quantity} шт "

#@receiver(pre_save, sender=Stock) #перемножить две строчки значением string
#def calculate_multiplication_result(sender, instance, **kwargs):
#    result = str(int(instance.product_quantity) * int(instance.product_price))
#    instance.expense_full_price = result




