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
    # Таблиця лідерів за останні 30 днів
    thirty_days_ago = timezone.now() - timedelta(days=30)

    leaders = Employee.objects.annotate(
        sales_count=Count('sale', filter=Sale.objects.filter(date__gte=thirty_days_ago).values('id'))
    ).order_by('-sales_count')

    return render(request, 'sales_app/leaderboard.html', {'leaders': leaders})


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


def admin_dashboard(request):
    total_sales = Sale.objects.count()
    total_revenue = Sale.objects.aggregate(total=Sum('product__price'))['total'] or 0
    employees_count = Employee.objects.count()
    products_count = Product.objects.count()

    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)

    recent_sales = Sale.objects.order_by('-date')[:5]

    top_employees = Employee.objects.filter(sale__date__date__gte=last_30_days) \
                        .annotate(sales_count=Count('sale')) \
                        .order_by('-sales_count')[:5]

    active_plans = SalesPlan.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    )

    plans_progress = []
    for plan in active_plans:
        actual_sales = Sale.objects.filter(
            product=plan.product,
            date__date__gte=plan.start_date,
            date__date__lte=today
        ).aggregate(total=Sum('quantity'))['total'] or 0

        if plan.target_amount > 0:
            progress_percent = (actual_sales / plan.target_amount) * 100
        else:
            progress_percent = 0

        plans_progress.append({
            'plan': plan,
            'actual_sales': actual_sales,
            'progress_percent': progress_percent,
            'days_left': (plan.end_date - today).days
        })

    low_stock_products = Product.objects.filter(active=True, quantity__lt=10).order_by('quantity')[:5]

    return render(request, 'sales_app/admin_dashboard.html', {
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'employees_count': employees_count,
        'products_count': products_count,
        'recent_sales': recent_sales,
        'top_employees': top_employees,
        'plans_progress': plans_progress,
        'low_stock_products': low_stock_products,
    })