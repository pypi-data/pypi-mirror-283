# Transformer Library

This library provides a set of tools to transform Avro schemas into various formats such as JSON schema, SQL for Apache Flink, and PostgreSQL SQL. Additionally, it can transform data from these formats back into Avro schemas. Whether you're working with Avro schemas in your data pipeline or database schema, this library aims to simplify the conversion process for you.

## Features

- Convert Avro schema to JSON schema.
- Generate SQL statements for Apache Flink based on Avro schema.
- Generate PostgreSQL SQL statements based on Avro schema.
- Generate SQLSERVER SQL statements based on Avro schema.
- Generate CLICKHOUSE SQL statements based on Avro schema.
- Convert a single avro type to SQL type.

## Usage

Here's a quick guide on how to use the library:

### 1. Convert an Avro Schema to JSON schema

```python
from popsink_transformer.transformer import Transformer

transformer = Transformer(from_source=avro_schema)
json_schema = transformer.avro_to_json.convert()
print(json_schema)
```

### 2. Generate SQL for Apache Flink from an Avro schema

```python
from popsink_transformer.transformer import Transformer
from popsink_transformer.avro_to_sql.utils.type_converter import SqlEngine

transformer = Transformer(
    from_source=avro_schema,
    sql_engine=SqlEngine.FLINK,
)
flink_sql = transformer.avro_to_sql.convert()
print(flink_sql)
```

### 3. Generate PostgreSQL SQL from an Avro schema

```python
from popsink_transformer.transformer import Transformer
from popsink_transformer.avro_to_sql.utils.type_converter import SqlEngine

transformer = Transformer(
    from_source=avro_schema,
    sql_engine=SqlEngine.POSTGRES,
)
postgres_sql = transformer.avro_to_sql.convert()
print(postgres_sql)
```

### 4. Convert an Avro type to SQL type

```python
from popsink_transformer.avro_to_sql.utils.type_converter import (
    SqlEngine,
    convert_avro_type_to_sql_type,
)

postgres_sql_type = convert_avro_type_to_sql_type(
    avro_field_type="float",
    sql_engine=SqlEngine.POSTGRES
)
print(postgres_sql_type)
output: 'REAL'
```

### 5. Generate SQLSERVER SQL from an Avro schema

```python
from popsink_transformer.transformer import Transformer
from popsink_transformer.avro_to_sql.utils.type_converter import SqlEngine

transformer = Transformer(
    from_source=avro_schema,
    sql_engine=SqlEngine.SQLSERVER,
)
sqlserver_sql = transformer.avro_to_sql.convert()
print(sqlserver_sql)
```