"""Type converter."""

from enum import Enum
from popsink_transformer.errors import PopsinkTransformerError


class SqlEngine(Enum):
    """SQL types supported."""

    POSTGRES = "postgres"
    FLINK = "flink"
    SQLSERVER = "sqlserver"
    CLICKHOUSE = "clickhouse"
    DB2I = "db2i"


def get_avro_to_sql_mapping(sql_engine: SqlEngine):
    """Get the appropriate Avro to SQL mapping based on the SQL type."""
    if sql_engine is SqlEngine.POSTGRES:
        return {
            "boolean": "BOOLEAN",
            "int": "INTEGER",
            "long": "BIGINT",
            "float": "REAL",
            "double": "DOUBLE PRECISION",
            "bytes": "BIT",
            "string": "STRING",
            "enum": "JSON",
            "fixed": "JSON",
            "uuid": "UUID",
            "date": "DATE",
        }

    if sql_engine is SqlEngine.FLINK:
        return {
            "boolean": "BOOLEAN",
            "int": "INTEGER",
            "long": "BIGINT",
            "float": "FLOAT",
            "double": "DOUBLE",
            "bytes": "BYTES",
            "string": "STRING",
            "enum": "STRING",
            "fixed": "DECIMAL",
            "date": "DATE",
            "uuid": "STRING",
        }

    if sql_engine is SqlEngine.SQLSERVER:
        return {
            "boolean": "BIT",
            "int": "INT",
            "long": "BIGINT",
            "float": "FLOAT",
            "double": "FLOAT",
            "bytes": "BYTES",
            "string": "TEXT",
            "enum": "TEXT",
            "fixed": "TEXT",
            "date": "DATE",
            "uuid": "TEXT",
        }

    if sql_engine is SqlEngine.CLICKHOUSE:
        return {
            "boolean": "BOOL",
            "int": "INT",
            "long": "BIGINT",
            "float": "FLOAT",
            "double": "DOUBLE",
            "bytes": "TEXT",
            "string": "TEXT",
            "enum": "ENUM",
            "fixed": "STRING",
            "date": "DATE",
            "uuid": "UUID",
        }

    if sql_engine is SqlEngine.DB2I:
        return {
            "boolean": "INT(1)",
            "int": "INT",
            "long": "BIGINT",
            "float": "FLOAT",
            "double": "DOUBLE",
            "bytes": "BINARY",
            "string": "VARCHAR(32672)",
            "enum": "VARCHAR(32672)",
            "fixed": "VARCHAR(32672)",
            "date": "DATE",
            "uuid": "VARCHAR(32672)",
        }

    raise PopsinkTransformerError("Incorrect SQL type has been specified.")


def convert_avro_type_to_sql_type(avro_field_type: str, sql_engine: SqlEngine) -> str:
    """Convert an Avro type to SQL type."""
    if not avro_field_type:
        raise PopsinkTransformerError("Avro field type cannot be empty")

    if not sql_engine:
        raise PopsinkTransformerError("SQL type cannot be empty")

    avro_to_sql_mapping = get_avro_to_sql_mapping(sql_engine=sql_engine)

    if avro_field_type not in avro_to_sql_mapping:
        raise PopsinkTransformerError(
            f"No matching SQL type found for Avro type: {avro_field_type}"
        )

    return avro_to_sql_mapping[avro_field_type]
