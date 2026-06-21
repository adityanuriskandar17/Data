# ============================================
# OOP PYTHON UNTUK DATA ENGINEERING
# ============================================
# Konsep OOP yang relevan untuk data pipeline

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json

# --- ENCAPSULATION ---
class DatabaseConnection:
    def __init__(self, host: str, port: int, user: str, password: str):
        self.host = host
        self.port = port
        self._user = user          # protected
        self.__password = password  # private - name mangling

    def connect(self):
        print(f"Connecting to {self.host}:{self.port}")

    def _validate(self):
        """Internal method - hanya dipanggil di dalam class."""
        return len(self._user) > 0

# --- INHERITANCE ---
class PostgreSQLConnection(DatabaseConnection):
    def __init__(self, host, port, user, password, database):
        super().__init__(host, port, user, password)
        self.database = database

    def connect(self):
        # Override method parent
        print(f"Connecting to PostgreSQL at {self.host}:{self.port}/{self.database}")
        self._validate()

# --- ABSTRACTION ---
class DataSource(ABC):
    @abstractmethod
    def extract(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def load(self, data: List[Dict[str, Any]]):
        pass

    def run_pipeline(self):
        """Template method - urutan pipeline sudah ditentukan."""
        data = self.extract()
        transformed = self.transform(data)
        self.load(transformed)
        print("Pipeline selesai!")

class CSVToPostgresPipeline(DataSource):
    def __init__(self, csv_path: str, table: str):
        self.csv_path = csv_path
        self.table = table

    def extract(self):
        import csv
        with open(self.csv_path) as f:
            return list(csv.DictReader(f))

    def transform(self, data):
        for row in data:
            row["created_at"] = "2025-01-01"
        return data

    def load(self, data):
        print(f"Loading {len(data)} rows ke table {self.table}")

# --- POLYMORPHISM ---
class JSONDataSource(DataSource):
    def extract(self):
        with open("data.json") as f:
            return json.load(f)

    def transform(self, data):
        return [d for d in data if d.get("active")]

    def load(self, data):
        with open("output.json", "w") as f:
            json.dump(data, f)

# --- PENGGUNAAN ---
pipeline = CSVToPostgresPipeline("input.csv", "users")
pipeline.run_pipeline()
