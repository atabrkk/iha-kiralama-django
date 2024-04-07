from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Uav, Rental, Category
from .forms import UavForm, RentalForm


# Create your views here.


def get_all_uav(request):
    uavs = Uav.objects.filter(status='Active')
    context = {
        'uavs': uavs
    }
    return render(request, 'uavs.html', context)


def uav_list_filtered(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    uavs = Uav.objects.filter(status='Active')

    if min_price:
        uavs = uavs.filter(price__gte=min_price)
    if max_price:
        uavs = uavs.filter(price__lte=max_price)

    context = {
        'uavs': uavs
    }
    return render(request, 'uavs.html', context)


def search(request):
    """
       Arama yapmak için kullanılan view fonksiyonu.

       GET parametresi olarak 'keyword' beklenir. Bu anahtar kelimeye
       göre UAV (Unmanned Aerial Vehicle) nesnelerini filtreler ve
       'name', 'features' ve 'brand' alanlarında anahtar kelimeyi içeren
       nesneleri getirir. 'status' alanı 'Active' olan nesneler arasında
       filtreleme yapılır.

       Context olarak 'uavs' adında bir liste ve 'keyword' adında bir string
       içeren bir sözlük döndürür. 'uavs' listesi, anahtar kelimeyi içeren ve
       'status' alanı 'Active' olan UAV nesnelerini içerir. 'keyword' ise
       kullanıcının arama yaparken kullandığı anahtar kelimeyi içerir.

       :param request: Django HTTP request nesnesi
       :return: Django HTTP response nesnesi, 'search.html' şablonu ile render edilir.
       """
    keyword = request.GET.get('keyword')
    uavs = Uav.objects.filter(
        Q(name__icontains=keyword) | Q(features__icontains=keyword) | Q(brand__icontains=keyword),
        status='Active')
    context = {
        'uavs': uavs,
        'keyword': keyword
    }
    return render(request, 'search.html', context)


@login_required
def search_reservations(request):
    user = request.user
    keyword = request.GET.get('keyword')
    reservations = Rental.objects.filter(
        Q(start_date__icontains=keyword) | Q(total_price__icontains=keyword), user=user)
    context = {
        'reservations': reservations,
        'keyword': keyword
    }
    return render(request, 'search_reservations.html', context)


def get_uav(request, slug):
    single_uav = get_object_or_404(Uav, status='Active', slug=slug)
    context = {
        'single_uav': single_uav
    }
    return render(request, 'uav.html', context)


def add_uav(request):
    """
       UAV (Unmanned Aerial Vehicle) eklemek için kullanılan view fonksiyonu.

       POST metoduyla çağrıldığında, kullanıcıdan gelen verileri kullanarak bir
       UavForm nesnesi oluşturur. Form geçerli ise, veritabanına kaydeder ve
       'all-uavs' URL'sine yönlendirir. GET metoduyla çağrıldığında ise boş bir
       UavForm nesnesi oluşturarak 'add_uav.html' şablonunu render eder.

       :param request: Django HTTP request nesnesi
       :return: Django HTTP response nesnesi, 'add_uav.html' şablonu ile render edilir.
       """
    if request.method == 'POST':
        form = UavForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all-uavs')
    form = UavForm()
    context = {
        'form': form
    }
    return render(request, 'add_uav.html', context)


def edit_uav(request, slug):
    uav = get_object_or_404(Uav, slug=slug)
    if request.method == 'POST':
        form = UavForm(request.POST, request.FILES, instance=uav)
        if form.is_valid():
            form.save()
            return redirect('all-uavs')
    form = UavForm(instance=uav)
    context = {
        'form': form,
        'uav': uav
    }
    return render(request, 'edit_uav.html', context)


def delete_uav(request, slug):
    uav = get_object_or_404(Uav, slug=slug)
    uav.delete()
    return redirect('all-uavs')


def edit_user_uav(request, pk):
    user = request.user
    rental = get_object_or_404(Rental, id=pk, user=user)
    if request.method == 'POST':
        form = RentalForm(request.POST, instance=rental)
        if form.is_valid():
            total_days = (rental.end_date - rental.start_date).days * rental.uav.price
            rental.total_price = total_days
            form.save()
            return redirect('user_reservations')
    form = RentalForm(instance=rental)
    context = {
        'form': form,
        'rental': rental
    }
    return render(request, 'edit_user_uav.html', context)


def delete_user_uav(request, pk):
    rental = get_object_or_404(Rental, id=pk)
    rental.delete()
    return redirect('user_reservations')


@login_required
def create_rental(request, slug):
    """
        Bir UAV (Unmanned Aerial Vehicle) için kiralama oluşturmak için kullanılan view fonksiyonu.

        GET parametresi olarak 'slug' beklenir. Bu slug değeri kullanılarak ilgili
        UAV nesnesi getirilir. POST metoduyla çağrıldığında, kullanıcıdan gelen verileri
        kullanarak bir RentalForm nesnesi oluşturur. Form geçerli ise, kiralama nesnesini
        veritabanına kaydeder ve 'user_reservations' URL'sine yönlendirir.

        :param request: Django HTTP request nesnesi
        :param slug: UAV'nin slug değeri
        :return: Django HTTP response nesnesi, 'create_rental.html' şablonu ile render edilir.
        """
    uav = get_object_or_404(Uav, slug=slug)
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.user = request.user
            rental.uav = uav
            total_days = (rental.end_date - rental.start_date).days * uav.price
            rental.total_price = total_days
            rental.save()
            return redirect('user_reservations')
        else:
            print('form is invalid')
            print(form.errors)
    form = RentalForm()
    context = {
        'form': form,
        'uav': uav
    }
    return render(request, 'create_rental.html', context)


@login_required
def user_reservations(request):
    user = request.user
    user_reservations = Rental.objects.filter(user=user)
    context = {
        'user_reservations': user_reservations
    }
    return render(request, 'user_reservations.html', context)


def reservations_filtered(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    user_reservations = Rental.objects.all()

    if min_price:
        user_reservations = user_reservations.filter(total_price__gte=min_price)
    if max_price:
        user_reservations = user_reservations.filter(total_price__lte=max_price)

    context = {
        'user_reservations': user_reservations
    }
    return render(request, 'user_reservations.html', context)


def uavs_by_category(request, category_slug):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    uavs = Uav.objects.filter(status='Active', category__category_slug=category_slug)
    category = get_object_or_404(Category, category_slug=category_slug)
    context = {
        'uavs': uavs,
        'category': category
    }
    return render(request, 'uavs_by_category.html', context)