from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Employee, Product, Sale, SalesPlan
from .forms import SaleForm, SalesFilterForm


def home(request):
    # Основні показники для головної сторінки
    total_sales = Sale.objects.count()
    total_revenue = Sale.objects.aggregate(total=Sum('product__price'))['total'] or 0
    employees_count = Employee.objects.count()
    products_count = Product.objects.count()

    # Останні продажі
    recent_sales = Sale.objects.order_by('-date')[:5]

    return render(request, 'sales_app/home.html', {
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'employees_count': employees_count,
        'products_count': products_count,
        'recent_sales': recent_sales,
    })


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'sales_app/employee_list.html', {'employees': employees})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'sales_app/product_list.html', {'products': products})

def sales_list(request):
    sales = Sale.objects.all().order_by('-date')

    filter_form = SalesFilterForm(request.GET)

    if filter_form.is_valid():
        start_date = filter_form.cleaned_data.get('start_date')
        end_date = filter_form.cleaned_data.get('end_date')
        employee = filter_form.cleaned_data.get('employee')
        product = filter_form.cleaned_data.get('product')

        if start_date:
            sales = sales.filter(date__date__gte=start_date)
        if end_date:
            sales = sales.filter(date__date__lte=end_date)

        if employee:
            sales = sales.filter(employee=employee)

        if product:
            sales = sales.filter(product=product)

    return render(request, 'sales_app/sales_list.html', {'sales': sales, 'filter_form': filter_form})

def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продаж успішно додано!')
            return redirect('sales_list')
    else:
        form = SaleForm()

    return render(request, 'sales_app/add_sale.html', {'form': form})


def leaderboard(request):
    thirty_days_ago = timezone.now() - timedelta(days=30)

    # Отримуємо топ співробітників за кількістю продажів
    leaders = Employee.objects.annotate(
        sales_count=Count('sale', filter=Sale.objects.filter(date__gte=thirty_days_ago))
    ).order_by('-sales_count')[:10]

    return render(request, 'sales_app/leaderboard.html', {
        'leaders': leaders,
    })
def daily_stats(request):
    # Статистика за останні 7 днів
    seven_days_ago = timezone.now().date() - timedelta(days=7)

    daily_data = []
    for days_ago in range(7):
        date = timezone.now().date() - timedelta(days=days_ago)
        sales_count = Sale.objects.filter(date__date=date).count()
        revenue = Sale.objects.filter(date__date=date).aggregate(
            total=Sum('product__price'))['total'] or 0

        daily_data.append({
            'date': date,
            'sales_count': sales_count,
            'revenue': revenue
        })

    daily_data.reverse()  # Щоб показати від старих до нових

    return render(request, 'sales_app/daily_stats.html', {'daily_data': daily_data})