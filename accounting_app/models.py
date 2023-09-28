from django.db import models


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
    #Продукты(товар)справочник
    product_name = models.CharField("Название", max_length=255)
    product_vendor = models.CharField("Артикул", max_length=255)
    product_group = models.ForeignKey("group", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Группа")
    product_unit = models.CharField("Единица измерения", max_length=10)
    product_description = models.TextField("Дополнительная информация", blank=True, null=True)




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
    #Накладная (приход)
    providers = models.ForeignKey("Provider", on_delete=models.CASCADE, verbose_name="Поставщик")
    invoice_number = models.CharField("Номер накладной", max_length=100)
    product_date = models.DateField("Дата поступления ", blank=False)
    product_price = models.DecimalField("Цена по накладной", max_digits=10, decimal_places=2)
    product_price_nds = models.DecimalField("Цена с НДС", max_digits=10, decimal_places=2)



    class Meta:
        verbose_name = "Накладная"
        verbose_name_plural = "Накладные"


    def __str__(self):
        return f"Invoice #{self.invoice_number} / id : {self.id}  "



class Expense(models.Model):
    #Накладная (расход)
    clients = models.ForeignKey("Client", on_delete=models.CASCADE, verbose_name="Клиент")
    expense_number = models.CharField("Номер накладной", max_length=100)
    expense_price = models.DecimalField("Цена продажи", max_digits=10, decimal_places=2)
    expense_nds = models.DecimalField("Цена с ндс ", max_digits=10, decimal_places=2)
    expense_date = models.DateField("Дата продажи",  blank=False)



    class Meta:
        verbose_name = "Расход"
        verbose_name_plural = "Расходы"

    def __str__(self):
       return f"Продано : {self.clients} за {self.expense_price} р. "



class Price_change(models.Model):
    #Изменение цены
    product_name = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="Товар")
    price_change_date = models.DateField("Дата изменения цены", blank=True)
    expense_sale_price = models.DecimalField("Старая цена со склада", max_digits=10, decimal_places=2)
    #разрешить чтоб поля были пустые работали (от Виталика)
    price_change_new = models.DecimalField("Новая цена", max_digits=10, decimal_places=2)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE, verbose_name="Склад")


    class Meta:
        verbose_name = "Изменение цены"
        verbose_name_plural = "Изменение цены"




class Bank(models.Model):
    #Банк справочник
    bank_name = models.CharField("Название банка", max_length=255)
    bank_bik = models.CharField("БИК банка", max_length=25)


    class Meta:
        verbose_name = "Банк"
        verbose_name_plural = "Банки"

    def __str__(self):
            return self.bank_name



class Stock(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, verbose_name="Накладная")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="Товар")
    product_quantity = models.CharField("Количество товара", max_length=100)
    product_country = models.CharField("Страна товара", max_length=255)
    expense_sale_price = models.DecimalField("Цена продажи за один товар", max_digits=10, decimal_places=2)


    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склад"


    def __str__(self):
       return f"Номер : {self.invoice}  {self.product} "