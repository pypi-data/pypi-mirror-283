import requests
import secrets

class VectorX:
    def __init__(self, token:str):
        self.token = token
        self.base_url = "https://vx.launchxlabs.ai"

    def __str__(self):
        return self.token

    def generate_key(self)->str:
        # Generate a random hex key of length 16
        key = secrets.token_hex(8)  # 8 bytes * 2 hex chars/byte = 16 chars
        print("Store this encryption key in a secure location. Loss of the key will result in the irreversible loss of associated vector data.\nKey: ",key)
        return key

    def create_index(self, name:str, size:int, key:str, distance:str):
        distance = distance.upper()
        if distance not in ["COSINE", "L2", "DOT_PRODUCT"]:
            raise ValueError(f"Invalid distance metric: {distance}")
        headers = {
            'Authorization': f'{self.token}',
            'Content-Type': 'application/json'
        }
        data = {
            'name': name,
            'size': size,
            'algo': distance,
            'checksum':self.checksum(key),
        }
        response = requests.post(f'{self.base_url}/index/create', headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(f"Error creating index: {response.text}")
        return "Index created successfully"

    def list_indexes(self):
        headers = {
            'Authorization': f'{self.token}',
        }
        response = requests.get(f'{self.base_url}/index/list', headers=headers)
        indexes = response.json()
        for index in indexes:
            index['name'] = index['name'].split('_')[2]
            # Delete checksum from index
            del index['checksum']
        return indexes

    def delete_index(self, name:str):
        headers = {
            'Authorization': f'{self.token}',
        }
        response = requests.get(f'{self.base_url}/index/{name}/delete', headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error deleting index: {response.text}")
        return f'Index {name} deleted successfully'

    def checksum(self, key:str)->int:
        # Convert last two characters of key to integer
        return int(key[-2:], 16)



