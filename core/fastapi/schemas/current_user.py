from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    id: int = Field(None, description="ID")
    role_id: int = Field(None, description="Role ID")
    token: str = Field(None, description="Token")

    class Config:
        validate_assignment = True
