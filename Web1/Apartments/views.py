from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm, AddApartmentForm, ImageForm, RequestForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Apartment, Image, Request, User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import transaction
import pyautogui as pag


def Home(req):
    return render(req, 'Home.html')


def Login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            return redirect('register')

    form = LoginForm()
    return render(request, 'Login.html', {'form': form})


def Register(req):
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            pag.alert(text="נרשמת בהצלחה!✔", title="jhh")
            return redirect('home')
        else:
            return HttpResponse("ops form not valid")

    form = RegisterForm()
    return render(req, 'Register.html', {'form': form})


@login_required(login_url='/login')
def AddApartment(request):
    if request.user.status == 1:
        return HttpResponse("oooooops you are not valid ❌")
    print(request.user)
    if request.method == 'POST':
        form = AddApartmentForm(request.POST, request.FILES)
        if form.is_valid():
            # יצירת אובייקט אך לא שמירתו
            apartment = form.save(commit=False)
            apartment.seller = request.user  # הקצאת המוכר (המשתמש הנוכחי)
            apartment.save()  # שמירת האובייקט אחרי הקצאת המוכר

            # טיפול בתמונות
            if 'MainImages' in request.FILES:
                images = request.FILES.getlist('MainImages')  # קבלת כל הקבצים שהועלו
                for image_file in images:
                    # יצירת אובייקט Image לכל תמונה שהועלתה
                    Image.objects.create(apartmentID=apartment, url=image_file)

            return redirect('SellerList')
        else:
            pag.alert(text="הטופס לא וליד", title="jhh")
    else:
        form = AddApartmentForm()

    return render(request, 'edit.html', {'form': form})


@login_required(login_url='/login')
def UpdateApartment(request, apartment_id):
    if request.user.status == 1:
        return HttpResponse("oooooops you are not valid ❌")
    apartment = GetApartmentById(apartment_id)

    if request.method == 'POST':
        form = AddApartmentForm(request.POST, instance=apartment)
        if form.is_valid():
            apartment_ = form.save()
            apartment_.seller = request.user
            return redirect('SellerList')
    else:
        form = AddApartmentForm(instance=apartment)

    return render(request, 'edit.html', {'form': form, 'apartment': apartment})

@login_required(login_url='/login')
def UpdateBuy(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    print(apartment)
    apartment.Status=True
    print(apartment)
    apartment.save()
    user = request.user
    apartments = Apartment.objects.filter(seller=user)
    data = {
        'apartments': apartments
    }

    return render(request, 'SellerList.html')
def SellerList(request):
    user = request.user
    apartments = Apartment.objects.filter(seller=user)

    data = {
            'apartments': apartments
         }
    return render(request, 'SellerList.html', data)


def GetApartmentById(apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    return apartment



def show(request, apartment_id):
    print(apartment_id)
    # אנחנו לוקחים את הפניות שקשורות לדירה עם ה-ID הזה
    apartment_requests = Request.objects.filter(apartmentID=apartment_id)
    print(apartment_requests)
    data = {
        'request': apartment_requests
    }

    return render(request, 'request.html', data)


def DeleteApartment(request, apartment_id):

    apartment = GetApartmentById(apartment_id)
    apartment.delete()
    pag.alert(text="נמחק בהצלחה", title="מחיקה")
    return redirect('SellerList')


def CustomerList(request):
    # אם לא הוזן חיפוש (שדות ריקים)
    search_type = request.GET.get('SearchType', None)
    search_value = request.GET.get('Search', '').strip()
    min_price = request.GET.get('MinSort', '').strip()
    max_price = request.GET.get('MaxSort', '').strip()

    # אם לא הוזן חיפוש או שהשדות ריקים, הצג את כל הדירות
    apartments = Apartment.objects.filter(Status=False)

    # מסננים אם הוזן חיפוש
    if search_value:
        if search_type == "city":
            apartments = apartments.filter(city=search_value,Status=False)
        elif search_type == "numberRoom":
            apartments = apartments.filter(rooms=search_value,Status=False)
        elif search_type == "floor":
            apartments = apartments.filter(floor=search_value,Status=False)

    # אם הוזנו טווחי מחירים
    if min_price and max_price:
        apartments = apartments.filter(price__gte=min_price, price__lte=max_price,Status=False)
    elif min_price:
        apartments = apartments.filter(price__gte=min_price,Status=False)
    elif max_price:
        apartments = apartments.filter(price__lte=max_price,Status=False)

    images = Image.objects.all()
    for apartment in apartments:
        apartment.final_price = apartment.price + (apartment.seller.commission / 100 * apartment.price)

    data = {
        'apartments': apartments,
        'images': images,
    }
    return render(request, 'CustomerList.html', data)


@login_required(login_url='/login')
def create_request(request, apartment_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        user = request.user
        print(request.POST.get('content'))
        form = RequestForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['content']
            apartment = get_object_or_404(Apartment, id=apartment_id)

            new_request = Request.objects.create(
                apartmentID=apartment,  # שמו של השדה צריך להיות אובייקט, לא מזהה
                content=text,
                sendUser=user
            )
            print(new_request)
            if new_request is not None:
                return redirect('CustomerList')
            else:
                pag.alert(text="הטופס לא וליד", title="jhh")
        else:
            print(form.errors)
    else:
        form = RequestForm()

    return render(request, 'CustomerList.html', {'form': form})


def logout_and_clear_session(request):
    logout(request)  # מבצע יציאה (logout) ומנקה את ה-session
    return redirect('home')