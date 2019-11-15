from django.shortcuts import render, redirect
import bcrypt
from .models import Users, authors, books, rating
from django.contrib import messages

def check(request):
    errors = Users.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['pw']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print(pw_hash)
        newuser=Users.objects.create(fname=request.POST['fname'], lname=request.POST['lname'], email=request.POST['email'], pw=pw_hash.decode()) 
        request.session['logemail'] = request.POST['email']
        messages.success(request, "Successfully registered")
        return redirect('/success')

def index(request):
    if 'logemail' not in request.session:
        request.session['logemail'] = None
    return render(request, 'app_one/index.html')

def login(request):
    logemail = request.POST['logemail']
    user = Users.objects.get(email=logemail)
    if user:
        if bcrypt.checkpw(request.POST['logpw'].encode(), user.pw.encode()):
            request.session['logemail'] = logemail
            return redirect('/success')
        else:
            messages.error(request, "Incorrect password, try again!")
            return redirect('/')
    else:
        messages.error(request, "User doesn't exist, try again!")
        return redirect('/')
    
def success(request):
    email = request.session['logemail']
    user = Users.objects.get(email = email)
    return render (request, 'app_one/success.html', {'fname' : user.fname, 'userid':user.id})

def logout(request):
    request.session.clear()
    return redirect('/')
    
def books1(request):
    logemail = request.session['logemail']
    user = Users.objects.get(email = logemail)
    context = {
        'user' : user,
        'booklist' : books.objects.all(),
        'allcomments' : rating.objects.all()
    }
    return render(request, 'app_one/books.html', context)

def add(request):
    context = {
        'auslist' : authors.objects.all(), 
    }
    return render(request, 'app_one/add.html', context)

def addprocess(request):
    email = request.session['logemail']
    user = Users.objects.get(email = email)
    bt = request.POST['btitle']
    br = request.POST['stars']
    bu = user
    breview = request.POST['reviewbox']
    if request.POST['authorlist'] != ' ':
        baa = request.POST['authorlist']
        ba = authors.objects.get(name = baa)
        newbook = books.objects.create(title = bt, user = bu, author = ba)
    # elif 
    else:
        na = request.POST['newauthor']
        newauthor = authors.objects.create(name = na)
        newbook = books.objects.create(title = bt, user = bu, author = newauthor)
    newrating = rating.objects.create(rating = br, review = breview, books = newbook, user = user)
    # newrating = books.rating.set(br)

    return redirect(f'/books/{newbook.id}')

def showbook(request, num):
    sb = books.objects.get(id=num)
    context = {
        'sb' : sb,
        'allreviews' : rating.objects.all(),
    }
    return render(request, 'app_one/showbook.html', context)

def userpage(request):
    email = request.session['logemail']
    user = Users.objects.get(email = email)
    context = {
        'user' : user,
    }
    return render (request, 'app_one/userpage.html')

def addareview(request, num):
    upreview = request.POST['updatereview']
    newstar = request.POST['stars']
    selbook = books.objects.get(id=num)
    email = request.session['logemail']
    user = Users.objects.get(email = email)
    # newrating = rating.objects.get(books=selbook)
    # newrating.review = upreview
    # newrating.rating = newstar
    newrating = rating.objects.create(rating = newstar, review = upreview, books = selbook, user=user)
    return redirect(f'/books/{selbook.id}')