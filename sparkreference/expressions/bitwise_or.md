# BitwiseOr

## Overview

The `BitwiseOr` expression performs a bitwise OR operation between two integral expressions. It applies the bitwise OR operator (`|`) to each corresponding bit of the two operands, returning 1 if either bit is 1, and 0 only when both bits are 0. This expression has been available since Spark 1.4.0 and is classified as a commutative bitwise function.

## Syntax

```sql
expr1 | expr2
```

```scala
// DataFrame API
col("column1").bitwiseOR(col("column2"))
// or using expr
expr("column1 | column2")
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | Left operand for the bitwise OR operation (must be integral type) |
| right | Expression | Right operand for the bitwise OR operation (must be integral type) |

## Return Type

Returns the same integral data type as the input operands. The return type matches the promoted type of the two input expressions following Spark's type promotion rules.

## Supported Data Types

- `ByteType`
- `ShortType` 
- `IntegerType`
- `LongType`

All input expressions must be of `IntegralType`. Non-integral types are not supported.

## Algorithm

- Validates that both input expressions are of integral data types
- Performs type-specific bitwise OR operation based on the resolved data type
- For ByteType and ShortType, results are explicitly cast back to the original type after the OR operation
- Uses lazy evaluation with type-specific lambda functions for optimal performance
- Leverages null-safe evaluation to handle null inputs appropriately

## Partitioning Behavior

- **Preserves partitioning**: Yes, this expression does not affect data distribution
- **Requires shuffle**: No, the operation is performed row-by-row locally
- **Partition elimination**: Not applicable, as this is a row-level computation expression

## Edge Cases

- **Null handling**: If either operand is null, the result is null (null-safe evaluation)
- **Type promotion**: Both operands must be promotable to the same integral type
- **Overflow behavior**: Uses LEGACY evaluation mode, following standard JVM bitwise operation semantics
- **Commutative property**: `a | b` produces the same result as `b | a` due to the commutative nature of bitwise OR

## Code Generation

This expression supports Catalyst code generation (Tungsten). The `nullSafeEval` method and type-specific lambda functions are optimized for code generation, avoiding interpreted evaluation overhead in the critical path.

## Examples

```sql
-- Basic bitwise OR
SELECT 3 | 5;  -- Returns 7

-- Column-based operations
SELECT col1 | col2 FROM table_name;

-- With different integral types
SELECT CAST(12 AS BIGINT) | CAST(10 AS BIGINT);  -- Returns 14

-- Null handling
SELECT NULL | 5;  -- Returns NULL
SELECT 3 | NULL;  -- Returns NULL
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Basic usage
df.select(col("column1").bitwiseOR(col("column2")))

// Using expr function
df.select(expr("column1 | column2"))

// With literal values
df.select(col("flags").bitwiseOR(lit(4)))
```

## See Also

- `BitwiseAnd` - Bitwise AND operation
- `BitwiseXor` - Bitwise XOR operation  
- `BitwiseNot` - Bitwise NOT operation
- `ShiftLeft` - Left bit shift operation
- `ShiftRight` - Right bit shift operation