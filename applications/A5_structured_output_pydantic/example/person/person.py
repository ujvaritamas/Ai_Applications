from pydantic import BaseModel, Field
import json
from typing import Any, Literal

class Person(BaseModel):
    """A person is a human being with the denoted attributes."""

    name: str = Field(..., 
        description="Which is the name of the person?"
    )
    age: int = Field(..., 
        description="Which is the age of the person?"
    )
    email: str = Field(..., 
        description="Which is the email of the person?"
    )
    country: Literal["Germany", "Switzerland", "Austria"] = Field(..., 
        description="In which country does the person reside?"
    )

