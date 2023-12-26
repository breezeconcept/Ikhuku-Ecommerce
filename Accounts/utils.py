from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.response import Response

def get_user_id_from_jwt(request):
    """
    Extracts the user ID from the JWT token in the request.
    Returns the user ID if the token is valid, else returns None.
    """
    user_id = None
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            jwt_obj = JWTAuthentication()
            validated_token = jwt_obj.get_validated_token(token)
            user = jwt_obj.get_user(validated_token)
            user_id = user.id
    except AuthenticationFailed as e:
        # Handle exceptions if token validation fails
        return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
    
    return user_id
