from rest_framework.authentication import TokenAuthentication

class TokenAuthentication(TokenAuthentication):
    """
        Changes the default header keyword from 'Token' to 'Bearer'.
    """
    keyword = 'Bearer'