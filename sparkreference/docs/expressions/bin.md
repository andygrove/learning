# Bin

## Overview
The `Bin` expression converts a long integer value to its binary string representation. It takes a numeric input and returns a UTF-8 string containing the binary representation of that number.

## Syntax
```sql
BIN(expr)
```

```scala
bin(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Long | The numeric expression to convert to binary representation |

## Return Type
`StringType` - Returns a UTF-8 encoded string containing the binary representation.

## Supported Data Types

- Long integers (LongType)
- Values that can be implicitly cast to LongType through `ImplicitCastInputTypes`

## Algorithm

- Accepts a long integer input value
- Converts the long value to its binary string representation using `UTF8String.toBinaryString()`
- Returns the binary representation as a UTF-8 string
- Implements null-safe evaluation to handle null inputs appropriately
- Uses code generation for optimized execution when possible

## Partitioning Behavior

- This expression preserves partitioning as it performs a deterministic transformation on individual rows
- Does not require shuffle operations
- Can be pushed down to individual partitions independently

## Edge Cases

- **Null handling**: Returns null when the input is null (null-intolerant behavior with `nullIntolerant = true`)
- **Negative numbers**: Handles negative long values according to two's complement binary representation
- **Zero input**: Returns "0" for zero input values
- **Type conversion**: Automatically casts compatible numeric types to LongType through implicit casting

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method. It generates optimized Java code that calls `UTF8String.toBinaryString()` directly, avoiding interpreted evaluation overhead.

## Examples
```sql
-- Convert decimal numbers to binary
SELECT BIN(12);
-- Returns: "1100"

SELECT BIN(0);
-- Returns: "0"

SELECT BIN(-1);
-- Returns binary representation of -1 in two's complement
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(bin(col("number_column")))

// With literal values
df.select(bin(lit(42)))
// Returns: "101010"
```

## See Also

- `Hex` - Converts numbers to hexadecimal representation
- `Conv` - Converts numbers between different bases
- `Oct` - Converts numbers to octal representation