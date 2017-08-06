from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

# rest framework imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions


from alternosite.models import Product
from alternosite.serializers import RecentUploadSerializer


def index(request):
    products = Product.objects.filter(approved=True, removed=False).order_by("-id")[:4]
    return render(request, 'index.html', {'products': products})


def loginuser(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
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
            return render(request, 'register.html',  context)
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        return render(request, 'register.html')


def detailProduct(request, **kwargs):
    product_id = kwargs['id']
    product = Product.objects.get(id=product_id)
    return render(request, 'productdetail.html', {'product': product})


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
