# ToBinary

## Overview
The `ToBinary` expression converts string values to binary format using a specified encoding format. It supports multiple encoding formats including hexadecimal, UTF-8, and Base64, with hexadecimal as the default format when no format is specified.

## Syntax
```sql
to_binary(expr [, format])
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | String | The input string expression to convert to binary |
| format | String (optional) | The encoding format: 'hex', 'utf-8', 'utf8', or 'base64'. Defaults to 'hex' |

## Return Type
Binary (BinaryType)

## Supported Data Types

- Input: StringTypeWithCollation (supports trim collation)
- Format parameter: StringType or NullType (must be foldable/constant)

## Algorithm

- Evaluates the format parameter at compile time and converts to lowercase
- Maps format strings to internal Spark expressions:
  - 'hex' → Unhex expression with failOnError=true
  - 'utf-8' or 'utf8' → Encode expression with UTF-8 encoding
  - 'base64' → UnBase64 expression with failOnError=true
- Returns null literal for invalid formats or null format parameter
- Performs format validation during type checking phase

## Partitioning Behavior
This expression preserves partitioning as it operates row-by-row without requiring data shuffling between partitions.

## Edge Cases

- Null input expression returns null
- Null format parameter results in null output
- Invalid format strings return null (when nullOnInvalidFormat=false)
- Format parameter must be a constant/foldable expression, not a column reference
- Format matching is case-insensitive
- Invalid hex, UTF-8, or Base64 input will cause runtime failures due to failOnError=true

## Code Generation
As a RuntimeReplaceable expression, ToBinary is replaced by other expressions (Unhex, Encode, UnBase64) during query planning, inheriting their code generation capabilities.

## Examples
```sql
-- Convert hex string to binary (default format)
SELECT to_binary('48656C6C6F');

-- Convert hex string to binary (explicit format)
SELECT to_binary('48656C6C6F', 'hex');

-- Convert UTF-8 string to binary
SELECT to_binary('Hello', 'utf-8');

-- Convert Base64 string to binary
SELECT to_binary('SGVsbG8=', 'base64');
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Default hex format
df.select(expr("to_binary(hex_column)"))

// With explicit format
df.select(expr("to_binary(string_column, 'utf-8')"))
```

## See Also

- Unhex - Convert hexadecimal strings to binary
- Encode - Encode strings using specified character sets
- UnBase64 - Decode Base64 strings to binary
- Hex - Convert binary to hexadecimal string representation