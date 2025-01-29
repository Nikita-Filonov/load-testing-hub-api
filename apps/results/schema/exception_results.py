from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field

from utils.schema.database import DatabaseSchema
from utils.schema.query import QuerySchema


class ExceptionResult(DatabaseSchema):
    id: int
    message: str
    number_of_exceptions: int = Field(alias="numberOfExceptions")


class ExceptionResultDetails(ExceptionResult):
    details: str


class CreateExceptionResult(BaseModel):
    message: str
    details: str
    number_of_exceptions: int = Field(alias="numberOfExceptions")


class GetExceptionResultsQuery(QuerySchema):
    load_test_result_id: int = Field(alias="loadTestResultId")

    @classmethod
    async def as_query(
            cls,
            load_test_result_id: int = Query(alias="loadTestResultId")
    ) -> Self:
        return GetExceptionResultsQuery(
            load_test_result_id=load_test_result_id
        )


class GetExceptionResultsResponse(BaseModel):
    results: list[ExceptionResult]


class GetExceptionResultDetailsResponse(BaseModel):
    details: ExceptionResultDetails


class CreateExceptionResultsRequest(BaseModel):
    results: list[CreateExceptionResult]
    load_test_result_id: int = Field(alias="loadTestResultId")
