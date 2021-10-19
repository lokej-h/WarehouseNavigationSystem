class Shelf:
    """Shelf type"""

    def __init__(self, pid, x, y):
        self.pids = pid
        self.x = x
        self.y = y

    def __str__(self):
        return f"Shelf at ({self.x}. {self.y}) containing items {self.pids}"

    def __repr__(self):
        return str(self)