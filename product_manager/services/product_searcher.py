from typing import List, Optional
from product_manager.models.product_model import Product
from product_manager.interfaces.product_repositories import IProductReader

class ProductSearcher:
    def __init__(self, reader: IProductReader):
        self.reader = reader

    def find_by_category(self, category: str) -> List[Product]:
        return self.reader.get_by_category(category)