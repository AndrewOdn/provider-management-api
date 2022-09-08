from pydantic import BaseModel, Field, constr


class base500(BaseModel):
    title: str = 'Internal Server Error'


class base_header(BaseModel):
    """
    eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im1hbmFnZXIwMDYiLCJ1c2VyX2lkIjo4OSwiY3JlYXRlZCI6MTY2MjQ3MzQ3ODIxN30.kMC4lmZBFTuePQa494tdqaxbioE13H8I3fwy_2e5KxE
    """
    authorization: str


class base401(BaseModel):
    title: str
