# BitwiseAnd

## Overview
BitwiseAnd performs a bitwise AND operation between two integral expressions. It compares each bit of the first operand to the corresponding bit of the second operand, returning 1 when both bits are 1, and 0 otherwise. This expression is commutative, meaning the order of operands does not affect the result.

## Syntax
```sql
expression1 & expression2
```

```scala
// DataFrame API
col("column1").bitwiseAND(col("column2"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | Left operand - must evaluate to an integral type |
| right | Expression | Right operand - must evaluate to an integral type |

## Return Type
Returns the same integral data type as the input operands. The specific return type depends on the input types and follows standard type coercion rules.

## Supported Data Types
- `ByteType`
- `ShortType` 
- `IntegerType`
- `LongType`

All inputs must be of `IntegralType`. Non-integral types are not supported.

## Algorithm
- Both operands are evaluated to their respective integral values
- A type-specific bitwise AND function is selected based on the resolved data type
- The AND operation is performed bit-by-bit: `result_bit = left_bit & right_bit`
- Results are cast back to the appropriate integral type (toByte, toShort for smaller types)
- The operation uses LEGACY evaluation mode for backward compatibility

## Partitioning Behavior
- **Preserves partitioning**: This expression does not affect data partitioning as it operates row-by-row
- **No shuffle required**: The operation is performed locally on each partition
- Can be used safely in partitioned operations without causing data movement

## Edge Cases
- **Null handling**: If either operand is null, the result is null (null-safe evaluation)
- **Type coercion**: Both operands must resolve to the same integral type
- **Overflow behavior**: Uses LEGACY evaluation mode, which may have different overflow semantics
- **Smaller types**: Results for ByteType and ShortType are explicitly cast back to prevent type widening

## Code Generation
This expression extends `BinaryArithmetic` which supports Catalyst code generation (Tungsten). The bitwise AND operation will be code-generated for optimal performance rather than using interpreted evaluation.

## Examples
```sql
-- Basic bitwise AND
SELECT 3 & 5;  -- Returns 1

-- With column references  
SELECT user_id & 7 FROM users;

-- Multiple operations
SELECT (flags & 15) & 3 FROM events;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("value1").bitwiseAND(col("value2")))

// With literals
df.select(col("flags").bitwiseAND(lit(7)))
```

## See Also
- `BitwiseOr` - Bitwise OR operation
- `BitwiseXor` - Bitwise XOR operation  
- `BitwiseNot` - Bitwise NOT operation
- Other `BinaryArithmetic` expressions for arithmetic operations