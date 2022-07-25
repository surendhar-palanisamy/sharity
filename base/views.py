from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponseRedirect
from django.contrib import messages
from hashlib import sha256
from .models import *
from .forms import *
from .algorithm import *
from .blockchain import *
import datetime
from .decorators import *
from django.contrib.auth.decorators import login_required

# Create your views here.

# display homepage


@login_required(login_url='login')
def home(request):
   
    return render(request, 'Home.html')

# signup page

@unauthenticated_user
def Signup(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Registration Successful!')
            return redirect('login')

    context = {'form': form}
    return render(request, 'Signup.html', context)

# login

@unauthenticated_user
def Login(request):
    if not request.session.exists(request.session.session_key):

        request.session.create()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        valid_user = authenticate(
            request, username=username, password=password)
        if valid_user is not None:
            login(request, valid_user)
            return redirect('home')
        else:
            messages.info(request, "Credentials incorrect! Try Again.")
    context = {}
    return render(request, 'Login.html', context)

# dislay profile of the current user(logged in user)

@login_required(login_url='login')
def Profile_fun(request):

    return render(request, 'Profile.html')

@login_required(login_url='login')
def Logout_fun(request):
    logout(request)
    return redirect('login')

# payment password hashing function


def hasher(text):
    if text is not None:
        return sha256(text.encode('ascii')).hexdigest()

# update profile of the user(logged in user)


def from_dob_to_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

@login_required(login_url='login')
def Updateprofile(request):

    paypass_one = request.POST.get('paypass1')
    paypass_two = request.POST.get('paypass2')
    user = request.user
    var = Profile.objects.get(user=user)
    form = Profilemodelform(instance=var)
    if paypass_one == paypass_two:

        if request.method == 'POST':
            form = Profilemodelform(request.POST, request.FILES, instance=var)

            if form.is_valid():
                instance = form.save(commit=False)
                paypass_one = hasher(paypass_one)

                instance.payment_password = paypass_one
                instance.save()
                if request.POST.get('dob'):
                    age = from_dob_to_age(instance.dob)
                    print('This is your age', age)
                    messages.success(request, "Profile Updated Successfully!")
                    return redirect('profile')

    else:
        messages.success(request, "Password didn't match!")

    context = {'form': form}
    return render(request, 'Updateprofile.html', context)

# list all the post in the website

@login_required(login_url='login')
def Postlist(request):
    # post_list = Post.objects.all().order_by(sort_factor)
    post_list = Post.objects.order_by('-sort_factor').filter(completed=False)
    
    paginator_object = Paginator(post_list, 6)
    page_num = request.GET.get('page', 1)

    try:
        page = paginator_object.page(page_num)
    except EmptyPage:
        page = paginator_object.page(1)
    context = {'posts': page}
    return render(request, 'Posts.html', context)

# create post

@login_required(login_url='login')
def Postcreate(request):
    form = Postcreationform()
    posts = Post.objects.filter(profile=request.user.profile).filter(completed=False)

    if request.method == 'POST':
        form = Postcreationform(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.profile = request.user.profile
            dob = request.user.profile.dob
            instance.age = from_dob_to_age(dob)
            print('hello world')
            doc = bool(instance.documents)
            print('This is the content of the document',doc)
            if doc is False: 
                print("The doc field is Empty") 
            else:
                print('Wow document exists')
                instance.category = 1
            instance.save()
            return redirect('post')
    context = {'form': form, 'posts': posts}
    return render(request, 'Postcreate.html', context)

# Display the profile of receiver(of the respective post)

@login_required(login_url='login')
def Viewprofile(request, user_name):

    user = User.objects.get(username=user_name)
    profile = Profile.objects.get(user=user)
    posted = profile.post_set.filter(completed=False)
    # posted = posted
    transactions = profile.receiver_profile.all()

    context = {'profile': profile, 'posted': posted,
               'transactions': transactions}

    return render(request, 'Viewprofile.html', context)

# takes care of payment for the receiver


def Walletupdate_receiver(receiver_profile, instance):
    receiver_profile.wallet = receiver_profile.wallet + \
        int(instance.cash)
    receiver_profile.save(update_fields=['wallet'])


# def authenticate_payment():
@login_required(login_url='login')
# this displays the payment page where we can enter amount and payment password
def Makepayments(request, user_name, post_id):
    form = PaymentForm()
    receiver_username = User.objects.get(username=user_name)
    receiver_profile = Profile.objects.get(user=receiver_username)
    # payment pass hash value finding
    post = Post.objects.get(id=post_id)
    paypass_from_form = request.POST.get('paypass')
    hasher_paypass = hasher(paypass_from_form)
    sender_payment_password = request.user.profile.payment_password
    # entry check
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        
        if sender_payment_password == hasher_paypass:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.sender_profile = request.user.profile
                instance.receiver_profile = receiver_profile
                instance.post = post
                balance_amount_required = int(post.cash_required) - post.cash_received
                print('This is the balance requried',balance_amount_required)
                if balance_amount_required != 0:
                    if int(instance.cash) < instance.sender_profile.wallet :
                        if instance.sender_profile != instance.receiver_profile:

                            if int(post.cash_required) != post.cash_required and int(post.cash_required) > post.cash_received and int(instance.cash) <= balance_amount_required:
                                
                                Walletupdate_receiver(receiver_profile, instance)
                                sender_profile = request.user.profile
                                sender_profile.wallet = sender_profile.wallet - \
                                    int(instance.cash)
                                sender_profile.save(update_fields=['wallet'])
                                post.cash_received = post.cash_received + \
                                    int(instance.cash)
                                post.save(update_fields=['cash_received'])
                                instance.save()

                                messages.success(request, 'Payment Successful!')
                                return redirect("viewprofile", receiver_username)
                            else:
                        
                                messages.error(
                                    request, "Enter valid amount")
                        else:
                            messages.error(request, 'Transaction Prohibited!')
                    else:
                        messages.error(request, 'Not enough money in your wallet.')
                else:
                    messages.error(request,'Receiver stopped accepting payments')
        else:
            messages.error(request, "Password didn't match!")

    context = {'form': form, 'profile': receiver_profile}
    return render(request, 'Makepayments.html', context)

@login_required(login_url='login')
def Deletepost(request, post_id):
    instance = Post.objects.get(id=post_id)
    form = Postcreationform(instance=instance)
    if request.method == 'POST':
        if request.user.profile == instance.profile:
            instance.delete()
            return redirect('createpost')
        else:
            messages.info(request, 'Action Prohibited')
    context = {'instance': instance}
    return render(request, 'Deletepost.html', context)

def Faq(request):

    return render(request,'FAQs.html')

def About(request):

    return render(request,'About.html')

def Contact(request):

    return render(request,'Contact.html')


def Algorithm(request):
    var = algo()
    return render(request,'Algorithm.html')
