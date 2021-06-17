from django.http import Http404
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .serializers import ItemSerializer, ProductSerializer, CategorySearializer, OrderSerializer
from .models import Category, OrderItem, Products, Order
import json
import random


class LatestProductList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        products = Products.objects.all()[0:6]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class RandomProduct(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication,
                              TokenAuthentication, SessionAuthentication]

    def get(self, request, fromat=None):
        products = Products.objects.all()
        random_produuct = random.choice(products)
        serializer = ProductSerializer(random_produuct)
        return Response(serializer.data, status=200)


class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, product_id):
        try:
            return Products.objects.filter(id=product_id).first()
        except Products.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        product = self.get_object(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySearializer(categories, many=True)
        return Response(serializer.data)


class OrdersListView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.all(user=request.user, completed=True)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderItemView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [
        TokenAuthentication,
        BasicAuthentication,
        SessionAuthentication
    ]

    def get(self, request, format=None):
        order, created = Order.objects.get_or_create(
            user=request.user, completed=not True)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class AddItemToCartView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [
        BasicAuthentication,
        TokenAuthentication,
        SessionAuthentication
    ]

    def get_product_object(self, product_id):
        try:
            product = Products.objects.get(id=int(product_id))
            return product.id
        except Products.DoesNotExist:
            return Http404

    def post(self, request, format=None):
        product_id = request.data['product_id']
        quantity = request.data['quantity']

        order, created = Order.objects.get_or_create(
            user=request.user, completed=False)
        product = self.get_product_object(product_id)
        try:
            order_item = OrderItem.objects.get(
                order=order,  product=product_id)
            if order_item:
                serializer = ItemSerializer(order_item, data={
                    'quantity': int(order_item.quantity) + int(quantity),
                })
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=404)
                return Response('Added', status=200)

        except:
            serializer = ItemSerializer(data={
                'order': order.id,
                'product': product,
                'quantity': quantity
            })
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=404)
            return Response('Added', status=200)


class RemoveFromCartView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,
                              SessionAuthentication, BasicAuthentication]

    def post(self, request, fromat=None):

        order, created = Order.objects.get_or_create(user=request.user)
        product = Products.objects.get(id=request.data['product_id'])
        try:
            order_item = OrderItem.objects.filter(
                product=product, order=order).first()
        except:
            return Http404
        print(order_item)

        if order_item.quantity <= 1:
            order_item.delete()
            return Response("Updated", status=200)

        serializer = ItemSerializer(order_item, data={
            "quantity": order_item.quantity - 1
        })
        if serializer.is_valid():
            serializer.save()
            return Response("Updated", status=200)
        else:
            return Response(serializer.errors, status=400)


class CompleteOrder(APIView):

    def post(self, request, format=None):
        try:
            order = Order.objects.get(customer=request.user)
            try:
                order.completed = True
                order.save()

            except:
                return Response({'message': 'Error occoured'}, status=200)
        except Order.DoesNotExist:
            return Response({'Error': 'Order Doesnt Exist'}, status=400)
