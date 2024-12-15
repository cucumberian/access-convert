from pydantic import BaseModel, Field


class DbConnectSchema(BaseModel):
    host: str = Field(..., description="Host")
    port: int = Field(..., description="Port")
    user: str = Field(..., description="User")
    password: str = Field(..., description="Password")
    database: str = Field(..., description="Database")