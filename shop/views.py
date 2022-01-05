from django.shortcuts import render, get_object_or_404
# Internal Imports
from .models import Category, Product, Profile, Comment
# Import from cart
from cart.forms import CartAddProductForm

# Import from the base forms
from .forms import CommentForm

# Import for the login form
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm

# Login required import
from django.contrib.auth.decorators import login_required

# Import to help with pagination
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def product_list(request, category_slug=None):
    # pagination
    object_list = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        object_list = Product.objects.filter(category=category)

    paginator = Paginator(object_list, 8)  # 8 products per page
    page = request.GET.get('page')

    category = None
    categories = Category.objects.all()
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()  # Cart form

    # List of active comments for this post
    comments = product.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.product = product
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'shop/product/detail.html',
                  {'product': product,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'cart_product_form': cart_product_form})


def contact(request):
    return render(request, 'shop/product/contact.html')


def about(request):
    return render(request, 'shop/product/about.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'shop/account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()

            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request, 'shop/account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'shop/account/register.html',
                  {'user_form': user_form})


def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'shop/account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
