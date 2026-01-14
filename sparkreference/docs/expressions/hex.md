# Hex

## Overview
The `Hex` expression converts input values to their hexadecimal string representation. It accepts long integers, binary data, and strings, converting them to lowercase hexadecimal format. This is a deterministic, null-intolerant expression that preserves string collation types.

## Syntax
```sql
HEX(expr)
```

```scala
hex(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression to convert to hexadecimal format |

## Return Type
- For string input: Returns the same `StringType` with preserved collation
- For long and binary input: Returns `StringType` (default string producing behavior)

## Supported Data Types

- `LongType` - Long integers
- `BinaryType` - Binary data (byte arrays)
- `StringType` - String values (with trim collation support)

## Algorithm

- For `LongType`: Converts the long value directly to hexadecimal representation
- For `BinaryType`: Converts each byte in the array to its hexadecimal equivalent
- For `StringType`: First converts the string to UTF-8 bytes, then converts those bytes to hexadecimal
- Uses static `Hex.hex()` methods for the actual conversion logic
- Preserves the original string type and collation for string inputs

## Partitioning Behavior
- Preserves partitioning as it's a deterministic transformation
- Does not require shuffle operations
- Can be pushed down to individual partitions

## Edge Cases

- **Null handling**: Returns null for null inputs (null-intolerant behavior)
- **Empty strings**: Converts empty strings to empty hexadecimal representation
- **Binary data**: Handles empty byte arrays by producing empty hex strings
- **Long values**: Handles negative long values according to two's complement representation

## Code Generation
Supports Tungsten code generation through the `doGenCode` method. Uses `nullSafeCodeGen` to generate optimized bytecode that calls the static `Hex.hex()` methods directly, with special handling for string types that require byte conversion.

## Examples
```sql
-- Convert string to hex
SELECT HEX('Spark SQL');
-- Result: 537061726B2053514C

-- Convert number to hex
SELECT HEX(255);
-- Result: FF

-- Convert binary data to hex
SELECT HEX(CAST('hello' AS BINARY));
-- Result: 68656C6C6F
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(hex(col("text_column")))
df.select(hex(col("binary_column")))
df.select(hex(col("long_column")))
```

## See Also
- `Unhex` - Converts hexadecimal strings back to binary data
- `Base64` - Alternative encoding function for binary data
- `Conv` - General base conversion function