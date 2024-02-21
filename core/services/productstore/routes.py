from fastapi import APIRouter, Depends, HTTPException, Response, status
from .schemas import CompanySchema, ItemSchema
from .models import Company, Item
from core.constants import ALREADY_EXISTS, INTERNAL_ERROR, NOT_FOUND
from core.middleware.db_middleware import SessionLocal
from typing import List

router = APIRouter()

db = SessionLocal()


@router.get('/companies', response_model=List[CompanySchema], status_code=200)
def get_all_companies():
    """
    Retrieves all companies from the database.

    Returns:
        List[CompanySchema]: A list of company data represented by `CompanySchema` objects.

    Raises:
        HTTPException: An error occurred while retrieving companies.
    """
    try:
        company_obj = db.query(Company).all()
        return company_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve companies: {str(e)}")


@router.post('/company', response_model=CompanySchema, status_code=status.HTTP_201_CREATED)
def crerate_company(company: CompanySchema):
    """
    Creates a new company in the database.

    Args:
        company: A JSON object representing the new company data (validated against `CompanySchema`).

    Returns:
        CompanySchema: The newly created company data as a `CompanySchema` object.

    Raises:
        HTTPException:
            - 400 Bad Request: If a company with the same name already exists.
            - 500 Internal Server Error: If an unexpected error occurs during creation.
    """
    db_company = db.query(Company).filter(Company.name == company.name).first()
    if db_company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ALREADY_EXISTS)
    try:
        new_company = Company(
            name=company.name,
            address=company.address,
            email=company.address
        )
        db.add(new_company)
        db.commit()

        return new_company
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=INTERNAL_ERROR) from e


# ----------------------------- Item Model end Point -----------------------

@router.get('/items', response_model=List[ItemSchema], status_code=200)
def get_all_items():
    """
    Retrieves all items from the database.

    Returns:
        List[ItemSchema]: A list of item data represented by `ItemSchema` objects.

    Raises:
        HTTPException: An unexpected error occurred while retrieving items.
    """

    try:
        items = db.query(Item).all()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{INTERNAL_ERROR}: {str(e)}")


@router.get('/item/{item_id}', response_model=ItemSchema, status_code=status.HTTP_200_OK)
def get_an_item(item_id: int):
    """
    Retrieves an item by its ID from the database.

    Args:
        item_id (int): The unique identifier of the item to retrieve.

    Returns:
        ItemSchema: The retrieved item data as a `ItemSchema` object.

    Raises:
        HTTPException:
            - 404 Not Found: If no item is found with the provided ID.
    """

    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    return item


@router.post('/items', response_model=ItemSchema, status_code=status.HTTP_201_CREATED)
def create_an_item(item: ItemSchema) -> ItemSchema:
    """
    Creates a new item in the database.

    Args:
        item (ItemSchema): A JSON object representing the new item data (validated against `ItemSchema`).

    Returns:
        ItemSchema: The newly created item data as a `ItemSchema` object.

    Raises:
        HTTPException:
            - 400 Bad Request: If an item with the same name already exists.
            - 500 Internal Server Error: If an unexpected error occurs during creation.
    """

    db_item = db.query(Item).filter(Item.name == item.name).first()

    if db_item is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ALREADY_EXISTS)
    try:
        new_item = Item(
            name=item.name,
            price=item.price,
            description=item.description,
            on_offer=item.on_offer,
            company_id=item.company_id
        )

        db.add(new_item)
        db.commit()

        return new_item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=INTERNAL_ERROR) from e


@router.put('/item/{item_id}', response_model=ItemSchema, status_code=status.HTTP_200_OK)
def update_an_item(item_id: int, item: ItemSchema) -> ItemSchema:
    """
    Updates an existing item in the database.

    Args:
        item_id (int): The unique identifier of the item to update.
        item (ItemSchema): A JSON object containing the updated item data.

    Returns:
        ItemSchema: The updated item data as a `ItemSchema` object.

    Raises:
        HTTPException:
            - 404 Not Found: If no item is found with the provided ID.
    """
    item_to_update = db.query(Item).filter(Item.id == item_id).first()
    if not item_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)

    item_to_update.name = item.name
    item_to_update.price = item.price
    item_to_update.description = item.description
    item_to_update.on_offer = item.on_offer
    item_to_update.company_id = item.company_id

    db.commit()

    return item_to_update


@router.delete('/item/{item_id}')
def delete_item(item_id: int):
    """
    Deletes an item from the database by its ID.

    Args:
        item_id (int): The unique identifier of the item to delete.

    Raises:
        HTTPException:
            - 404 Not Found: If no item is found with the provided ID.
    """

    item_to_delete = db.query(Item).filter(Item.id == item_id).first()

    if not item_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)

    db.delete(item_to_delete)
    db.commit()

    return item_to_delete
