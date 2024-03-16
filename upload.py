import os
import timeit
import sys
import json
import pathlib

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


from dotenv import load_dotenv
from cryptography.fernet import Fernet


load_dotenv()




BASE_DIR = pathlib.Path(__file__).parent


ferret_key = os.getenv("ENCRYPTION_KEY")
cipher = Fernet(ferret_key.encode())
ENCRYPTED_DATA = BASE_DIR / 'objects/encypt.txt'
JSON_FILE = BASE_DIR/'objects/dict5k_.json'

# Read the encrypted data from the file
with open(ENCRYPTED_DATA, 'rb') as file:
    encrypted_data = file.read()

# Decrypt the data
decrypted_data = cipher.decrypt(encrypted_data)

# Decoding the decrypted data
json_string = decrypted_data.decode()

# Load JSON
auth = json.loads(json_string)
cred = credentials.Certificate(auth)
firebase_admin.initialize_app(cred)




db = firestore.client()

#add DOCUMENTS
#dt = BASE_DIR/'objects/dict5k_.json'
#dt = {'name':'ay', 'age':'92', 'status':'married', 'employed':'True'}
#db.collection('dictionary').add(dt)

# Read JSON data from file
with open(JSON_FILE, 'rb') as f:
    json_data = json.load(f)

# Upload data to Firestore with custom numeric IDs
collection_name = "DICT"  # Collection name
batch = db.batch()
index = 1
for data in json_data:
    doc_ref = db.collection(collection_name).document(str(index))
    batch.set(doc_ref, data)
    index += 1
    if index % 500 == 0:  # Batch size for better performance
        batch.commit()
        batch = db.batch()

# Commit any remaining batch
if index % 500 != 0:
    batch.commit()

print("JSON data uploaded to Firestore successfully!")