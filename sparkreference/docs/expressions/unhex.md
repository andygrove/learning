# Unhex

## Overview
The `Unhex` expression converts a hexadecimal string representation back to its original binary data. It performs the inverse operation of the `hex()` function by decoding hexadecimal-encoded strings into byte arrays.

## Syntax
```sql
unhex(hex_string)
```

```scala
// DataFrame API
col("hex_column").unhex()
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The hexadecimal string expression to be converted to binary data |
| failOnError | Boolean | Internal parameter controlling error handling behavior (default: false) |

## Return Type
`BinaryType` - Returns a byte array containing the decoded binary data.

## Supported Data Types

- `StringType` with collation support (requires trim-compatible collations)
- Input strings must contain valid hexadecimal characters (0-9, A-F, a-f)

## Algorithm

- Extracts bytes from the input UTF8String using `getBytes()`
- Delegates to `Hex.unhex()` method for actual hexadecimal decoding
- Converts pairs of hexadecimal characters back to their byte values
- Handles invalid hexadecimal input based on `failOnError` flag
- Returns null for invalid input when `failOnError` is false

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle as it operates on individual rows
- Maintains existing partition boundaries since it's a row-level transformation
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null Input**: Returns null when input is null (null intolerant behavior)
- **Invalid Hexadecimal**: Returns null by default, throws exception when `failOnError=true`
- **Odd-length Strings**: May cause `IllegalArgumentException` depending on underlying implementation
- **Empty String**: Likely returns empty byte array
- **Non-hexadecimal Characters**: Triggers error handling based on `failOnError` setting

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method:

- Uses `nullSafeCodeGen` for optimized null handling
- Generates direct method calls to avoid interpretation overhead
- Falls back to `nullSafeEval` call in generated code for complex logic

## Examples
```sql
-- Convert hexadecimal string to binary
SELECT unhex('537061726B2053514C');

-- Decode and convert back to string
SELECT decode(unhex('537061726B2053514C'), 'UTF-8');
-- Result: 'Spark SQL'

-- Handle invalid input (returns null)
SELECT unhex('invalid_hex_string');
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Convert hex column to binary
df.select(unhex(col("hex_column")))

// Chain with other operations
df.select(decode(unhex(col("hex_data")), "UTF-8").as("decoded_string"))
```

## See Also

- `hex()` - Converts binary data to hexadecimal string representation
- `decode()` - Converts binary data to string using specified character encoding
- `encode()` - Converts string to binary using specified character encoding