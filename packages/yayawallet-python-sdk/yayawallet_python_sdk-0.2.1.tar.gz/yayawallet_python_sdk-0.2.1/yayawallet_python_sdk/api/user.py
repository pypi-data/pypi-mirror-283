from ..functions.api_request import api_request

async def get_organization():
  api_response = await api_request("GET", "/user/organization", "", None)
  return api_response

async def get_profile():
  api_response = await api_request("GET", "/user/profile", "", None)
  return api_response

async def search_user(query: str):
  api_response = await api_request("POST", "/user/search", "", { "query": query })
  return api_response

async def create_customer_user(invitation_hash: str, name: str, email: str, phone: str, gender: str, date_of_birth: str, region: str, country: str, address: str, password: str, account_name: str, fin: str, photo_base64: str, id_front_base64: str, id_back_base64: str, meta_data: str):
  api_response = await api_request("POST", "/user/register", "", {"invitation_hash": invitation_hash, "name": name, "email": email, "phone": phone, "gender": gender, "date_of_birth": date_of_birth, "region": region, "country": country, "address": address, "password": password, "account_name": account_name, "fin": fin, "photo_base64": photo_base64, "id_front_base64": id_front_base64, "id_back_base64": id_back_base64, "meta_data": meta_data})
  return api_response

async def create_business_user(invitation_hash: str, name: str, email: str, phone: str, gender: str, date_of_birth: str, region: str, country: str, address: str, password: str, account_name: str, fin: str, photo_base64: str, id_front_base64: str, id_back_base64: str, tin_number: str, license_number: str, tin_doc_base64: str, license_doc_base64: str, meta_data: str):
  api_response = await api_request("POST", "/user/register-business", "", {"invitation_hash": invitation_hash, "name": name, "email": email, "phone": phone, "gender": gender, "date_of_birth": date_of_birth, "region": region, "country": country, "address": address, "password": password, "account_name": account_name, "fin": fin, "photo_base64": photo_base64, "id_front_base64": id_front_base64, "id_back_base64": id_back_base64, "tin_number": tin_number, "license_number": license_number, "tin_doc_base64": tin_doc_base64, "license_doc_base64": license_doc_base64, "meta_data": meta_data})
  return api_response