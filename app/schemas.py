from pydantic import BaseModel


class QueryLawsRequest(BaseModel):
    inquiry: str
