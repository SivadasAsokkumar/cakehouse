from rest_framework import serializers
from cakeapp.models import User,Cakes,CakeVarients,Carts,Orders,Reviews


class Userserializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)


    class Meta:
        model=User
        fields=["id","username","password","email","phone","address"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class CakeVarientSerializer(serializers.ModelSerializer):

    class Meta:
        model=CakeVarients
        fields="__all__"


class ReviewSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    cake=serializers.CharField(read_only=True)

    class Meta:
        model=Reviews
        fields="__all__"


class  CakeSerializer(serializers.ModelSerializer):
    Category=serializers.StringRelatedField(read_only=True)
    varients=CakeVarientSerializer(many=True,read_only=True)
    reviews=ReviewSerializer(many=True,read_only=True)
    
    
    class Meta:
        model=Cakes
        fields="__all__"


class CartSerializer(serializers.ModelSerializer):
    # id=serializers.CharField(read_only=True)
    cakevarient=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)


    class Meta:
        model=Carts
        fields="__all__"


class orderSerializer(serializers.ModelSerializer):
    cakevarient=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    orderd_date=serializers.CharField(read_only=True)
    expected_date=serializers.CharField(read_only=True)


    class Meta:
        model=Orders
        fields="__all__"







    


