from typing import List, Optional
from product_manager.models import Product
from product_manager.interfaces.product_repositories import IProductRepository

class ProductRetriever:
    def __init__(self, repository: IProductRepository):
        self.repository = repository

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.repository.get_by_id(product_id)

    def get_all(self) -> List[Product]:
        return self.repository.get_all()