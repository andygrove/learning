# BitwiseCount

## Overview
The `BitwiseCount` expression counts the number of set bits (1s) in the binary representation of an integer or boolean value. It is implemented as a unary expression that accepts integral types and boolean values, returning the population count (popcount) of the input.

## Syntax
```sql
bit_count(expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("bit_count(column_name)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Integral or Boolean | The expression whose bits should be counted |

## Return Type
`IntegerType` - Always returns an integer representing the count of set bits.

## Supported Data Types
- `BooleanType` - Counts 1 for true, 0 for false
- `ByteType` - 8-bit signed integers
- `ShortType` - 16-bit signed integers  
- `IntegerType` - 32-bit signed integers
- `LongType` - 64-bit signed integers

## Algorithm
- For `BooleanType`: Returns 1 if true, 0 if false
- For integral types: Uses `java.lang.Long.bitCount()` which implements population count
- The algorithm counts each bit position that contains a 1 in the binary representation
- Input values are cast to long for the bitCount operation regardless of original integral type
- Null inputs result in null outputs (null-intolerant behavior)

## Partitioning Behavior
- **Preserves partitioning**: Yes, this is a unary transformation that operates row-by-row
- **Requires shuffle**: No, computation is purely local to each partition
- **Partition-wise operation**: Each row is processed independently within its partition

## Edge Cases
- **Null handling**: Returns null for null inputs (nullIntolerant = true)
- **Boolean handling**: Special case where true → 1, false → 0
- **Negative numbers**: Uses two's complement representation, so negative numbers may have many set bits
- **Zero input**: Returns 0 (no bits set)
- **Maximum values**: For signed integers, the maximum possible bit count depends on the data type width

## Code Generation
This expression **supports code generation** (Tungsten). The `doGenCode` method provides optimized code paths:
- For `BooleanType`: Generates inline ternary operator `($c) ? 1 : 0`
- For integral types: Generates direct call to `java.lang.Long.bitCount($c)`
- Falls back to interpreted mode (`nullSafeEval`) only when code generation is disabled

## Examples
```sql
-- Count bits in integers
SELECT bit_count(0);     -- Returns: 0
SELECT bit_count(7);     -- Returns: 3 (binary: 111)
SELECT bit_count(8);     -- Returns: 1 (binary: 1000)
SELECT bit_count(-1);    -- Returns: 64 (all bits set in long representation)

-- Count bits in boolean
SELECT bit_count(true);  -- Returns: 1
SELECT bit_count(false); -- Returns: 0

-- With null values
SELECT bit_count(NULL);  -- Returns: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("bit_count(id)"))
  .show()

// Using with different data types
df.select(
  expr("bit_count(byte_col)"),
  expr("bit_count(short_col)"), 
  expr("bit_count(int_col)"),
  expr("bit_count(long_col)"),
  expr("bit_count(boolean_col)")
)
```

## See Also
- Bitwise AND (`&`), OR (`|`), XOR (`^`) expressions
- `shiftleft()`, `shiftright()` bitwise shift operations
- `bin()` function for binary string representation
- Other bitwise manipulation functions in the `bitwise_funcs` group