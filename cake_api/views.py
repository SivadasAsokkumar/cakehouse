from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.decorators import action

from cake_api.serializers import Userserializer,CakeSerializer,CartSerializer,orderSerializer,ReviewSerializer

from cakeapp.models import User,Cakes,CakeVarients,Carts,Orders,Reviews


class Userview(APIView):
    def post(self,request,*args, **kwargs):
     serializer=Userserializer(data=request.data)
     if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data)
     else:
        return Response(data=serializer.errors)
     

class CakeView(ModelViewSet):
   #authentication_classes=[authentication.BasicAuthentication]
   authentication_classes=[authentication.TokenAuthentication]
   permission_classes=[permissions.IsAuthenticated]
   serializer_class=CakeSerializer
   queryset=Cakes.objects.all()

   @action(methods=["post"],detail=True)
   def carts_add(self,request,*args, **kwargs):
      vid=kwargs.get("pk")
      varient_obj=CakeVarients.objects.get(id=vid)
      serializer=CartSerializer(data=request.data)
      user=request.user
      if serializer.is_valid():
         serializer.save(user=user,cakevarient=varient_obj)
         return Response(data=serializer.data)
      else:
         return Response(data=serializer.errors)
      

   @action(methods=["post"],detail=True)
   def place_order(self,request,*args,**kwargs):
      id=kwargs.get("pk")
      varient_obj=CakeVarients.objects.get(id=id)
      user=request.user
      serializer=orderSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save(cakevarient=varient_obj,user=user)
         return Response(data=serializer.data)
      else:
         return Response(data=serializer.errors)
      
   @action(methods=["post"],detail=True)
   def add_review(self,request,*args, **kwargs):
        c_id=kwargs.get("pk")
        cake_obj=Cakes.objects.get(id=c_id)
        user=request.user
        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cake=cake_obj,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


   
      

class CartsView(ViewSet):
   #authentication_classes=[authentication.BasicAuthentication]
   authentication_classes=[authentication.TokenAuthentication]
   permission_classes=[permissions.IsAuthenticated]
   def list(self,request,*args, **kwargs):
      user=request.user
      qs=Carts.objects.filter(user=user)
      serializer=CartSerializer(qs,many=True)
      return Response(data=serializer.data)
   


   def destroy(self,request,*args, **kwargs):
      id=kwargs.get("pk")
      qs=Carts.objects.filter(id=id).delete()
      return Response(data={"message":"deleted"})
   

class OrderView(ViewSet):
    #authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=orderSerializer
    
    def list(self,request,*args,**kwargs):
        qs=Orders.objects.filter(user=request.user)
        serializer=orderSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        instance=Orders.objects.get(id=id)
        if instance.user==request.user:
            instance.delete()
            return Response(data={"message":"order removed successfully"})
        else:
            return Response(data={"message":"permission denied for current user"})
        

class ReviewView(ViewSet):
    #authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ReviewSerializer
    
    def list(self,request,*args,**kwargs):
        qs=Reviews.objects.filter(user=request.user)
        serializer=ReviewSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        instance=Reviews.objects.get(id=id)
        if instance.user==request.user:
            instance.delete()
            return Response(data={"message":"review removed successfully"})
        else:
            return Response(data={"message":"permission denied for current user"})