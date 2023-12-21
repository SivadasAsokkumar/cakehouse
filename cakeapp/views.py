from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator

from django.views.generic import CreateView,FormView,ListView,UpdateView,DetailView,TemplateView,View
from cakeapp.forms import RegistrationForm,LoginForm,CategoryCreateForm,CakeAddForm,CakeVarientForm,OfferAddForm,OrderChangeForm
from cakeapp.models import User,Category,Cakes,CakeVarients,Offers,Orders,Reviews
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session!!!")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper



def is_admin(fn):
    def wrapper(request,*args,**Kwargs):
        if not request.user.is_superuser:
            messages.error(request,"permission denied for current user !!!")
            return redirect("signin")
        else:
           return fn(request,*args,**Kwargs)
    return wrapper

decs=[signin_required,is_admin]

class SignUpView(CreateView):

    template_name="cake/register.html"
    form_class=RegistrationForm
    model=User
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
         messages.success(self.request,"Account created")
         return super().form_valid(form)
    def form_invalid(self,form):
         messages.error(self.request,"failed to create")
         return super().form_invalid(form)
    
    
class SignInView(FormView):
    template_name="cake/login.html"
    form_class=LoginForm
     
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)

        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login successfully")
                return redirect("adminindex")
            else:
                messages.error(request,"invalid creadential")
                return render(request,self.template_name,{"form":form})  
            

class IndexView(TemplateView):
    template_name="cake/home.html"

class AdminView(TemplateView):
    template_name="cake/adminindex.html"

@method_decorator(decs,name="dispatch")
class CategoryCreateView(CreateView,ListView):
    template_name="cake/category_add.html"
    form_class=CategoryCreateForm
    model=Category
    context_object_name="categories"
    success_url=reverse_lazy("adminindex")

    def form_valid(self, form):
        messages.success(self.request,"category added successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"category adding failed")
        return super().form_invalid(form)
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True)
    
@signin_required
@is_admin
def remove_category(request,*args,**kwargs):
    id=kwargs.get("pk")
    Category.objects.filter(id=id).update(is_active=False)
    messages.success(request,"category removed")
    return redirect("category-add")

@method_decorator(decs,name="dispatch")
class CakeCreateView(CreateView):
    template_name="cake/cake_add.html"
    model=Cakes
    form_class=CakeAddForm
    success_url=reverse_lazy("adminindex")
    def form_valid(self, form):
        messages.success(self.request,"cake has been added")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"cake adding failed")
        return super().form_invalid(form)
    

@method_decorator(decs,name="dispatch")
class CakeListView(ListView):
    template_name="cake/cake_list.html"
    model=Cakes
    context_object_name="cake"

@method_decorator(decs,name="dispatch")
class CakeUpdateView(UpdateView):
    template_name="cake/cake_edit.html"
    model=Cakes
    form_class=CakeAddForm
    success_url=reverse_lazy("adminindex")
    def form_valid(self, form):
        messages.success(self.request,"cake added successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"cake updating failed")
        return super().form_invalid(form)
    

@signin_required
@is_admin
def remove_cakeView(request,*args,**kwrags):
    id=kwrags.get("pk")
    Cakes.objects.filter(id=id).delete()
    return redirect("cake-list")

@method_decorator(decs,name="dispatch")
class CakeVarientCreateView(CreateView):
    template_name="cake/cakevarient_add.html"
    form_class=CakeVarientForm
    model=CakeVarients
    success_url=reverse_lazy("adminindex")
    def form_valid(self, form):
        id=self.kwargs.get("pk")
        obj=Cakes.objects.get(id=id)
        form.instance.cake=obj
        messages.success(self.request,"cake varient has been added")
        return super().form_valid(form)
    
@method_decorator(decs,name="dispatch")
class CakeDetailView(DetailView):
    template_name="cake/cake_detail.html"
    model=Cakes
    context_object_name="cake"
    

@method_decorator(decs,name="dispatch")
class CakeVarientUpdateView(UpdateView):
    template_name="cake/varient_edit.html"
    form_class=CakeVarientForm
    model=CakeVarients
    success_url=reverse_lazy("cake-list")
    def form_valid(self, form):
        messages.success(self.request,"cake varient updated successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"cake varent updating failed")
        return super().form_invalid(form)
    
@signin_required
@is_admin
def remove_varient(request,*args,**kwargs):
    id=kwargs.get("pk")
    CakeVarients.objects.filter(id=id).delete()
    return redirect("cake-list")

@method_decorator(decs,name="dispatch")
class OfferCreateView(CreateView):
    template_name="cake/offer_add.html"
    model=Offers
    form_class=OfferAddForm
    success_url=reverse_lazy("cake-list")
    def form_valid(self, form):
        id=self.kwargs.get("pk")
        obj=CakeVarients.objects.get(id=id)
        form.instance.cakevarient=obj
        messages.success(self.request,"added successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request," not added")
        return super().form_invalid(form)
    
    def get_success_url(self):
        id=self.kwargs.get("pk")
        cak_varient_object=CakeVarients.objects.get(id=id)
        cake_id=cak_varient_object.cake.id
        return reverse("cake-detail",kwargs={"pk":cake_id})
    
@signin_required
@is_admin
def remove_offer(request,*args,**kwargs):
    id=kwargs.get("pk")
    offer_object=Offers.objects.get(id=id)
    cake_id=offer_object.cakevarient.cake.id
    offer_object.delete()
    return redirect("cake-detail",pk=cake_id)

@method_decorator(decs,name="dispatch")
class OrderView(ListView):
    template_name="cake/order.html"
    model=Orders
    context_object_name="orders"
    def get_queryset(self):
        return Orders.objects.filter(status="order-placed")
    


class OrderUpdateView(UpdateView):
    template_name="cake/order_edit.html"
    model=Orders
    form_class=OrderChangeForm
    success_url=reverse_lazy("adminindex")
    def form_valid(self,form):
        messages.success(self.request,"order updated successfully")
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.error(self.request,"order updating failed")
        return super().form_invalid(form)
    

@method_decorator(decs,name="dispatch")
class ReviewView(ListView):
    template_name="cake/review.html"
    model=Reviews
    context_object_name="review"



    


    

    



        

@signin_required
@is_admin
def sign_out_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")  

     
    
    