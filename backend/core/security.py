from ulid import ULID
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


#genererar en unik id med 32 bitar hexal som används som id for user och andra element 
def generate_ulid() -> str:
    return str(ULID())

#genererar en hashed?password
def get_password_hashed(password):
    return password_hash.hash(password)

#varifererar arr en password är rätt
def verify_password(plain_password, hash_password):
    return password_hash.verify(plain_password, hash_password)










