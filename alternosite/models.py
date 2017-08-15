# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    name = models.CharField(max_length=50)
    sub_category = models.ForeignKey(SubCategory, related_name='productlines', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    name = models.CharField(max_length=70)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    product_line = models.ForeignKey(ProductLine, related_name='products', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    web_link = models.CharField(max_length=200, blank=True, null=True)
    create_date = models.DateField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    height_field = models.IntegerField(default=20)
    width_field = models.IntegerField(default=20)
    image = models.ImageField(upload_to='images/',
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    removed = models.BooleanField(default=False)

    def get_api_like_url(self):
        return reverse("like-api-toggle", kwargs={"product": self.id})

    def remove(self):
        self.removed = True
        self.save()


class Comment(models.Model):

    product = models.ForeignKey(Product, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='comment_likes')
    removed = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def remove(self):
        self.removed = True
        self.save()
