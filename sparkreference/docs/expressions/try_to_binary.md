# TryToBinary

## Overview
The `TryToBinary` expression attempts to convert input values to binary format, returning NULL instead of throwing an error when the conversion fails. This is a "try" variant of the `ToBinary` expression that provides safe conversion with graceful error handling.

## Syntax
```sql
try_to_binary(expr)
try_to_binary(expr, format)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("try_to_binary(column_name)"))
df.select(expr("try_to_binary(column_name, format_string)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Expression | The input expression to convert to binary format |
| format | Expression (Optional) | Format specification for the conversion |

## Return Type
Returns `BinaryType` - a binary data type containing the converted value, or NULL if conversion fails.

## Supported Data Types

- String types (StringType)
- Numeric types that can be converted to binary representation
- Any data type supported by the underlying `ToBinary` expression

## Algorithm

- Wraps the `ToBinary` expression with `TryEval` for safe evaluation
- Sets `nullOnInvalidFormat = true` to handle format-related errors gracefully
- Uses `RuntimeReplaceable` pattern to delegate actual conversion logic to `ToBinary`
- Returns NULL when any conversion error occurs instead of throwing exceptions
- Preserves the original expression and optional format for proper parameter handling

## Partitioning Behavior

- Preserves partitioning as it performs row-level transformations without requiring data movement
- Does not require shuffle operations
- Can be applied within existing partitions independently

## Edge Cases

- **Null handling**: Returns NULL when input expression is NULL
- **Invalid format**: Returns NULL when format string is invalid or incompatible
- **Conversion failures**: Returns NULL for any input that cannot be converted to binary
- **Empty input**: Behavior depends on underlying `ToBinary` implementation
- **Format mismatch**: Returns NULL when input doesn't match the specified format

## Code Generation
This expression uses the `RuntimeReplaceable` pattern, which means it delegates to the underlying `TryEval(ToBinary(...))` expression for code generation. The actual code generation support depends on the `TryEval` and `ToBinary` implementations.

## Examples
```sql
-- Basic conversion attempt
SELECT try_to_binary('48656c6c6f') as binary_value;

-- With format specification
SELECT try_to_binary('Hello', 'utf-8') as binary_value;

-- Handling invalid input gracefully
SELECT try_to_binary('invalid_hex') as result; -- Returns NULL instead of error
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic conversion
df.select(expr("try_to_binary(hex_string)"))

// With format
df.select(expr("try_to_binary(input_col, 'hex')"))

// Safe conversion in transformations
df.withColumn("binary_data", expr("try_to_binary(source_column)"))
```

## See Also

- `ToBinary` - The base binary conversion expression that throws errors on failure
- `TryEval` - The wrapper expression that provides safe evaluation semantics
- `TryToNumber` - Similar try-based conversion for numeric types
- `TryToTimestamp` - Similar try-based conversion for timestamp types