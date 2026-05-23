from pydantic import BaseModel, Field, field_validator, HttpUrl
from datetime import date, datetime, timedelta
from typing import List, Optional, Literal


class GenreBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ActorBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class LanguageBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CountryBase(BaseModel):
    id: int
    code: str
    name: Optional[str]

    class Config:
        from_attributes = True


class MovieListItemSchema(BaseModel):
    id: int
    name: str
    date: date
    score: float
    overview: Optional[str]

    class Config:
        from_attributes = True


class MovieFull(MovieListItemSchema):
    status: str
    budget: float
    revenue: float
    country: Optional[CountryBase]
    genres: List[GenreBase]
    actors: List[ActorBase]
    languages: List[LanguageBase]


class MovieCreate(BaseModel):
    name: str = Field(..., max_length=255)
    date: date
    score: float = Field(..., ge=0, le=100)
    overview: str
    status: Literal["Released", "Post Production", "In Production"]
    budget: float = Field(..., ge=0)
    revenue: float = Field(..., ge=0)
    country: str
    genres: List[str]
    actors: List[str]
    languages: List[str]

    @field_validator("date")
    @classmethod
    def date_not_too_far_future(cls, v):
        if v > date.today() + timedelta(days=365):
            raise ValueError("Date cannot be more than one year in the future")
        return v


class MovieUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    date: Optional[date] = None
    score: Optional[float] = Field(None, ge=0, le=100)
    overview: Optional[str] = None
    status: Optional[Literal["Released", "Post Production", "In Production"]] = None
    budget: Optional[float] = Field(None, ge=0)
    revenue: Optional[float] = Field(None, ge=0)


class MovieListResponseSchema(BaseModel):
    movies: List[MovieListItemSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int


class MovieDetailSchema(MovieFull):
    pass
