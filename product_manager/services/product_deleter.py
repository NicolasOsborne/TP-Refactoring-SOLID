from product_manager.interfaces.product_repositories import IProductRepository
class ProductDeleter:
    def __init__(self, repository: IProductRepository):
        self.repository = repository

    def delete(self, product_id: int) -> bool:
        return self.repository.delete(product_id)