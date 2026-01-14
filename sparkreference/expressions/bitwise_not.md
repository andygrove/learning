# BitwiseNot

## Overview
The `BitwiseNot` expression performs a bitwise NOT operation (~) on integral values. It flips all bits in the binary representation of the input value, effectively computing the bitwise complement.

## Syntax
```sql
~expression
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(~col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression to apply bitwise NOT operation on |

## Return Type
Returns the same data type as the input expression. The output data type matches the child expression's data type exactly.

## Supported Data Types
- `ByteType`
- `ShortType` 
- `IntegerType`
- `LongType`

All integral types that extend `IntegralType` are supported. Non-integral types will cause a type validation error.

## Algorithm
- Validates that input is of integral type during analysis phase
- For each supported data type, applies the bitwise NOT operator (~) 
- Casts result back to original data type to handle byte/short overflow behavior
- Uses type-specific lambda functions cached lazily for efficient repeated evaluation
- Leverages null-intolerant evaluation (nulls propagate directly without computation)

## Partitioning Behavior
- **Preserves partitioning**: No, bitwise operations typically change hash codes and sort orders
- **Requires shuffle**: No, this is a per-row transformation that doesn't require data movement
- The expression operates independently on each row within partitions

## Edge Cases
- **Null handling**: Null-intolerant - if input is null, output is null without evaluation
- **Overflow behavior**: Results are cast back to original type, so byte/short values wrap around (e.g., `~(0.toByte)` becomes `-1.toByte`)
- **Type safety**: Only accepts integral types; other types cause compilation/analysis errors
- **Bit width**: Operation respects the bit width of the input type (8-bit for Byte, 16-bit for Short, etc.)

## Code Generation
This expression supports Tungsten code generation via the `doGenCode` method. It generates efficient Java code using `defineCodeGen` with the pattern `(CastType) ~(input)`, avoiding interpreted evaluation overhead in most cases.

## Examples
```sql
-- Basic bitwise NOT operations
SELECT ~0;        -- Returns -1
SELECT ~(-1);     -- Returns 0  
SELECT ~5;        -- Returns -6 (flips bits of 5)

-- With column references
SELECT ~status_code FROM events;

-- Nested with other expressions
SELECT ~(flags & 15) FROM configurations;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic usage
df.select(~col("flags"))

// Combined with other bitwise operations  
df.select(~(col("permissions") & lit(7)))

// With column alias
df.select((~col("mask")).alias("inverted_mask"))
```

## See Also
- `BitwiseAnd` - Bitwise AND operation between two expressions
- `BitwiseOr` - Bitwise OR operation between two expressions  
- `BitwiseXor` - Bitwise XOR operation between two expressions
- `ShiftLeft` / `ShiftRight` - Bit shifting operations