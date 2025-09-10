from product_manager.repositories.repository import ProductRepository

class ProductDeleter:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def delete(self, product_id: int) -> bool:
        return self.repository.delete(product_id)