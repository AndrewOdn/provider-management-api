"""
Base Pydantic models for all routes
"""
from pydantic import BaseModel


class Base500(BaseModel):
    """http500 response validation model"""

    title: str = "Internal Server Error"


class BaseHeader(BaseModel):
    """
    JWT token base header validation model
    Example:
    eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im1hbmFnZXIwMDYiLCJ1c2VyX2lkIjo4OSwiY3JlYXRlZCI6MTY2MjQ3MzQ3ODIxN30.kMC4lmZBFTuePQa494tdqaxbioE13H8I3fwy_2e5KxE
    """

    authorization: str


class Base401(BaseModel):
    """http401 response validation model"""

    title: str
