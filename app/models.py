from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr, IPvAnyAddress

### Market ###

class MarketBag(BaseModel):
    # pip install 'pydantic[email]'
    id: str = None
    pw: str = None
    item: str = None



### User ###

class UserRegister(BaseModel):
    # pip install 'pydantic[email]'
    email: str = None
    pw: str = None
    name: str = None
    nick_name: str = None
    phone_number: str = None

class UserLogin(BaseModel):
    # pip install 'pydantic[email]'
    email: str = None
    pw: str = None

class SnsType(str, Enum):
    email: str = "email"
    facebook: str = "facebook"
    google: str = "google"
    kakao: str = "kakao"


class Token(BaseModel):
    Authorization: str = None


class EmailRecipients(BaseModel):
    name: str
    email: str


class SendEmail(BaseModel):
    email_to: List[EmailRecipients] = None


class KakaoMsgBody(BaseModel):
    msg: str = None


class MessageOk(BaseModel):
    message: str = Field(default="OK")


class UserToken(BaseModel):
    id: int
    email: str = None
    name: str = None
    phone_number: str = None
    profile_img: str = None
    sns_type: str = None

    class Config:
        orm_mode = True


class UserMe(BaseModel):
    id: int
    email: str = None
    name: str = None
    phone_number: str = None
    profile_img: str = None
    sns_type: str = None

    class Config:
        orm_mode = True


class AddApiKey(BaseModel):
    user_memo: str = None

    class Config:
        orm_mode = True


class GetApiKeyList(AddApiKey):
    id: int = None
    access_key: str = None
    created_at: datetime = None


class GetApiKeys(GetApiKeyList):
    secret_key: str = None


class CreateAPIWhiteLists(BaseModel):
    ip_addr: str = None


class GetAPIWhiteLists(CreateAPIWhiteLists):
    id: int

    class Config:
        orm_mode = True



### Recipe ###

class Recipe(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[list] = None
    is_public: Optional[bool] = False


class RecipeCreate(Recipe):
    category_id: int
    name: str
    description: str
    ingredients: List[str]

    class Config:
        schema_extra = {
            "example": {
                "category_id": 1,
                "name": "Example Ingredient",
                "description": "Sample summarized description instruction",
                "ingredients": ["150ml ingredient 1", "2 tsp mixed ingredient"],
                "is_public": False,
            }
        }


class RecipeUpdate(Recipe):
    pass


class RecipeInDB(Recipe):  # shared by models in DB
    id: int
    name: str
    owner_id: int
    category_id: int

    class Config:
        orm_mode = True


class Recipe(RecipeInDB):  # return to client
    pass


class RecipeInDB(RecipeInDB):  # DB store
    pass

###