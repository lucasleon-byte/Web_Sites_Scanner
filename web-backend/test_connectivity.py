from pymongo import MongoClient
from pymongo.errors import PyMongoError

def test_mongo_connection():
    try:
        
        client = MongoClient("mongodb+srv://leonvunic:Nogomet123@clusterdiplomski.rqewm.mongodb.net/?retryWrites=true&w=majority&ssl=true")
        
        
        server_info = client.server_info() 
        print("Uspješna konekcija")
        print("Server info:", server_info)
        
    except ConnectionError:
        print("Neuspjela konekcija ")
    except Exception as e:
        print(f"greška: {e}")

if __name__ == "__main__":
    test_mongo_connection()
