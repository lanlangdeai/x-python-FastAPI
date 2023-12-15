from typing import Optional

from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    content: str
    published: Optional[bool]




