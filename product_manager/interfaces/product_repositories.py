from abc import ABC, abstractmethod
from typing import List, Optional
from product_manager.models.product_model import Product
class IProductReader(ABC):
    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all(self) -> List[Product]:
        pass

class IProductWriter(ABC):
    @abstractmethod
    def add(self, product: Product) -> Product:
        pass
    
    @abstractmethod
    def update(self, product: Product) -> bool:
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        pass

class IProductRepository(IProductReader, IProductWriter):
    pass