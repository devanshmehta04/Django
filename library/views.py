from django.shortcuts import render
from .models import Book, Author
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm, AuthorForm

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

@login_required
def author_list(request):
    authors = Author.objects.all()
    return render(request, 'library/author_list.html', {'authors': authors})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book_list')
    else:
        form = AuthenticationForm()
    return render(request, 'library/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'library/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('book_list')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'library/author_list.html', {'authors': authors})


def set_session(request):
    request.session['username'] = 'john_doe'  # Store the username in the session
    return HttpResponse("Session is set!")

def get_session(request):
    username = request.session.get('username', 'Guest')  # Retrieve the username from session
    return HttpResponse(f"Hello, {username}!")

def clear_session(request):
    try:
        del request.session['username']  # Delete a specific session variable
    except KeyError:
        pass
    return HttpResponse("Session data cleared.")

def set_cookie(request):
    response = HttpResponse("Cookie is set!")
    # Set a cookie for 30 days (expires after 30 days)
    response.set_cookie('username', 'john_doe', max_age=60*60*24*30)
    return response

def get_cookie(request):
    username = request.COOKIES.get('username', 'Guest')  # Get the cookie value or default to 'Guest'
    return HttpResponse(f"Hello, {username}!")

def delete_cookie(request):
    response = HttpResponse("Cookie is deleted!")
    response.delete_cookie('username')  # Deletes the 'username' cookie
    return response

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username  # Set the session variable
            response = HttpResponse("You are logged in!")
            response.set_cookie('username', username, max_age=60*60*24*30)  # Set the cookie
            return response
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'login.html')

def user_profile(request):
    username = request.session.get('username', 'Guest')  # Get from session
    # Optionally, get from cookie if session is not available
    if 'username' not in request.session:
        username = request.COOKIES.get('username', 'Guest')

    return HttpResponse(f"Welcome, {username}!")

def user_logout(request):
    # Clear the session
    request.session.flush()  # Clears all session data
    response = HttpResponse("You are logged out!")
    # Delete the cookie
    response.delete_cookie('username')
    return response

#####################################################################################################

# Home page displaying books and authors
def book_list(request):
    books = Book.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        if 'add_book' in request.POST:
            book_form = BookForm(request.POST)
            if book_form.is_valid():
                book_form.save()
        elif 'add_author' in request.POST:
            author_form = AuthorForm(request.POST)
            if author_form.is_valid():
                author_form.save()

    book_form = BookForm()
    author_form = AuthorForm()

    return render(request, 'library/home.html', {
        'books': books,
        'authors': authors,
        'book_form': book_form,
        'author_form': author_form,
    })

# View to edit a book
def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form})

# View to delete a book
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('home')


