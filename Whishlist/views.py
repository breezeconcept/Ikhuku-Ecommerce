from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Favorite
from .serializers import FavoriteSerializer
from rest_framework.pagination import PageNumberPagination
from Products.models import Product



class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user=self.request.user
        return Favorite.objects.filter(user=user)


class FavoriteCreateView(generics.CreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        product_id = request.data.get('product')  # Get product ID from request data

        # Check if the product is already in the favorites for the user
        if Favorite.objects.filter(user=user, product_id=product_id).exists():
            message = 'Product is already in the favorites'
            response_data = {
                "message": message,
                "status": status.HTTP_400_BAD_REQUEST,
                "data": {
                    "error_details": "You cannot add a single product twice to favorites."
                }
            }
            return Response(response_data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, is_favourite=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



# class FavoriteCreateView(generics.CreateAPIView):
#     serializer_class = FavoriteSerializer
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         user = self.request.user
#         product_id = request.data.get('product')  # Get product ID from request data

#         # Check if the product is already in the favorites for the user
#         if Favorite.objects.filter(user=user, product_id=product_id).exists():
#             message = 'Product is already in the favorites'
#             response_data = {
#                 "message": message,
#                 "status": status.HTTP_400_BAD_REQUEST,
#                 "data": {
#                     "error_details": "You cannot add a single product twice to favorites."
#                 }
#             }
#             return Response(response_data)

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(user=user, is_favourite=True)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class FavoriteDeleteView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id' 
