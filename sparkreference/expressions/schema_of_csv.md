# SchemaOfCsv

## Overview
The `SchemaOfCsv` expression analyzes a CSV string and returns its inferred schema as a struct type. It parses the provided CSV data to determine the data types and column structure, returning a schema representation that can be used for subsequent CSV processing operations.

## Syntax
```sql
SELECT schema_of_csv(csv_string [, options_map])
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(schema_of_csv($"csv_column"))
df.select(schema_of_csv($"csv_column", map("delimiter" -> ",")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `child` | `Expression` (String) | The CSV string to analyze for schema inference |
| `options` | `Map[String, String]` | Optional CSV parsing options (delimiter, quote character, etc.) |

## Return Type
Returns a `StructType` representing the inferred schema of the CSV data. The struct contains column names and their inferred data types based on the CSV content analysis.

## Supported Data Types
- **Input**: Only `StringType` is supported for the CSV input
- **Output**: Returns a struct type with inferred column types (INT, STRING, DOUBLE, etc.)

## Algorithm
- Evaluates the input CSV string at compile time (requires foldable expression)
- Uses `SchemaOfCsvEvaluator` to parse and analyze the CSV content
- Infers data types for each column based on the values in the CSV string
- Constructs a struct schema with appropriate column names and types
- Returns the schema as a literal struct type expression

## Partitioning Behavior
- **Preserves partitioning**: Yes, this is a deterministic expression that doesn't require data movement
- **Requires shuffle**: No, the expression operates on individual rows independently
- Can be used in partition pruning scenarios since it's foldable

## Edge Cases
- **Null handling**: Returns `DataTypeMismatch` error if input is null - nulls are not permitted
- **Empty input**: Requires non-empty, valid CSV string for schema inference
- **Non-foldable input**: Must be a constant/literal value - variables or column references cause compilation error
- **Invalid CSV format**: May return schema with default string types if parsing fails
- **Type inference**: Uses conservative type inference, defaulting to string for ambiguous values

## Code Generation
This expression uses the `RuntimeReplaceable` pattern and does not support direct code generation. Instead, it:
- Replaces itself with an `Invoke` expression at planning time
- Uses `SchemaOfCsvEvaluator` object for actual evaluation
- Falls back to interpreted mode through the invoke mechanism
- Evaluation happens at compile time since input must be foldable

## Examples
```sql
-- Basic schema inference
SELECT schema_of_csv('1,abc,2.5');
-- Returns: STRUCT<_c0: INT, _c1: STRING, _c2: DOUBLE>

-- With headers
SELECT schema_of_csv('id,name,score\n1,John,95.5');
-- Returns: STRUCT<id: INT, name: STRING, score: DOUBLE>

-- Using in CREATE TABLE
CREATE TABLE my_table 
USING DELTA
AS SELECT from_csv('1,John,95.5', schema_of_csv('1,John,95.5'));
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic schema inference
df.select(schema_of_csv(lit("1,abc,2.5")))

// With custom options
val options = Map("header" -> "true", "delimiter" -> ";")
df.select(schema_of_csv(lit("id;name\n1;John"), typedLit(options)))

// Use inferred schema for parsing
val csvData = "1,John,95.5"
val schema = schema_of_csv(lit(csvData))
df.select(from_csv($"csv_column", schema))
```

## See Also
- `from_csv()` - Parses CSV strings using a provided schema
- `to_csv()` - Converts struct columns to CSV strings
- `schema_of_json()` - Similar schema inference for JSON data