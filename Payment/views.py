from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order  # Import your Order model
from Carts.models import CartItem  # Import your CartItem model
from .serializers import OrderSerializer
import requests
from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer



class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Assign the logged-in user to the order



class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]



class CheckoutInitiationView(APIView):
    def post(self, request):
        try:
            # Fetch user's cart items
            cart_items = CartItem.objects.filter(user=request.user)
            
            # Calculate total amount based on cart items
            total_amount = calculate_total_amount(cart_items)
            
            # Create an order for the user
            order = Order.objects.create(user=request.user, total_amount=total_amount)

            # Serialize order details
            serializer = OrderSerializer(order) 

            # Return serialized order details for the checkout process
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle exceptions or errors during order creation or calculation
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

def calculate_total_amount(cart_items):
    # Calculate the total amount based on cart items
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    return total_amount




class PaymentProcessingView(APIView):
    def post(self, request):
        # Collect payment details from the request data
        tx_ref = request.data.get('tx_ref')
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'NGN')
        redirect_url = request.data.get('redirect_url')
        customer_email = request.data.get('customer_email')
        # Other required and optional fields...

        if not (tx_ref and amount and redirect_url and customer_email):
            return Response({'error': 'Incomplete payment details'}, status=status.HTTP_400_BAD_REQUEST)

        # Make a POST request to Flutterwave's API to initiate payment
        your_flutterwave_secret_key = settings.FLW_SEC_KEY
        headers = {
            'Authorization': f'Bearer {your_flutterwave_secret_key}'
        }
        payload = {
            'tx_ref': tx_ref,
            'amount': amount,
            'currency': currency,
            'redirect_url': redirect_url,
            # Include other payment details as per the Flutterwave documentation
        }

        try:
            # Initiate payment
            response = requests.post('https://api.flutterwave.com/v3/payments', json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json().get('data', {})
                payment_link = data.get('link')
                return Response({'payment_link': payment_link}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Payment initiation failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        status = request.query_params.get('status')
        tx_ref = request.query_params.get('tx_ref')
        transaction_id = request.query_params.get('transaction_id')
        # Other parameters...

        if status == 'successful':
            # Verify the transaction status with Flutterwave
            verify_url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
            your_flutterwave_secret_key = settings.FLW_SEC_KEY
            headers = {
                'Authorization': f'Bearer {your_flutterwave_secret_key}'
            }

            try:
                # Verify transaction status
                response = requests.get(verify_url, headers=headers)
                if response.status_code == 200:
                    transaction_data = response.json().get('data')
                    if transaction_data.get('status') == 'successful':
                        # Process the successful payment: Update your database, send confirmation emails, etc.
                        order = Order.objects.get(tx_ref=tx_ref)
                        order.status = 'paid'
                        order.save()
                        
                        # Send a confirmation email to the customer
                        # Your email sending logic here...
                        
                        return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': 'Transaction verification failed'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': 'Transaction verification failed'}, status=status.HTTP_400_BAD_REQUEST)
            except Order.DoesNotExist:
                return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Handle cases where the transaction status isn't successful
            return Response({'message': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)
