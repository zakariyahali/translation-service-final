# Making sure the data coming from the front end is validated
"""
I always insist on using schemas to have full control of the data flow from fe -> be.
"""



# schemas.py

from pydantic import BaseModel

class TranslationRequestSchema(BaseModel):
    text: str
    languages: str

    class Config:
        schema_extra = {
            "example": {
                "text": "Hello, world!",
                "languages": "english, german, russian"
            }
        }
