# OctetLength

## Overview
The `OctetLength` expression calculates the number of bytes in a string or binary value. It returns the byte length rather than the character length, making it useful for understanding storage requirements and handling multi-byte character encodings.

## Syntax
```sql
OCTET_LENGTH(expr)
```

```scala
octet_length(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | StringType with collation support or BinaryType | The input string or binary data to measure |

## Return Type
`IntegerType` - Returns an integer representing the number of bytes.

## Supported Data Types

- `StringType` with collation support (including trim collation)
- `BinaryType` for binary data arrays

## Algorithm

- For string inputs: Calls `UTF8String.numBytes()` to get the byte count of the UTF-8 encoded string
- For binary inputs: Returns the length of the byte array directly
- Implements null-safe evaluation, returning null if input is null
- Uses implicit type casting to convert compatible input types
- Supports both interpreted evaluation and code generation for performance

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle as it's a deterministic function
- Can be pushed down to individual partitions for parallel execution
- Maintains existing partitioning schemes when used in transformations

## Edge Cases

- **Null handling**: Returns `null` when input is `null` (null-intolerant behavior)
- **Empty strings**: Returns `0` for empty strings
- **Multi-byte characters**: Correctly counts bytes, not characters (e.g., Unicode characters may use 2-4 bytes)
- **Binary data**: Handles binary arrays of any size within integer limits
- **Large inputs**: May overflow if byte count exceeds `Integer.MAX_VALUE`

## Code Generation
This expression supports Tungsten code generation for optimal performance:

- For StringType: Generates `($c).numBytes()` code
- For BinaryType: Generates `($c).length` code
- Falls back to interpreted mode only if code generation context doesn't support it

## Examples
```sql
-- Basic string length in bytes
SELECT OCTET_LENGTH('Spark SQL');
-- Result: 9

-- Multi-byte character example
SELECT OCTET_LENGTH('你好');
-- Result: 6 (2 characters × 3 bytes each in UTF-8)

-- Binary data example  
SELECT OCTET_LENGTH(x'537061726b2053514c');
-- Result: 9

-- Null handling
SELECT OCTET_LENGTH(NULL);
-- Result: NULL
```

```scala
import org.apache.spark.sql.functions._

// DataFrame API usage
df.select(octet_length(col("text_column")))

// With column alias
df.select(octet_length(col("data")).alias("byte_length"))

// In filter conditions
df.filter(octet_length(col("message")) > 100)
```

## See Also

- `LENGTH` - Returns character length instead of byte length
- `BIT_LENGTH` - Returns length in bits (8 × octet length)
- `CHAR_LENGTH` - Alias for character-based length functions