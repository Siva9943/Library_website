from django.shortcuts import render,redirect
from lib.form import Validate_form
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import datetime
from django.db import transaction
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# tracking/views.py
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import GPSPoint, TractorSession


def tracker_view(request):
    return render(request, 'tractor.html')
@csrf_exempt
def save_gps(request):
    data = json.loads(request.body)
    lat = data['lat']
    lng = data['lng']
    speed = data['speed']

    session = TractorSession.objects.last()  # simplify for now
    GPSPoint.objects.create(session=session, latitude=lat, longitude=lng, speed=speed)
    return JsonResponse({'status': 'saved'})

def student_signup(request):
    username=request.POST.get('username')
    email=request.POST.get('email')
    form=Validate_form()
    if request.method=='POST':
        form=Validate_form(request.POST)
        if form.is_valid():
            form.save()
            admin_user = User.objects.filter(email=email).first()
            user_id = admin_user.id
            user_details = StudentDetails(username = request.POST.get('username'),
            email = request.POST.get('email'),user_id = user_id)
            user_details.save()
            return redirect('/login')
        else:
         return HttpResponse("<script>alert('Please Check your Form!'); window.location.href='/signup';</script>")
    return render(request,'student_signup.html')

def login_user(request):
    if request.method=='POST':
        name=request.POST.get('Name')
        password=request.POST.get('Password')
        try:
            user = authenticate(request, username=name, password=password)
            if user is not None:
                login(request, user) 
                if user.is_superuser:  
                    return redirect('/admin_dashboard')  
                else:
                    student = StudentDetails.objects.filter(user_id=user.id).first()
                    if student and student.status == 1:
                        return redirect('/take_book')
                    return redirect('/student_dashboard') 
            else:
                return redirect('/login') 
        except Exception as e:
            print(f"Login error: {e}") 
    return render(request,'login.html')
def admin_login(request):
    obj = BookDetails.objects.all() 
    return render(request,'admin_dashboard.html',{'obj': obj})
def student_login(request):
    student=StudentDetails.objects.all()
    return render(request,'student_dashboard.html',{'student':student})
def logout_user(request):
    logout(request)  
    return redirect("index") 

def book_add(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            user_id = request.user.id
            BookDetails.objects.create(name=request.POST.get('Name'),
                                       book_code=request.POST.get('Code'),
                                       author_name=request.POST.get('Author'),
                                        date=request.POST.get('Date'),
                                        status=request.POST.get('Status'),
                                        amount=request.POST.get('Amount'),
                                        created_by=user_id,
                                        available_books = request.POST.get('available_books'),
                                        book_img = request.FILES.get('files',None))
            return redirect("bookdetails")
        else:
            return redirect("addbook")
    return render(request, 'add_book.html')

def index(request):
    return(
        render(request,'index.html')
    )

def book_details(request):
    obj = BookDetails.objects.all() 
    return render(request, 'admin_dashboard.html', {'obj': obj})

def updatebook(request,pk):
    obj=BookDetails.objects.get(id=pk)
    print(obj,"sivapraadss")
    if request.method=='POST':
        library = BookDetails.objects.filter(id=pk).first()
        library.name = request.POST.get('Name')
        library.book_code = request.POST.get('Code')
        library.author_name = request.POST.get('Author')
        library.date = request.POST.get('Date')
        library.amount = request.POST.get('Amount')
        library.available_books = request.POST.get('available_books')
        library.book_img = request.FILES['updatebook']
        date = datetime.now().date()
        library.updated_date = date
        library.updated_by = request.user.id
        library.save()
        return redirect('/book_details')
    print("done")
    return render(request,'updatebook.html',{'obj':obj})

def deletebook(request,pk):
    a = BookDetails.objects.filter(id=pk).first()
    a.delete()
    return redirect('/book_details')


def take_book(request):
    obj = BookDetails.objects.all()
    if request.method=='POST':
        book_name=request.POST.get('search')
        book_code=request.POST.get('searchcode')
        if book_code =='':
            obj  = BookDetails.objects.filter(name=book_name)
        if book_name == '':
            obj = BookDetails.objects.filter(book_code=book_code)
            
        
    return render(request,'take_book.html',{'obj':obj})

@transaction.atomic()
def takebook(request,pk):
        if request.user.is_authenticated:
            date = datetime.now().date()
            book_id = pk
            book_details = BookDetails.objects.filter(id = book_id).first()
            if book_details.available_books != 0:
                book_name = book_details.name
                book_code = book_details.book_code
                book_price = book_details.amount
                book_quantity = book_details.available_books
                student_details = StudentDetails.objects.filter(user_id = request.user.id).first()
                student_id = student_details.id
            # reduce amount
                user_amount = student_details.wallet_balance
                current_amount = user_amount - book_price
                student_details.wallet_balance = current_amount
                student_details.save()
            
                book_history = BookTransferHistory(student_id = student_id,
                                                code = book_code,
                                                book_name = book_name,
                                                status = "Take")
                book_history.save()
                    
                #UserBookstatus Registeration
                status = UserBookStatus(student_id=student_id,book_id = book_id)
                status.save()

                #UserBookDetails Registeration
                user = UserBookDetails.objects.filter(student_id = student_id).first()
                if user is  None:
                    user_book_details = UserBookDetails(student_id = student_id,
                                                books_quantity = 1,created_at = date)
                    user_book_details.save()
                else:
                    user_update = UserBookDetails.objects.filter(student_id = student_id).first()
                    books_quantity = user_update.books_quantity 
                    quantity = int(books_quantity) +1
                    user_update.books_quantity = quantity
                    user_update.save()

                #Books reduction in BookDetails
                book_details = BookDetails.objects.filter(id = book_id).first()
                quantity = book_details.available_books
                quantity -= 1

                book_details.available_books = quantity
                if quantity == 0:
                    book_details.status = 'Unavailable'
                book_details.save()
            else:
                print("No stocks")
            return redirect('/take_book')

@transaction.atomic()
def retainbook(request,pk):
    if request.user.is_authenticated:
        user_id = request.user.id
        book_id = pk
        student = StudentDetails.objects.filter(user_id = user_id).first()
        student_id = student.id
        user_book = UserBookStatus.objects.filter(student_id=student_id,book_id=book_id).first()
        if user_book is not None:
            if user_book.status == 1:
                book_details = BookDetails.objects.filter(id = book_id).first()
                book_name = book_details.name
                book_code = book_details.book_code
                book_price = book_details.amount
                # history book
                book_history = BookTransferHistory(student_id = student_id,code = book_code,
                                                    book_name = book_name,status = "Return")
                book_history.save()
                books_reduction = UserBookDetails.objects.filter(student_id = student_id).first()
                book_quantity = books_reduction.books_quantity
                quantity = book_quantity-1
                books_reduction.books_quantity = quantity
                books_reduction.save()
# update book
                book_details = BookDetails.objects.filter(id = book_id).first()
                quantity = book_details.available_books
                quantity+=1
                book_details.available_books = quantity
                if quantity !=0:
                    book_details.status = 'Available'
                book_details.save()
                user_book.delete()
            else:
                print("you dont have book so you are not able to return")

        else:
            print("please purchase book")


                
    return redirect('/take_book')
