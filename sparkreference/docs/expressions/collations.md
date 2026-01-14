# Collations

## Overview
The `collations` function is a table-generating function (generator) that returns metadata information about all available collations in the Spark system. It provides detailed information about collation properties including sensitivity settings, locale information, and ICU version details.

## Syntax
```sql
SELECT * FROM collations()
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | - | This function takes no arguments |

## Return Type
Returns a table with the following schema:
- `CATALOG` (String, non-nullable): Catalog name
- `SCHEMA` (String, non-nullable): Schema name  
- `NAME` (String, non-nullable): Collation name
- `LANGUAGE` (String, nullable): Language code
- `COUNTRY` (String, nullable): Country code
- `ACCENT_SENSITIVITY` (String, non-nullable): Either "ACCENT_SENSITIVE" or "ACCENT_INSENSITIVE"
- `CASE_SENSITIVITY` (String, non-nullable): Either "CASE_SENSITIVE" or "CASE_INSENSITIVE"
- `PAD_ATTRIBUTE` (String, non-nullable): Padding attribute setting
- `ICU_VERSION` (String, nullable): ICU library version

## Supported Data Types
This is a parameterless generator function, so no input data types apply.

## Algorithm

- Calls `CollationFactory.listCollations()` to retrieve all available collation identifiers
- Loads metadata for each collation using `CollationFactory.loadCollationMeta()`
- Transforms boolean sensitivity flags into human-readable string values
- Constructs `InternalRow` objects containing collation metadata
- Returns an iterable collection of rows representing all collations

## Partitioning Behavior
As a leaf generator expression:

- Does not preserve input partitioning (no input data)
- Generates data independently on each partition
- Does not require shuffle operations
- Output is generated locally on each executor

## Edge Cases

- Returns empty result set if no collations are available in the system
- Null values are returned for optional fields (LANGUAGE, COUNTRY, ICU_VERSION) when not available
- All mandatory fields (CATALOG, SCHEMA, NAME, sensitivity flags, PAD_ATTRIBUTE) are always populated
- No input validation required since function is parameterless

## Code Generation
This expression extends `CodegenFallback`, meaning it does not support Tungsten code generation and always falls back to interpreted evaluation mode for each row generation.

## Examples
```sql
-- Get all available collations
SELECT * FROM collations();

-- Filter for UTF8_BINARY collation
SELECT * FROM collations() WHERE NAME = 'UTF8_BINARY';

-- Find accent-sensitive collations
SELECT NAME, LANGUAGE, COUNTRY 
FROM collations() 
WHERE ACCENT_SENSITIVITY = 'ACCENT_SENSITIVE';
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Generate collations table
val collationsDF = spark.sql("SELECT * FROM collations()")

// Filter and select specific collations
val utf8Collations = collationsDF
  .filter($"NAME".contains("UTF8"))
  .select($"NAME", $"CASE_SENSITIVITY", $"ACCENT_SENSITIVITY")
```

## See Also

- Table-valued functions
- Generator expressions
- Collation support in Spark SQL
- `CollationFactory` utility class