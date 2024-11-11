from django.shortcuts import render
from .models import Product
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from django.shortcuts import render, get_object_or_404
from .models import Product, Category  # Импортируем Category
from django.core.paginator import Paginator
from django.db.models import Q


def index(request):
    # Получаем последние 5 добавленных товаров
    new_products = Product.objects.filter(available=True).order_by('-created')[:5]
    # Получаем 5 самых популярных товаров по количеству просмотров
    popular_products = Product.objects.filter(available=True).order_by('-views')[:5]
    categories = Category.objects.all()
    return render(request, 'store/index.html', {
        'new_products': new_products,
        'popular_products': popular_products,
        'categories': categories,
    })


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    # Фильтрация по категории
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Фильтрация по производителю (например, передаём параметр 'manufacturer' в запросе)
    manufacturer = request.GET.get('manufacturer')
    if manufacturer:
        products = products.filter(manufacturer__icontains=manufacturer)

    # Фильтрация по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    # Поиск по названию или описанию
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Сортировка
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == 'popularity':
        products = products.order_by('-views')
    elif sort_by == 'newest':
        products = products.order_by('-created')
    else:
        products = products.order_by('name')

    # Пагинация
    paginator = Paginator(products, 12)  # Показывать 12 товаров на странице
    page = request.GET.get('page')
    products = paginator.get_page(page)

    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    # Увеличиваем количество просмотров
    product.views += 1
    product.save()
    return render(request, 'store/product_detail.html', {'product': product})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Аутентификация пользователя после регистрации
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('store:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'store/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Аутентификация пользователя
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store:index')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})