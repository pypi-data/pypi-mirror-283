"""Transformer manager."""

from popsink_transformer.avro_to_json.main import AvroToJson
from popsink_transformer.avro_to_sql.main import AvroToSQL, SqlEngine


class Transformer:
    """Transformer class."""

    def __init__(
        self,
        from_source: dict = None,
        sql_engine: SqlEngine = None,
    ) -> None:
        self.avro_to_json = AvroToJson(from_source=from_source)
        self.avro_to_sql = AvroToSQL(
            from_source=from_source,
            sql_engine=sql_engine,
        )
