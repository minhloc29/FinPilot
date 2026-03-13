"""
Resolve stock symbols from user query
"""

from app.data.symbol_database import SymbolDatabase
import re

class SymbolResolver:

    def __init__(self, symbol_db: SymbolDatabase):

        self.symbol_db = symbol_db

    def resolve(self, message: str):

        tokens = re.findall(r"[A-Z]{2,4}", message.upper())

        for token in tokens:

            if self.symbol_db.has_symbol(token):

                return token

        return None