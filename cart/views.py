import json
from lib2to3.pgen2 import token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.urls import reverse
# views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CartUpdateSerializer, ProductSerializer,AddToCartSerializer,ApplyCouponSerializer
from rest_framework.permissions import BasePermission
from authentication.backends import JWTAuthentication

class MyCustomPermission(BasePermission):
    def has_permission(self, request, view,):
        # your custom permission logic here
        return True 

class ProductCreateView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [MyCustomPermission]
    def post(self, request):
        serializer = ProductSerializer(data=request.data)    # Deserialize the request data into a ProductSerializer object
        user_id = self.request.user['userId']
        print(user_id,"   USER_ID___________")
        if serializer.is_valid():
            # Open the products JSON file and load its contents into a dictionary
            with open('productlist.json', 'r') as f:
                product_list = json.load(f)

            with open('productId_price.json', 'r') as f:
                product_price_list = json.load(f)
            # Checking if productId already exist or not
            new_product = serializer.validated_data
            for product in product_list['products']:
                if product['productId'] == new_product['productId']:
                    return Response({'productId': 'Product with this ID already exists.'},
                                    status=status.HTTP_400_BAD_REQUEST)

            # Add the new product to the dictionary
            product_list['products'].append(new_product)
            product_price_list.update({new_product['productId']: new_product['unit_price']})
            with open('productId_price.json', 'w') as f:
                json.dump(product_price_list,f,indent=4)

            # Write the updated dictionary back to the JSON file
            with open('productlist.json', 'w') as f:
                json.dump(product_list, f,indent=4)

            # Return a success response
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            # Return an error response with the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddToCartView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[MyCustomPermission]
    def post(self, request):
        # Get the user ID from the request
        user_id = self.request.user['userId']
        print(user_id,"   USER_ID___________")

        serializer = AddToCartSerializer(data=request.data)
        print(request.data,"DATA__________")
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        print(validated_data,"DAAAAAAAAA")
        with open('productlist.json', 'r') as f:
            product_list = json.load(f)

        product_exist=False
        for product in product_list['products']:
            if product['productId']==validated_data['productId']:
                product_exist=True

        if product_exist==False:
            return Response({'error': 'ProductId does not exist.'})
        # Load the usercarts.json file
        with open('userscart.json', 'r') as f:
            user_carts = json.load(f)

        # Find the user's cart, or create a new one if it doesn't exist
        user_cart = None
        for user in user_carts['users']:
            if user['userId'] == user_id:
                user_cart = user['cart']
                break
        if not user_cart:
            user_cart = []
            user_carts['users'].append({'userId': user_id, 'cart': user_cart})

        product = None
        for item in user_cart:
            if item['productId'] == validated_data['productId']:
                product = item
                break
        if not product:
            product = {'productId': validated_data['productId'],'quantity': 0}
            user_cart.append(product)

        # Update the quantity and save the file
        product['quantity'] += validated_data['quantity']

        with open('userscart.json', 'w') as f:
            json.dump(user_carts,f, indent=4)

        return Response({'success': True}, status=status.HTTP_201_CREATED)

class UpdateCartView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[MyCustomPermission]
    def put(self, request):
        user_id = self.request.user['userId']
        # Deserialize the request data into a CartUpdateSerializer object
        serializer = CartUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Open the userscart JSON file and load its contents into a dictionary
        with open('userscart.json', 'r') as f:
            userscart = json.load(f)

        # Find the user's cart and the specified product in the cart
        for user in userscart['users']:
            if user['userId'] == user_id:
                for item in user['cart']:
                    if item['productId'] == int(validated_data['productId']):
                        print("NAMASTE")
                        # Update the quantity of the specified product
                        item['quantity'] = int(validated_data['quantity'])
                        # Write the updated dictionary back to the JSON file
                        with open('userscart.json', 'w') as f:
                            json.dump(userscart, f, indent=4)
                        # Return a success response
                        return Response({'message': 'Cart updated successfully'}, status=status.HTTP_200_OK)

        # If the specified user or product is not found, return an error response
        return Response({'message': 'User or product not found'}, status=status.HTTP_404_NOT_FOUND)
     


class DeleteProductFromCartView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [MyCustomPermission]
    def delete(self, request, product_id):
        # Get the user ID from the request
        user_id = self.request.user['userId']

        # Load the usercarts.json file
        with open('userscart.json', 'r') as f:
            user_carts = json.load(f)

        # Find the user's cart, or return a 404 error if it doesn't exist
        user_cart = None
        for user in user_carts['users']:
            if user['userId'] == user_id:
                user_cart = user['cart']
                break
        if not user_cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        # Find the product in the cart, or return a 404 error if it doesn't exist
        product = None
        for item in user_cart:
            if item['productId'] == product_id:
                product = item
                break
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Remove the product from the cart and save the file
        user_cart.remove(product)
        with open('userscart.json', 'w') as f:
            json.dump(user_carts, f,indent=4)

        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)


class CartInfoView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[MyCustomPermission]
    def get(self,request,user_id):
        if self.request.user['userId']!=user_id:
            return Response({'error': 'token not valid'})
        with open('userscart.json') as file:
            data = json.load(file)

        total_price = 0
        total_quantity = 0
        cart_items = []
        print(self.request.user['userId'])
        with open('productId_price.json', 'r') as f:
            product_price_list = json.load(f)
            print(product_price_list,"ZXZCXZCXZCX")
        for user in data['users']:
            if user['userId'] == self.request.user['userId']:
                for item in user['cart']:
                    # Assuming there is a Product model with a price field
                    cart_items.append({
                        'product_id':item['productId'],
                        'product_quantity':item['quantity'],
                        'unit_price':product_price_list[str(item['productId'])]
                    })
                    
                    total_price =total_price + product_price_list[str(item['productId'])] * item['quantity']
                    
                    total_quantity =total_quantity+ item['quantity']
                break
        response_data = {
            'cart_items': cart_items,
            'total_price': total_price,
            'total_quantity': total_quantity
        }
        return Response(response_data)

class ApplyCouponView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[MyCustomPermission]
    def post(self, request):
        serializer = ApplyCouponSerializer(data=request.data)
        print(request.data,"DATA__________")
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user_id = self.request.user['userId']
        url = reverse('check-out',args=[user_id])
        url="http://127.0.0.1:8000"+url
        print(self.request.auth,"DFDFFD")
        headers = {'Authorization': f'Bearer {self.request.auth}'}
        print(headers," HEADRER_________")
        response = requests.get(url,headers=headers)

 
        if response.status_code == 200:
            # If the request was successful, get the total price from the response
            total_price = response.json().get('total_price')
            with open('coupons.json') as f:
                coupon_data = f.read()

            coupons = json.loads(coupon_data)['coupons']
            for coupon in coupons:
                if coupon['name']==validated_data['coupon_code']:
                    if total_price>=coupon['min_order_value']:
                        total_price=total_price-total_price*(coupon['discount_percent']/100)
                        response_data = {
                        'discounted_price': total_price,
                        'total_quantity': response.json().get('total_quantity')}
                        return Response(response_data)

            return Response({'error': 'Cupon code not applicable'})
        else:
            # If the request failed, return an error response
            return Response({'error': 'Failed to get cart info'})




