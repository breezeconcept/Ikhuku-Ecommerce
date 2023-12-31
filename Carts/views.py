from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CartItem
from .serializers import CartItemSerializer
# from django.db import IntegrityError
from rest_framework.views import APIView

        

class CartItemListView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        product_id = request.data.get('product')  # Extract product ID from request data
        quantity = request.data.get('quantity', 1)

        # Check if the same product is already in the user's cart
        existing_item = CartItem.objects.filter(user=user, product_id=product_id).first()
        if existing_item:
            # If the item exists, update its quantity
            existing_item.quantity += int(quantity)
            existing_item.save()
            serializer = self.get_serializer(existing_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # If the item doesn't exist, create a new one
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


        

        


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)
    
        

class CartItemRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        user = request.user
        cart_item = CartItem.objects.filter(user=user, product_id=product_id).first()

        if cart_item:
            cart_item.delete()
            return Response({'message': 'Product removed from cart successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Product not found in cart'}, status=status.HTTP_404_NOT_FOUND)



