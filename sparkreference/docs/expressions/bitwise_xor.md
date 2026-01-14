# BitwiseXor

## Overview
BitwiseXor is a binary arithmetic expression that performs bitwise XOR operations between two integral expressions. It returns 1 for each bit position where the corresponding bits of either operand (but not both) are 1, and 0 where both bits are the same.

## Syntax
```sql
expression1 ^ expression2
```

```scala
// DataFrame API
col("column1").bitwiseXOR(col("column2"))
// or using expr()
expr("column1 ^ column2")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | Left operand for the bitwise XOR operation |
| right | Expression | Right operand for the bitwise XOR operation |

## Return Type
Returns the same integral data type as the input expressions (after type coercion if needed).

## Supported Data Types
- `ByteType`
- `ShortType` 
- `IntegerType`
- `LongType`

All inputs must be of `IntegralType` (whole numbers only).

## Algorithm
- Type-specific XOR functions are lazily initialized based on the expression's data type
- For each supported type, performs native Scala bitwise XOR operation (`^`)
- Results are cast back to the appropriate type (`.toByte`, `.toShort`) for smaller integral types
- Uses null-safe evaluation to handle null inputs
- Implements commutative property optimization during query planning

## Partitioning Behavior
- **Preserves partitioning**: Yes, when used in projections
- **Requires shuffle**: No, this is a row-level operation that doesn't require data movement
- Can be pushed down to individual partitions for parallel execution

## Edge Cases
- **Null handling**: If either operand is null, the result is null (null-safe evaluation)
- **Empty input**: Not applicable for binary operations
- **Overflow/underflow**: Not applicable - bitwise operations don't overflow within their type bounds
- **Type coercion**: Both operands must resolve to the same integral type after implicit casting

## Code Generation
This expression extends `BinaryArithmetic` which supports Tungsten code generation. The expression will generate optimized Java bytecode rather than falling back to interpreted evaluation mode for better performance.

## Examples
```sql
-- Basic bitwise XOR
SELECT 3 ^ 5;
-- Result: 6 (011 XOR 101 = 110)

-- Column operations  
SELECT col1 ^ col2 FROM table1;

-- With literals
SELECT id ^ 255 FROM users;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("value1").bitwiseXOR(col("value2")))

// Using expression strings
df.selectExpr("value1 ^ value2 as xor_result")

// With literals
df.select(col("flags") ^ lit(128))
```

## See Also
- `BitwiseAnd` - Bitwise AND operation
- `BitwiseOr` - Bitwise OR operation  
- `BitwiseNot` - Bitwise NOT operation
- `ShiftLeft` / `ShiftRight` - Bit shifting operations