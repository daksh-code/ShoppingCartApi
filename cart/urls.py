from django.urls import path
from cart.views import  ProductCreateView,AddToCartView,DeleteProductFromCartView,ApplyCouponView,CartInfoView,UpdateCartView



urlpatterns = [
     path('add_new_product/', ProductCreateView.as_view()),
     path('add_product_to_cart/', AddToCartView.as_view()),
     path('update_cart_product/', UpdateCartView.as_view()),
     path('delete_product_from_cart/<int:product_id>', DeleteProductFromCartView.as_view()),
     path('checkout/<int:user_id>', CartInfoView.as_view(),name='check-out'),
     path('apply_cupon_code/', ApplyCouponView.as_view()),
]

