from pydantic import BaseModel


class CompanySchema(BaseModel):
    id: int
    name: str
    address: str
    email: str

    class Config:
        from_attributes = True


class ItemSchema(BaseModel):  # serializer
    id: int
    name: str
    description: str
    price: int
    on_offer: bool
    company_id: int

    class Config:
        from_attributes = True


