class TranspositionTable:
    """局面評価キャッシュ"""

    def __init__(self):
        self.table = {}

    def get(self, key):
        return self.table.get(key)

    def put(self, key, value):
        self.table[key] = value

    def clear(self):
        self.table.clear()