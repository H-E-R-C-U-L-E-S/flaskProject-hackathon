import sqlite3
from sentence_transformers import SentenceTransformer
from semantic_search import semantic_search

class Database:
    def __init__(self, db_file='ecom_products.db'):
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def __connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def __disconnect(self):
        self.cursor.close()
        self.conn.close()

    def add_product(self, name,type, brand, specifications, price):
        self.__connect()
        # Load pre-trained model for generating embeddings
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        # Generate embedding for the phone's specifications
        embedding = model.encode([specifications])[0]

        # Insert the phone into the database
        self.cursor.execute(
            "INSERT INTO products (name,type, brand, specifications, price, embedding) VALUES (?, ?, ?, ?, ?,?)",
            (name,type, brand, specifications, price, embedding.tobytes()))

        self.conn.commit()
        self.__disconnect()

    def filter_by_type(self, type):
        self.__connect()
        self.cursor.execute(
            "SELECT id, name, brand, specifications, price, embedding FROM products WHERE type = ?",
            (type,))
        rows = self.cursor.fetchall()
        self.__disconnect()
        return rows
    def filter_by_price(self, max_price, min_price= 0):
        self.__connect()
        self.cursor.execute(
            "SELECT id, name, brand, specifications, price, embedding FROM products WHERE price between ? AND ?",
            (min_price, max_price))
        rows = self.cursor.fetchall()
        self.__disconnect()
        return rows

    def filter_by_brand(self, brand):
        self.__connect()
        self.cursor.execute(
            "SELECT id, name, brand, specifications, price, embedding FROM products WHERE LOWER(brand) = LOWER(?)",
            (brand,))
        rows = self.cursor.fetchall()
        self.__disconnect()
        return rows


    def get_all_products(self):
        self.__connect()
        self.cursor.execute("SELECT id, name, brand, specifications, price, embedding FROM products")
        rows = self.cursor.fetchall()
        self.__disconnect()
        return rows
