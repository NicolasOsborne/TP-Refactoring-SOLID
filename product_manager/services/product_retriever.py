from typing import List, Optional
from product_manager.models import Product
from product_manager.repositories.repository import ProductRepository

class ProductRetriever:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.repository.get_by_id(product_id)

    def get_all(self) -> List[Product]:
        return self.repository.get_all()