from pymongo import MongoClient
from pymongo.errors import PyMongoError

def test_mongo_connection():
    try:
        # Zamijenite ovo sa svojom konekcijskom strunom
        client = MongoClient("mongodb+srv://leonvunic:Nogomet123@clusterdiplomski.rqewm.mongodb.net/?retryWrites=true&w=majority&ssl=true")
        
        # Pokušajte dohvatiti informacije o serveru
        server_info = client.server_info() 
        print("Uspješna konekcija s MongoDB!")
        print("Server info:", server_info)
        
    except ConnectionError:
        print("Neuspjela konekcija s MongoDB. Provjerite konekcijski string.")
    except Exception as e:
        print(f"Dogodila se greška: {e}")

if __name__ == "__main__":
    test_mongo_connection()
