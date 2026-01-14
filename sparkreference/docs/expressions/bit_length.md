# BitLength

## Overview
The `BitLength` expression returns the length of a string or binary value in bits. It multiplies the byte length by 8 to convert from bytes to bits, supporting both string and binary data types with collation-aware string handling.

## Syntax
```sql
BIT_LENGTH(expr)
```

```scala
// DataFrame API
col("column_name").expr("bit_length(column_name)")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | String or Binary | The input string or binary value to measure |

## Return Type
`IntegerType` - Returns an integer representing the bit length of the input.

## Supported Data Types

- `StringType` with collation support (including trim collation)
- `BinaryType`

## Algorithm

- For string inputs, calculates `UTF8String.numBytes * 8` to get the bit length
- For binary inputs, calculates `Array[Byte].length * 8` to get the bit length  
- Leverages implicit casting to convert compatible input types to supported types
- Uses null-safe evaluation to handle null inputs appropriately
- Supports both interpreted and code-generated execution paths

## Partitioning Behavior
This expression preserves partitioning as it is a deterministic transformation that operates on individual rows without requiring data movement or shuffle operations.

## Edge Cases

- **Null handling**: Returns null when input is null (null-intolerant behavior)
- **Empty input**: Returns 0 for empty strings or empty binary arrays
- **Multi-byte characters**: Correctly handles UTF-8 encoded strings by counting actual bytes, not characters
- **Large inputs**: May overflow if the input size exceeds integer limits when multiplied by 8

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, generating optimized bytecode for both string and binary input types rather than falling back to interpreted mode.

## Examples
```sql
-- String input
SELECT BIT_LENGTH('Spark SQL');
-- Returns: 72 (9 bytes * 8 bits)

-- Binary input  
SELECT BIT_LENGTH(x'537061726b2053514c');
-- Returns: 72

-- Null input
SELECT BIT_LENGTH(NULL);
-- Returns: NULL

-- Empty string
SELECT BIT_LENGTH('');
-- Returns: 0
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("bit_length(text_column)").as("bit_length"))

// With binary column
df.select(expr("bit_length(binary_column)").as("binary_bit_length"))
```

## See Also

- `LENGTH` - Returns character length of strings
- `OCTET_LENGTH` - Returns byte length (equivalent to bit_length/8)
- String manipulation functions for related text processing operations