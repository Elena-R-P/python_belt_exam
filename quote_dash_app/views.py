from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Quote

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'first_name':
                messages.error(request, value, extra_tags='first_name')
            if key == 'last_name':
                messages.error(request, value, extra_tags='last_name')
            if key == 'reg_email':
                messages.error(request, value, extra_tags='reg_email')
            if key == 'reg_password':
                messages.error(request, value, extra_tags='reg_password')
            if key == 'confirm_pw':
                messages.error(request, value, extra_tags='confirm_pw')
        return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(request.POST['reg_password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['reg_email'],
            password = hashed_password
        )
        request.session['user_id'] = user.id
        return redirect('/quotes')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'log_email':
                messages.error(request, value, extra_tags='log_email')
            if key == 'log_password':
                messages.error(request, value, extra_tags='log_password')
        return redirect('/')
    else:
        user_list = User.objects.filter(email=request.POST['log_email'])
        if len(user_list) == 0:
            messages.error(request, "We could not find a user with that email address", extra_tags='log_email')
            return redirect('/')
        else:
            user = user_list[0]
            if bcrypt.checkpw(request.POST['log_password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/quotes')
            else:
                messages.error(request, "Your password does not match", extra_tags='log_password')
                return redirect('/')

def quotes(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'quotes': Quote.objects.all()
        }
        return render(request, 'quotes.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def quote_add(request):
    if request.method == 'GET':
        context = {
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'quotes.html', context)
    if request.method == 'POST':
        errors = Quote.objects.quote_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                if key == 'author':
                    messages.error(request, value, extra_tags='author')
                if key == 'quote_desc':
                    messages.error(request, value, extra_tags='quote_desc')
            return redirect('/quotes')
        else:
            user = User.objects.get(id=request.session['user_id'])
            quote = Quote.objects.create(
                author = request.POST['author'],
                quote_desc = request.POST['quote_desc'],
                posted_by = user
            )
            return redirect('/quotes')

def user_quotes(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user
    }
    return render(request, 'user_quotes.html', context)

def edit_account(request, user_id):
    context = {
            'user': User.objects.get(id=user_id)
        }
    return render(request, 'edit_account.html', context)

def update_account(request, user_id):
    errors = User.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'first_name':
                messages.error(request, value, extra_tags='first_name')
            if key == 'last_name':
                messages.error(request, value, extra_tags='last_name')
            if key == 'reg_email':
                messages.error(request, value, extra_tags='reg_email')
        return redirect(f'/myaccount/{user_id}')
    else:
        user = User.objects.get(id=user_id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['reg_email']
        user.save()
        request.session['user_id'] = user.id
        return redirect('/quotes')

def delete(request, quote_id):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    quote = Quote.objects.get(id=quote_id)
    quote.delete()
    return redirect('/quotes', context)