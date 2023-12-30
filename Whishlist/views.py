from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Favorite
from .serializers import FavoriteSerializer
from rest_framework.pagination import PageNumberPagination



class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)



class FavoriteCreateView(generics.CreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user


        # Check if a seller profile already exists for the user
        if Favorite.objects.filter(user=user).exists():
            message = 'Product is already on the whislist'
            response_data = {
                "message": message,
                "status": status.HTTP_400_BAD_REQUEST,
                "data": {
                    "error_details": "You cannot add a single product twice to whishlist."
                }
            }
            return Response(response_data)
        
        # try:
        #     serializer.save(user=user)
        # except IntegrityError:
        #     return Response({'message': 'Favorite already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



        


class FavoriteDeleteView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id' 
