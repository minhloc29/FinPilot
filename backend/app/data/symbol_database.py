"""
Symbol database (in-memory)
"""

from typing import List


class SymbolDatabase:

    def __init__(self, symbols: List[str]):

        self.symbols = set(
            s.upper() for s in symbols
        )

    def has_symbol(self, symbol: str) -> bool:

        return symbol.upper() in self.symbols

    def get_all_symbols(self) -> List[str]:

        return list(self.symbols)