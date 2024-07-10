from ..functions.api_request import api_request

from rest_framework import status

from django.http import StreamingHttpResponse

from ..serializers.user_serializers import CustomerUserSerializer, BusinessUserSerializer

async def get_organization():
  api_response = await api_request("GET", "/user/organization", "", None)
  return api_response

async def get_profile():
  api_response = await api_request("GET", "/user/profile", "", None)
  return api_response

async def search_user(query: str):
  api_response = await api_request("POST", "/user/search", "", { "query": query })
  return api_response

async def create_customer_user(data):
  serializer = CustomerUserSerializer(data=data)

  if serializer.is_valid():
      validated_data = serializer.validated_data
      api_response = await api_request("POST", "/user/register", "", **validated_data)
      return api_response
  else:
      return StreamingHttpResponse(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,\
      )
  
async def create_business_user(data):
  serializer = BusinessUserSerializer(data=data)

  if serializer.is_valid():
      validated_data = serializer.validated_data
      api_response = await api_request("POST", "/user/register-business", "", **validated_data)
      return api_response
  else:
      return StreamingHttpResponse(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,\
      )