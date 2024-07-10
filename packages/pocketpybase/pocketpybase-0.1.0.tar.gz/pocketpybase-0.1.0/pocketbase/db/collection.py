from deps.auths import Auths
import httpx

class Collection:
    def __init__(self, pb, collection_name):
        self.pb = pb
        self.collection_name = collection_name
        self.auths = Auths(pb.username, pb.password, pb.host_url)
        self.session = httpx.Client()
    def status_error(self, response):
        if response.status_code == 400:
            raise Exception("Validation failed")
        elif response.status_code == 403:
            raise Exception("Only admins can create collections")
        elif response.status_code == 404:
            raise Exception("Collection not found")
        elif response.status_code != 200:
            raise Exception("Failed to create collection, status code: " + str(response.status_code)) 
        else:
            return
        
    def create_record(self, record):
        token = self.auths.get_token()
        response = self.session.post(
            f'{self.pb.host_url}/api/collections/{self.collection_name}/records',
            json=record,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        self.status_error(response)
        return response.json()

    def get_record_by_id(self, record_id):
        token = self.auths.get_token()
        response = self.session.get(
            f'{self.pb.host_url}/api/collections/{self.collection_name}/records/{record_id}',
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        self.status_error(response)
        return response.json()

    def update_record(self, record_id, record):
        token = self.auths.get_token()
        response = self.session.patch(
            f'{self.pb.host_url}/api/collections/{self.collection_name}/records/{record_id}',
            json=record,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        self.status_error(response)
        return response.json()

    def delete_record(self, record_id):
        token = self.auths.get_token()
        response = self.session.delete(
            f'{self.pb.host_url}/api/collections/{self.collection_name}/records/{record_id}',
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        print(response.status_code)
        if response.status_code != 204:
            raise Exception("Failed to delete record")
        return
    
    def create_collection(self, collection, db_type, schema):
        token = self.auths.get_token()
        response = self.session.post(
            f'{self.pb.host_url}/api/collections',
            json={
                "name": collection,
                "type": db_type,
                "schema": schema
            },
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        self.status_error(response)
        return response.json()