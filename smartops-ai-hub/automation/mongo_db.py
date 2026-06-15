import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoDBManager:
    """
    CONECTOR NOSQL: Se encarga de la conexión directa con MongoDB.
    Si MongoDB está apagado, tiene un sistema de respaldo para que el proyecto no se caiga.
    """
    def __init__(self):
        # Lee la URI desde el entorno o usa el localhost por defecto de Docker
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        try:
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
            self.client.admin.command('ping')  # Verifica si la base de datos responde
            self.db = self.client['smartops_ai_database']
            self.logs_collection = self.db['ai_execution_logs']
            self.is_connected = True
        except ConnectionFailure:
            self.is_connected = False
            self.logs_collection = None

    def save_log(self, document):
        """Guarda el JSON completo en Mongo y devuelve su ID de 24 caracteres"""
        if self.is_connected and self.logs_collection is not None:
            result = self.logs_collection.insert_one(document)
            return str(result.inserted_id)
        return "ID_MOCK_MONGO_OFFLINE_12345"
