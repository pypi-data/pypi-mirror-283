import requests
from .libvx import encode, decode
from .vectorx import VectorX
from .crypto import encrypt_ecb, decrypt_ecb

class Index:
    def __init__(self, name:str, key:str, vx:VectorX):
        self.name = name
        self.key = key
        self.vx = vx

    def __str__(self):
        return self.name

    def upsert(self, vectors):
        checksum = self.vx.checksum(self.key)
        for vector in vectors:
            vector["vector"] = encode(self.key, vector["vector"])
            vector["meta"] = encrypt_ecb(self.key, vector["meta"])

        headers = {
            'Authorization': f'{self.vx.token}',
            'Content-Type': 'application/json'
        }
        data = {
            'checksum': checksum,
            'vectors': vectors,
        }
        response = requests.post(f'{self.vx.base_url}/vector/{self.name}/upsert', headers=headers, json=data)
        print(response.text)
        if response.status_code != 200:
            raise Exception(f"Error upserting vectors: {response.text}")
        return "Vectors inserted successfully"

    def query(self, vector):
        checksum = self.vx.checksum(self.key)
        vector = encode(self.key, vector)
        headers = {
            'Authorization': f'{self.vx.token}',
            'Content-Type': 'application/json'
        }
        data = {
            'checksum': checksum,
            'vector': vector,
        }
        response = requests.post(f'{self.vx.base_url}/vector/{self.name}/query', headers=headers, json=data)
        print(response.text)
        if response.status_code != 200:
            raise Exception(f"Error querying vectors: {response.text}")
        resp_json = response.json()
        for result in resp_json:
            result["vector"] = decode(self.key, result["vector"])
            result["meta"] = decrypt_ecb(self.key, result["meta"])
        return response.json()

    def delete(self, id):
        checksum = self.vx.checksum(self.key)
        headers = {
            'Authorization': f'{self.vx.token}',
            }
        resp = requests.get(f'{self.vx.base_url}/vector/{self.name}/delete/{id}', headers=headers)
        print(resp.text)
        return f'Vector {id} deleted successfully'
