from utils.clients.postgres.types import ColumnExpressionType, QueryType


async def build_query(
        query: QueryType,
        limit: int | None = None,
        offset: int | None = None,
        distinct: ColumnExpressionType | None = None,
        order_by: ColumnExpressionType | None = None,
        clause_filter: ColumnExpressionType | None = None
) -> QueryType:
    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)

    if order_by:
        query = query.order_by(*order_by)

    if distinct:
        query = query.distinct(*distinct)

    if clause_filter:
        query = query.filter(*clause_filter)

    return query
