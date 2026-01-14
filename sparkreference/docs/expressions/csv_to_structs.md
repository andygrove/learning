# CsvToStructs

## Overview
The `CsvToStructs` expression parses CSV-formatted strings and converts them into structured data (struct type). It provides a way to transform delimited string data into strongly-typed structured columns within Spark DataFrames, enabling schema enforcement and structured access to CSV data.

## Syntax
```sql
-- SQL syntax
from_csv(csvStr, schema[, options])
```

```scala
// DataFrame API usage
from_csv(col("csv_column"), schema, options)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| csvStr | StringType | The CSV-formatted string to parse |
| schema | StructType or String | The target schema defining the structure and data types |
| options | Map[String, String] | Optional CSV parsing options (delimiter, quote character, etc.) |

## Return Type
Returns a `StructType` matching the provided schema parameter. The struct contains fields corresponding to the parsed CSV columns with their respective data types as defined in the schema.

## Supported Data Types
- **Input**: StringType (CSV-formatted strings)
- **Output**: Any StructType with supported nested types including:
  - Primitive types: StringType, IntegerType, LongType, DoubleType, BooleanType, TimestampType, DateType
  - Complex types: ArrayType, MapType, nested StructType
  - All standard Spark SQL data types within the struct fields

## Algorithm
- Validates the input CSV string format and schema compatibility
- Applies CSV parsing options (delimiter, quote character, escape character, etc.)
- Tokenizes the CSV string according to RFC 4180 standards with customizable options
- Performs type casting for each field according to the target schema specification
- Handles malformed records based on parsing mode (PERMISSIVE, DROPMALFORMED, FAILFAST)

## Partitioning Behavior
- **Preserves partitioning**: Yes, this is a row-level transformation that maintains existing partition boundaries
- **Requires shuffle**: No, operates independently on each row without cross-partition dependencies
- Can be applied within partition-wise operations without affecting data distribution

## Edge Cases
- **Null handling**: Returns null struct if input CSV string is null; individual fields become null for empty/invalid values in PERMISSIVE mode
- **Empty input**: Empty strings result in struct with null fields depending on schema requirements
- **Malformed CSV**: Behavior depends on parsing mode - can return null, drop records, or fail with exception
- **Schema mismatch**: Extra CSV fields are ignored; missing fields become null in the resulting struct
- **Type conversion errors**: Invalid type conversions result in null values in PERMISSIVE mode

## Code Generation
Supports Whole-Stage Code Generation (Tungsten) for optimal performance. The expression generates efficient Java code for CSV parsing and struct creation, avoiding object creation overhead during execution when possible.

## Examples
```sql
-- Parse CSV string into struct with explicit schema
SELECT from_csv('1,John,25', 'id INT, name STRING, age INT') as person;

-- Using with custom options
SELECT from_csv('1|John|25', 'id INT, name STRING, age INT', map('delimiter', '|')) as person;

-- Example from source code comment
SELECT from_csv('26/08/2015', 'time Timestamp', map('timestampFormat', 'dd/MM/yyyy')) as parsed;
-- Result: {"time":2015-08-26 00:00:00}
```

```scala
// DataFrame API usage
import org.apache.spark.sql.types._

val schema = StructType(Seq(
  StructField("id", IntegerType),
  StructField("name", StringType),
  StructField("age", IntegerType)
))

df.select(from_csv($"csv_data", schema).as("parsed_data"))

// With custom options
val options = Map("delimiter" -> "|", "timestampFormat" -> "dd/MM/yyyy")
df.select(from_csv($"csv_data", schema, options).as("parsed_data"))
```

## See Also
- `StructsToCsv` - Converts struct data back to CSV format
- `JsonToStructs` - Similar functionality for JSON data parsing  
- `SchemaOfCsv` - Infers schema from CSV data samples
- CSV data source options for bulk CSV file processing