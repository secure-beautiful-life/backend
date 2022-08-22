from pydantic import BaseModel, Field


class RequestSuccessResponseSchema(BaseModel):
    message: str = Field("OK")


class BadRequestResponseSchema(BaseModel):
    error_code: str
    message: str


class DefaultOpenAPIResponseSchema:
    model: dict = {
        "400": {"model": BadRequestResponseSchema},
    }
