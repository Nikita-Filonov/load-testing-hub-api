from sqlalchemy import ColumnExpressionArgument, Select, Update, Delete, Insert

QueryType = Select | Update | Delete | Insert
ColumnExpressionType = tuple[ColumnExpressionArgument[bool], ...]
