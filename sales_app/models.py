from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    position = models.CharField(max_length=100, verbose_name="Посада")
    phone = models.CharField(max_length=15, verbose_name="Телефон")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    class Meta:
        verbose_name = "Працівник"
        verbose_name_plural = "Працівники"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва товару")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    active = models.BooleanField(default=True, verbose_name="Активний")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"


class SalesPlan(models.Model):
    start_date = models.DateField(verbose_name="Дата початку")
    end_date = models.DateField(verbose_name="Дата закінчення")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    target_amount = models.IntegerField(verbose_name="Цільова кількість")

    def __str__(self):
        return f"План на {self.product.name} ({self.start_date} - {self.end_date})"

    class Meta:
        verbose_name = "План продажів"
        verbose_name_plural = "Плани продажів"


class Sale(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Працівник")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField(default=1, verbose_name="Кількість")
    date = models.DateTimeField(default=timezone.now, verbose_name="Дата продажу")

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.employee} продав {self.product.name} x{self.quantity}"

    class Meta:
        verbose_name = "Продаж"
        verbose_name_plural = "Продажі"