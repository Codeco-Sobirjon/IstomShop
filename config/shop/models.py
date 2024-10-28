from django.db import models



class Service(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name='Заголовок')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        db_table = "table_service"


class OurPartner(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Заголовок')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Our Partner"
        verbose_name_plural = "Our Partners"
        db_table = "table_our_partner"


class Consultant(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Заголовок')
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name="Телефон")
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Consultant"
        verbose_name_plural = "Consultants"
        db_table = "table_consultant"


PRICE_TYPE = (
    ('USD', 'USD'),
    ('UZS', 'UZS'),
    ('RUB', 'RUB'),
)


class Banner(models.Model):
    header = models.CharField(max_length=200, null=True, blank=True, verbose_name='Главный заголовок')
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name='Заголовок')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    discount = models.IntegerField(null=True, blank=True, verbose_name='Скидка')
    price = models.IntegerField(null=True, blank=True, verbose_name='Цена')
    price_type = models.CharField(max_length=200, null=True, blank=True, choices=PRICE_TYPE, default='RUB', verbose_name='Тип цены')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        db_table = "table_banner"


class MainCategories(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Main Categories"
        verbose_name_plural = "Main Categories"
        db_table = "table_main_categories"


class SubCategory(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Имя")
    main_categories = models.ForeignKey(MainCategories, on_delete=models.CASCADE, null=True, blank=True, related_name="mainCategories", verbose_name='Главная категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sub Categories"
        verbose_name_plural = "Sub Categories"
        db_table = "table_categories"


class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Имя")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    price = models.IntegerField(null=True, blank=True, verbose_name="Цена")
    quantity = models.IntegerField(null=True, blank=True, verbose_name="Количество")
    price_type = models.CharField(max_length=200, null=True, blank=True, choices=PRICE_TYPE, default='RUB', verbose_name="Тип цены")
    vendor_code = models.CharField(max_length=200, null=True, blank=True, verbose_name="Артикул")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True, related_name="categoryProduct", verbose_name="Подкатегория")
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Изображение")
    characteristics = models.JSONField(null=True, blank=True, verbose_name="Характеристики")
    advantages = models.JSONField(null=True, blank=True, verbose_name="Преимущества")
    manufactured_city = models.CharField(max_length=200, null=True, blank=True, verbose_name="Город производства")
    firm = models.CharField(max_length=200, null=True, blank=True, verbose_name="Твердый")
    created_at = models.DateField(null=True, blank=True, verbose_name="Дата")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "table_product"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name="productImage", verbose_name="Продукт")
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Изображение")

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        db_table = "table_product_image"


class ProductCard(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name="productCard", verbose_name="Продукт")
    quantity = models.IntegerField(null=True, blank=True, verbose_name="Количество")
    total_price = models.IntegerField(null=True, blank=True, verbose_name="Итоговая цена")
    price_type = models.CharField(max_length=200, null=True, blank=True, choices=PRICE_TYPE, default='RUB', verbose_name="Тип цены")
    full_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Полное имя")
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name="Телефон")
    email = models.EmailField(null=True, blank=True, verbose_name="Электронная почта")
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name="Адрес")
    created_at = models.DateField(null=True, blank=True, auto_now_add=True, verbose_name="Дата")

    # def __str__(self):
    #     return self.product.name

    class Meta:
        verbose_name = "Product Card"
        verbose_name_plural = "Product Cards"
        db_table = "table_product_card"