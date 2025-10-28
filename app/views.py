from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from task.settings import BASE_DIR
import os

# Create your views here.
from .models import Customuser,Category,Product




ROLES = ['seller','user']

def all_category():
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return context

def all_products():
    products = Product.objects.all()
    context = {
        'products' : products
    }
    return context



def home(request):
    return render(request,'app/home.html')



@login_required(login_url="user_login")
def products(request):
    role = request.session['role']
    if role == "user":
        context = all_products()
        paginator = Paginator(context['products'],5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context.update({'page_obj':page_obj})
        return render(request,'app/products.html',context)
    else:
        messages.add_message(request,messages.INFO,f"Invalid user needs a user role to access the page")
        return redirect("user_login")



def product_details(request,slug):
    title  = (slug.replace("-"," ")).title()
    product = Product.objects.get(title = title)
    context = {
        'product' : product
    }
    return render(request,'app/product_details.html',context)



def take_query(request):
    user = request.session['name']
    if request.method == 'POST':
        query = request.POST.get('search',"")
        print(query)
        order = request.POST['filter']
        print(order)
        if order == 'asc':
            products = Product.objects.all().order_by('price')
        elif order == 'desc':
            products = Product.objects.all().order_by('-price')
        paginator = Paginator(products,5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)       
        return render(request,'app/products.html',{'page_obj':page_obj,'user':user})
    return redirect('products')


# -----------------------------------------------------------------------------------------------------------------

#seller 
@login_required(login_url="user_login")
def add_products(request):
    context = all_category()
    role = request.session['role']
    if request.method == 'GET' and role == 'seller':
        return render(request,'app/add_products.html',context)
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        product_img = request.FILES["image"]
        price  = request.POST['price']
        category = request.POST['category']
        print(title,description,product_img,price,category)
        obj = Product(title=title,description=description,product_img=product_img,price=price,category=category)
        try:
            obj.save()
            messages.add_message(request,messages.INFO,'Product added successfully')
        except:
            messages.add_message(request,messages.INFO,'Product might already exist')
        return redirect("add_products")
    

@login_required(login_url="user_login")
def seller_dashboard(request):
    role = request.session['role']
    user = request.session['name']
    if role == 'seller':
        context = all_products()
        paginator = Paginator(context['products'],5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context.update({'page_obj':page_obj,'user': user})
        return render(request,'app/seller_dashboard.html',context)
    else:
        messages.add_message(request,messages.INFO,f"Invalid user needs a seller role to access the page")
        return redirect("user_login")


@login_required(login_url="user_login")
def delete_product(request,product_id):
    role = request.session['role']
    user = request.session['name']
    if role == 'seller':
        obj = Product.objects.get(id = product_id)
        context = all_products()
        paginator = Paginator(context['products'],5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context.update({'page_obj':page_obj,'user': user})
        img_path = obj.product_img.url
        try:
            os.remove(BASE_DIR/img_path)
            obj.delete()
            messages.add_message(request,messages.INFO,"Product deleted successfully")
        except FileNotFoundError:
            messages.add_message(request,messages.INFO,"Product is not found")
        except:
            messages.add_message(request,messages.INFO,"Product is not deleted")
       
        return render(request,'app/seller_dashboard.html',context)
        # return redirect('seller_dashboard',context)
    else:
        messages.add_message(request,messages.INFO,f"Invalid user needs a seller role to access the page")
        return redirect("user_login")
    
    







# -----------------------------------------------------------------------------------------------------------------




# login , logout  ,register

def user_register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        role  = request.POST['role']
        print(role)

        user = Customuser(first_name=fname.capitalize(),last_name=lname.capitalize(),username=username,email=email,phone=phone,role=role)
        user.set_password(password)
        try:
            user.save()
        except Exception as e:
            print(e)
            messages.add_message(request,messages.INFO,"User cannot be registered")
            return redirect('user_register')
        return redirect('user_login')
    return render(request,'app/register.html',{'roles':ROLES})


def user_login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            request.session['user_id'] = user.id 
            request.session["name"] = user.get_full_name()
            request.session['role'] = user.role
            if user.role == 'seller':
                return redirect('seller_dashboard')
            else:
                return redirect('products')
        else:
            messages.add_message(request,messages.INFO,"INVALID Credentials try login again !!!")
            return redirect("user_login")
    return render(request,'app/login.html')


def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect("home")