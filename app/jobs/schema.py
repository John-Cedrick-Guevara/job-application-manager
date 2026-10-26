from datetime import date

from pydantic import BaseModel, ConfigDict, Field

class JobBase(BaseModel):
    title: str = Field(min_length=2, max_length=200, example="Software Engineer")
    company: str = Field(min_length=2, max_length=200, example="Tech Company")
    location: str = Field(min_length=2, max_length=200, example="San Francisco, CA")
    description: str = Field(min_length=2, max_length=500, example="Job description goes here.")
    source: str = Field(min_length=2, max_length=200, example="LinkedIn")
    posted_at: date = Field(default=None, example="2023-01-01")

class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    pass

class JobRead(JobBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class JobDelete(JobRead):
    pass