import requests

BaseUrl = "http://127.0.0.1:8000"

payload = {
    "name": "Abdulrahman",
    "lastname": "Hendieh",
    "username": "alamarchal",
    "age": 22,
    "email": "abdulrahmanhendieh@gmail.com",
    "gender": "man",
    "phone_number": "0707708921",
    "password": "abdulrahman11111"
}

payload_2 = {
    "name": "Sara",
    "lastname": "Nilsson",
    "username": "saran",
    "age": 25,
    "email": "sara.nilsson@example.com",
    "gender": "kvinna",
    "phone_number": "0701234567",
    "password": "sarapassword123"
}

payload_3 = {
    "name": "Omar",
    "lastname": "Ali",
    "username": "omar_ali",
    "age": 28,
    "email": "omar.ali@example.com",
    "gender": "man",
    "phone_number": "0739876543",
    "password": "omarsecurepass"
}

payload_4 = {
    "name": "Elin",
    "lastname": "Karlsson",
    "username": "elink",
    "age": 23,
    "email": "elin.karlsson@example.com",
    "gender": "kvinna",
    "phone_number": "0765554433",
    "password": "elinpassword99"
}

log_data = {
    'email': payload["email"],
    'password': payload["password"]
}

def create_user():
    
    response = requests.post(f"{BaseUrl}/user/create", json = payload)
    print(response.json())

def login():
    
    response = requests.post(f"{BaseUrl}/user/login", json =  log_data)
    print(response.json())


def test_delete_account():
    
    
    requests.post(f"{BaseUrl}/user/create", json = payload_2)

    login_data = {
        "email": "abdulrahmanhendieh@gmail.com",
        "password": "abdulrahman11111"
    }
    
    login_response = requests.post(f"{BaseUrl}/user/login", json=login_data)
    token = login_response.json().get("access_token")
    
    if not token:
        print("Kunde inte logga in. Kontrollera uppgifterna.")
        return

    headers = {
        "Authorization": f"Bearer {token}"
    }

    target_username = "alamarchal"

    delete_response = requests.delete(
        f"{BaseUrl}/user/delete?username={target_username}", 
        headers=headers
    )

    print("Statuskod:", delete_response.status_code)
    
    try:
        print("Svar från servern:", delete_response.json())
    except Exception:
        print("Svar från servern:", delete_response.text)
        
def logout_user():
    
    response = requests.post(f"{BaseUrl}/user/create", json = payload_4)
    print(response.json())
    
    login_data = {
        "email": payload_4["email"],
        "password": payload_4["password"]
    }
    
    # 1. Logga in
    login_response = requests.post(f"{BaseUrl}/user/login", json=login_data)
    
    if login_response.status_code != 200:
        print("Inloggning misslyckades:", login_response.json())
        return
        
    login_out_data = login_response.json()
    access_token = login_out_data["access_token"]
    
    # 2. Förbered authorization-header
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # 3. Skicka logout-anrop
    response = requests.post(f"{BaseUrl}/user/logout", headers=header)
    
    print("Logout Statuskod:", response.status_code)
    print("Logout Svar:", response.json())
    

def refresh_user_access_token():
    
    requests.post(f"{BaseUrl}/user/create", json = payload_4)
   
      
    login_data = {
          "email": payload_4["email"],
          "password": payload_4["password"]
      }
      
      # 1. Logga in
    login_response = requests.post(f"{BaseUrl}/user/login", json=login_data)
      
    if login_response.status_code != 200:
          print("Inloggning misslyckades:", login_response.json())
          return
          
    login_out_data = login_response.json()
    refresh_token = login_out_data["refresh_token"]
    
    refresh_data = {
        "refresh_token": refresh_token
    }
    response_r = requests.post(f"{BaseUrl}/user/refresh", json = refresh_data)
    
    print(response_r.json())



refresh_user_access_token()
  
    
    
    






