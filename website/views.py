from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'successfully Logged In!')
            return redirect('home')
        else:
            messages.success(request, 'Error Logging In,Try Again')
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})

def logout_user(request):
    logout(request)
    messages.success(request, 'You Have Been Logged Out Successfully')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You Have Successfully Registered,Welcome!')
            return redirect('home')
    else:
        form = SignUpForm()
        return render (request, 'register.html', {'form':form})
    
    return render (request, 'register.html', {'form':form})


def customer_records(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, 'You Must Be Logged In To View Customer\'s records') 
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        dlt = Record.objects.get(id=pk)
        dlt.delete()
        messages.success(request, 'Record Successfully Deleted...')
        return redirect('home')
    else:
        messages.success(request, 'You Must Be Logged In To Delete Customer\'s Record')
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record Successfully Added!')
                return redirect('home')
        else:
            return render(request, 'add.html', {'form':form})
    else:
        messages.success(request, 'You Have To Be Logged In To Add Record')
        return redirect('home')


def update_record(request,pk):
    if request.user.is_authenticated:
        old = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=old)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated Successfully')
            return redirect('home')

        else:
            return render (request, 'update.html', {'form':form})

    else:
        messages.success(request, 'You Must Be Logged In To Update Record')
        return redirect('home')
