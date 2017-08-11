from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

# rest framework imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions

# alternosite imports
from alternosite.models import Product, SubCategory, Category
from alternosite.serializers import ProductListSerializer


def index(request):
    products = Product.objects.filter(approved=True, removed=False).order_by("-id")[:4]
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    context = list()
    for cat in categories:
        dict_ = dict()
        subs = sub_categories.filter(category__name=cat.name)
        list_ = list()
        for sub in subs:
            list_.append(sub.name)
        dict_['name'] = cat.name
        dict_['subs'] = list_
        context.append(dict_)
    return render(request, 'index.html', {'products': products, 'categories': context})


def loginuser(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'registration/login.html')
    else:
        return render(request, 'registration/login.html')


def logoutuser(request):
    logout(request)
    return HttpResponseRedirect("/")


def registeruser(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            context = {
                "error": "This username already exists",
            }
            return render(request, 'registration/login.html', context)
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        return render(request, 'registration/login.html')


def detailProduct(request, **kwargs):
    product_id = kwargs['id']
    product = Product.objects.get(id=product_id)
    product_line = Product.objects.filter(product_line=product.product_line).exclude(id=product.id)
    product_line = product_line.annotate(consumption_times=Count('likes')) \
        .order_by('-consumption_times')
    return render(request, 'productdetail.html', {'main_product': product, 'product_line': product_line})


@login_required()
def account(request, **kwargs):
    user = request.user
    product_likes = Product.objects.filter(likes=user)
    added = Product.objects.filter(user=user)
    context = {'user': user,
               'liked_products': product_likes,
               'added': added}
    return render(request, 'account.html', context)


class ProductLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, product=None, format=None):
        obj = get_object_or_404(Product, id=product)
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated():
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data)


class CommentLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, product=None, format=None):
        obj = get_object_or_404(Product, product=product)
        user = self.request.user
        liked = False
        if user.is_authenticated():
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
        data = {
            "liked": liked
        }
        return Response(data)


class ProductAutocompleteList(APIView):
    """
    List of products that contain the 'term' passed in as a GET.
    """

    def get(self, request, **kwargs):
        q = request.GET.get('term', '')
        products = Product.objects.filter(Q(name__icontains=q))

        serializer = ProductListSerializer(products, many=True)

        return Response(serializer.data)
