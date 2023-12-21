from django.urls import path
from cakeapp.views import SignUpView,SignInView,CategoryCreateView,CakeCreateView,CakeListView,CakeUpdateView,remove_category,remove_cakeView\
,CakeVarientCreateView,CakeDetailView,IndexView,CakeVarientUpdateView,remove_varient,OfferCreateView,remove_offer,sign_out_view,AdminView,OrderView\
,OrderUpdateView,ReviewView



urlpatterns=[
    path("register/",SignUpView.as_view(),name="signup"),
    path("",IndexView.as_view(),name="index"),
    path("signin/",SignInView.as_view(),name="signin"),
    path("dashboard/",AdminView.as_view(),name="adminindex"),
    path("add/",CategoryCreateView.as_view(),name="category-add"),
    path("categories/<int:pk>/remove/",remove_category,name="remove-category"),
    path("cakes/add",CakeCreateView.as_view(),name="cake-add"),
    path("cakes/all",CakeListView.as_view(),name="cake-list"),
    path("cakes/<int:pk>/change",CakeUpdateView.as_view(),name="cake-change"),
    path("cakes/<int:pk>/remove",remove_cakeView,name="cake-remove"),
    path("cakes/<int:pk>/varients/add",CakeVarientCreateView.as_view(),name="add-varient"),
    path("cakes/<int:pk>/",CakeDetailView.as_view(),name="cake-detail"),
    path("varient/<int:pk>/change/",CakeVarientUpdateView.as_view(),name="update-varient"),
    path("varients/<int:pk>/remove",remove_varient,name="remove-varient"),
    path("varients/<int:pk>/offer/add",OfferCreateView.as_view(),name="offer-add"),
    path("varients/<int:pk>/offers/remove",remove_offer,name="remove-offer"),
    path("cake/orders/",OrderView.as_view(),name="order"),
    path("cake/orders/<int:pk>/change",OrderUpdateView.as_view(), name="order-change"),
    path("cake/reviews",ReviewView.as_view(), name="review"),
    path("logout",sign_out_view,name="signout")






]