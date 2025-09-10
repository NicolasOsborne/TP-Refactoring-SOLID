from dataclasses import dataclass

@dataclass
class Product:
    id: int = None
    name: str = None
    description: str = None
    price: float = None
    category: str = None