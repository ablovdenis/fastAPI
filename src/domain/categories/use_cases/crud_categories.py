from typing import List

from sqlalchemy.orm import Session

from ....infrastructure.sqlite.repositories.categories import CategoryRepository
from ....schems.categories import CategoryOut, CategoryUpdateAndCreate



class MethodsForCategory:
    def __init__(self):
        self._repo = CategoryRepository()

    def get(self, DataBase: Session, skip: int, limit: int) -> List[CategoryOut]:
        return [CategoryOut.model_validate(user) for user in self._repo.get(DataBase, skip, limit)]

    def get_detail(self, DataBase: Session, category_slug: str) -> CategoryOut:
        return CategoryOut.model_validate(self._repo.get_detail(DataBase, category_slug))

    def create(self, DataBase: Session, payload: CategoryUpdateAndCreate) -> CategoryOut:
        return CategoryOut.model_validate(self._repo.create(DataBase, payload))

    def update(self, DataBase: Session, category_slug: str, payload: CategoryUpdateAndCreate) -> CategoryOut:
        return CategoryOut.model_validate(self._repo.update(DataBase, category_slug, payload))
    
    def destroy(self, DataBase: Session, category_slug: str):
        self._repo.destroy(DataBase, category_slug)