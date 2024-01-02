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
import uuid
from django.core.mail import send_mail
from django.utils import timezone

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from django.http import Http404


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




# Inside your CheckoutInitiationView
class CheckoutInitiationView(APIView):
    def post(self, request):
        try:
            existing_order = Order.objects.filter(
                user=request.user, is_completed=False, status='pending'
            ).first()

            if existing_order:
                # Update the existing order with current cart items
                cart_items = CartItem.objects.filter(user=request.user)

                # Calculate total amount based on updated cart items
                total_amount = calculate_total_amount(cart_items)

                # Update existing order details
                existing_order.total_amount = total_amount
                existing_order.save()

                # Serialize existing order details
                serializer = OrderSerializer(existing_order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Create a new order
                cart_items = CartItem.objects.filter(user=request.user)
                total_amount = calculate_total_amount(cart_items)
                new_order = Order.objects.create(
                    user=request.user, total_amount=total_amount
                )

                # Serialize new order details
                serializer = OrderSerializer(new_order)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle exceptions during order creation/update
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def calculate_total_amount(cart_items):
    # Calculate the total amount based on cart items
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    return total_amount





# View to update the latest pending order with user details (address information)
class OrderUpdateView(APIView):
    def post(self, request):
        try:
            # Fetch the latest pending order for the authenticated user
            order = Order.objects.filter(
                user=request.user, is_completed=False, status='pending'
            ).order_by('-created_at').first()

            if order:
                # Extract address details from request data
                street_address = request.data.get('street_address')
                city = request.data.get('city')
                state = request.data.get('state')
                postal_code = request.data.get('postal_code')

                # Update order with user details
                order.street_address = street_address
                order.city = city
                order.state = state
                order.postal_code = postal_code
                order.save()

                # Serialize updated order details
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No pending order found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle exceptions during order update
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class PaystackInitiationView(APIView):
    def post(self, request):
        try:
            user = self.request.user
            order = Order.objects.filter(user=user, is_completed=False, status='pending').first()

            if order:
                amount = order.total_amount
                amount = float(amount)  # Convert Decimal to float
                email = user.email
            else:
                # Create a new order with pending status if one does not exist
                cart_items = CartItem.objects.filter(user=user)
                amount = calculate_total_amount(cart_items)
                order = Order.objects.create(user=user, total_amount=amount, status='pending')

            reference = str(uuid.uuid4())  # Generate a unique reference for the transaction

            # Save the reference to the order
            order.reference = reference
            order.save()

            paystack_data = {
                'email': email,
                'amount': amount * 100,  # Convert amount to the lowest currency unit (kobo in this case)
                'currency': 'NGN',  # Replace with your desired currency code
                'ref': reference,  # Use the generated reference
                # Add more parameters as needed based on your requirements
            }

            paystack_url = 'https://api.paystack.co/transaction/initialize'
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',  # Replace with your Paystack secret key
                'Content-Type': 'application/json',
            }

            # Make a POST request to initialize the transaction
            response = requests.post(paystack_url, json=paystack_data, headers=headers)
            paystack_response = response.json()

            # Check if the Paystack initialization was successful
            if response.status_code == 200 and paystack_response.get('status'):
                # Retrieve the Paystack reference from the response
                paystack_response_reference = paystack_response.get('data', {}).get('reference')

                # Update the order with Paystack's reference
                order.paystack_reference = paystack_response_reference
                order.save()

                # Return the Paystack response to the client
                return Response(paystack_response, status=status.HTTP_200_OK)
            else:
                # Handle Paystack initialization failure
                return Response({'error': 'Paystack initialization failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Order.DoesNotExist:
            return Response({'error': 'Pending order not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle exceptions or errors during the payment initiation process
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







# class PaystackInitiationView(APIView):
#     def post(self, request):
#         try:
#             user = self.request.user
#             order = Order.objects.filter(user=user, is_completed=False, status='pending').first()

#             if order:
#                 amount = order.total_amount
#                 amount = float(amount)  # Convert Decimal to float
#                 email = user.email
#             else:
#                 # Create a new order with pending status if one does not exist
#                 cart_items = CartItem.objects.filter(user=user)
#                 amount = calculate_total_amount(cart_items)
#                 order = Order.objects.create(user=user, total_amount=amount, status='pending')

#             reference = str(uuid.uuid4())  # Generate a unique reference for the transaction

#             # Save the reference to the order
#             order.reference = reference
#             order.save()

#             # paystack_response_reference = '7PVGX8MEk85tgeEpVDtD'  # Replace this with the actual Paystack reference received in the response
#             # order.paystack_reference = paystack_response_reference  # Save Paystack's reference
#             # order.save()

#             paystack_data = {
#                 'email': email,
#                 'amount': amount * 100,  # Convert amount to the lowest currency unit (kobo in this case)
#                 'currency': 'NGN',  # Replace with your desired currency code
#                 'ref': reference,  # Use the generated reference
#                 # Add more parameters as needed based on your requirements
#             }

#             paystack_url = 'https://api.paystack.co/transaction/initialize'
#             headers = {
#                 'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',  # Replace with your Paystack secret key
#                 'Content-Type': 'application/json',
#             }

#             # Make a POST request to initialize the transaction
#             response = requests.post(paystack_url, json=paystack_data, headers=headers)
#             paystack_response = response.json()

#             # Check if the Paystack initialization was successful
#             if response.status_code == 200 and paystack_response.get('status'):
#                 # Return the Paystack response to the client
#                 return Response(paystack_response, status=status.HTTP_200_OK)
#             else:
#                 # Handle Paystack initialization failure
#                 return Response({'error': 'Paystack initialization failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         except Order.DoesNotExist:
#             return Response({'error': 'Pending order not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             # Handle exceptions or errors during the payment initiation process
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class PaystackWebhookView(APIView):
    def post(self, request):
        try:
            payload = request.data
            print(f"Received reference in webhook payload: {payload}")
            event_data = payload.get('data', {})  # Access the 'data' key in the payload
            reference = event_data.get('reference')  # Retrieve the 'reference' field from 'data'

            print(f"Received reference in webhook payload: {reference}")  # Print the reference value
            status = payload.get('status')

            # user = self.request.user
            

            try:
                # order = Order.objects.filter(user=user, is_completed=False, status='pending').first()
                order = Order.objects.get(paystack_reference=reference)
            except Order.DoesNotExist:
                raise Http404('Order not found')

            if order:
                if status == 'success':
                    order.status = 'completed'
                    order.is_completed = True
                    order.completed_at = timezone.now()

                    # # Logic to generate the receipt document
                    # # receipt_content = f"Receipt for Order #{order.id}\nTotal Amount: {order.total_amount}"  # Replace with your receipt content generation logic
                    # pdf_buffer = generate_pdf_receipt(order)

                    # # Save the generated receipt to the 'receipt' field
                    # order.receipt.save(f"receipt_order_{order.id}.txt", pdf_buffer, save=True)

                    # # Sending email to buyer
                    # buyer_email = order.user.email
                    # subject_buyer = 'Order Receipt'
                    # message_buyer = 'Thank you for your order! Please find your receipt attached.'
                    # send_mail(subject_buyer, message_buyer, settings.EMAIL_HOST_USER, [buyer_email], fail_silently=False, attachment=[order.receipt.path])

                    # # Sending email to sellers (Replace this logic with actual identification of sellers)
                    # # For example, if each product has a seller field, you could do something like this:
                    # # Get all products in the order and notify their sellers
                    # products = order.products.all()
                    # sellers_emails = list(products.values_list('seller__user__email', flat=True).distinct())

                    # if sellers_emails:
                    #     subject_seller = 'New Order Notification'
                    #     message_seller = f'Your product has been ordered. Order ID: {order.id}'
                    #     send_mail(subject_seller, message_seller, settings.EMAIL_HOST_USER, sellers_emails, fail_silently=False)

                    order.save()

                    return Response({'message': 'Order status updated. Receipt sent to the buyer and notification sent to sellers.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Order status not updated'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Http404({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        except Order.DoesNotExist:
            return Http404({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def generate_pdf_receipt(order):
    # Create a BytesIO buffer to write the PDF content
    buffer = BytesIO()

    # Create a new PDF document
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set the receipt content based on order details
    receipt_content = f"Receipt for Order #{order.id}\nTotal Amount: {order.total_amount}"
    # You can add more details to the receipt content as needed

    # Draw the receipt content on the PDF
    pdf.drawString(100, 700, receipt_content)  # Adjust the position and styling as needed

    # Save the PDF document
    pdf.save()

    # Move the buffer's pointer back to the beginning
    buffer.seek(0)

    return buffer





class PaystackPaymentCallbackView(APIView):
    def post(self, request):
        try:
            reference = request.data.get('reference')  # Get reference from frontend
            # Call Paystack verify API
            verify_url = f'https://api.paystack.co/transaction/verify/{reference}'
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            }
            response = requests.get(verify_url, headers=headers)
            if response.status_code == 200:
                # Process Paystack verify API response
                # Update order status based on payment success/failure
                # Return success or failure response
                return Response({'message': 'Payment verified'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to verify payment'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










































# class CheckoutInitiationView(APIView):
#     def post(self, request):
#         try:
#             # Fetch user's cart items
#             cart_items = CartItem.objects.filter(user=request.user)
            
#             # Calculate total amount based on cart items
#             total_amount = calculate_total_amount(cart_items)
            
#             # Create an order for the user
#             order = Order.objects.create(user=request.user, total_amount=total_amount)

#             # Serialize order details
#             serializer = OrderSerializer(order) 

#             # Return serialized order details for the checkout process
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             # Handle exceptions or errors during order creation or calculation
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

# def calculate_total_amount(cart_items):
#     # Calculate the total amount based on cart items
#     total_amount = sum(item.product.price * item.quantity for item in cart_items)
#     return total_amount





# import uuid
# class CheckoutInitiationView(APIView):
#     def post(self, request):
#         try:
#             # Retrieve necessary details from the request or your database
#             # email = request.data.get('email')  # Assuming email is passed in the request
#             # amount = request.data.get('amount')  # Assuming amount is passed in the request
#             email = self.request.user.email
#             # order = Order.objects.filter(user=request.user)
#             # serializer = OrderSerializer(order) 
#             amount = self.request.user.Order.total_amount
#             tx_ref = str(uuid.uuid4())
#             reference = tx_ref  # Generate a unique reference for the transaction

#             paystack_data = {
#                 'email': email,
#                 'amount': amount * 100,  # Convert amount to the lowest currency unit (kobo in this case)
#                 'currency': 'NGN',  # Replace with your desired currency code
#                 'ref': reference,  # Use the generated reference
#                 # Add more parameters as needed based on your requirements
#             }

#             paystack_url = 'https://api.paystack.co/transaction/initialize'
#             headers = {
#                 'Authorization': f'Bearer PAYSTACK_SECRET_KEY',  # Replace with your Paystack secret key
#                 'Content-Type': 'application/json',
#             }

#             # Make a POST request to initialize the transaction
#             response = requests.post(paystack_url, json=paystack_data, headers=headers)
#             paystack_response = response.json()

#             # Check if the Paystack initialization was successful
#             if response.status_code == 200 and paystack_response.get('status'):
#                 # Return the Paystack response to the client
#                 return Response(paystack_response, status=status.HTTP_200_OK)
#             else:
#                 # Handle Paystack initialization failure
#                 return Response({'error': 'Paystack initialization failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         except Exception as e:
#             # Handle exceptions or errors during the payment initiation process
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





















































# import uuid

# class PaymentProcessingView(APIView):
#     def post(self, request):
#         # Collect payment details from the request data
#         # tx_ref = request.data.get('tx_ref')
#         amount = request.data.get('amount')
#         currency = request.data.get('currency', 'NGN')
#         redirect_url = request.data.get('redirect_url')
#         customer_email = request.data.get('customer_email')
#         # Other required and optional fields...

        

#         # Generate a unique transaction reference
#         tx_ref = str(uuid.uuid4())  # This creates a unique UUID-based reference

#         # Define the amount and currency for the transaction
#         # amount = "1000"  # For demonstration, assume it's 1000 units of the currency (e.g., 1000 NGN)
#         # currency = "NGN"  # Nigerian Naira

#         # Define the redirect URL after payment completion
#         # redirect_url = "https://127.0.0.1/api/user/process-payment/"

#         # Define the customer's email address
#         # email = self.request.user.email
#         # customer_email = "codegranites@gmail.com"


#         if not (tx_ref and amount and redirect_url and customer_email):
#             return Response({'error': 'Incomplete payment details'}, status=status.HTTP_400_BAD_REQUEST)

#         # Make a POST request to Flutterwave's API to initiate payment
#         your_flutterwave_secret_key = settings.FLW_SEC_KEY
#         headers = {
#             'Authorization': f'Bearer {your_flutterwave_secret_key}'
#         }

#         # Construct the payload for initiating the payment
#         payload = {
#             'tx_ref': tx_ref,
#             'amount': amount,
#             'currency': currency,
#             'redirect_url': redirect_url,
#             'customer_email': customer_email
#         }

#         print(payload)

#         try:
#             # Initiate payment
#             response = requests.post('https://api.flutterwave.com/v3/payments', json=payload, headers=headers)
#             if response.status_code == 200:
#                 data = response.json().get('data', {})
#                 payment_link = data.get('link')
#                 return Response({'payment_link': payment_link}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Payment initiation failed'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def get(self, request):
#         status = request.query_params.get('status')
#         tx_ref = request.query_params.get('tx_ref')
#         transaction_id = request.query_params.get('transaction_id')
#         # Other parameters...

#         if status == 'successful':
#             # Verify the transaction status with Flutterwave
#             verify_url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
#             your_flutterwave_secret_key = settings.FLW_SEC_KEY
#             headers = {
#                 'Authorization': f'Bearer {your_flutterwave_secret_key}'
#             }

#             try:
#                 # Verify transaction status
#                 response = requests.get(verify_url, headers=headers)
#                 if response.status_code == 200:
#                     transaction_data = response.json().get('data')
#                     if transaction_data.get('status') == 'successful':
#                         # Process the successful payment: Update your database, send confirmation emails, etc.
#                         order = Order.objects.get(tx_ref=tx_ref)
#                         order.status = 'paid'
#                         order.save()
                        
#                         # Send a confirmation email to the customer
#                         # Your email sending logic here...
                        
#                         return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)
#                     else:
#                         return Response({'message': 'Transaction verification failed'}, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     return Response({'message': 'Transaction verification failed'}, status=status.HTTP_400_BAD_REQUEST)
#             except Order.DoesNotExist:
#                 return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             # Handle cases where the transaction status isn't successful
#             return Response({'message': 'Payment verification failed'})
