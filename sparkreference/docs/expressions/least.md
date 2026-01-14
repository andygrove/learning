# Least

## Overview

The `Least` expression returns the smallest value among all its input expressions. It compares multiple expressions of the same data type and returns the minimum value according to the natural ordering of that type. This is a commutative expression that can accept any number of arguments greater than one.

## Syntax

```sql
LEAST(expr1, expr2, ...)
```

```scala
// DataFrame API
least(col("col1"), col("col2"), col("col3"))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | Two or more expressions to compare. All expressions must have compatible data types that can be coerced to the same type. |

## Return Type

Returns the same data type as the merged common type of all input expressions after type coercion.

## Supported Data Types

All data types that support ordering comparison:

- Numeric types (IntegerType, LongType, FloatType, DoubleType, DecimalType)
- String types (StringType)
- Date and time types (DateType, TimestampType)
- Binary types (BinaryType)
- Any other types that have a defined ordering through TypeUtils.getInterpretedOrdering

## Algorithm

- Validates that at least 2 arguments are provided, otherwise throws compilation error

- Performs type coercion to ensure all expressions have the same data type

- Uses fold-left operation starting with null as the accumulator

- For each child expression, evaluates the value and compares with current minimum

- Uses the data type's natural ordering to determine which value is smaller

## Partitioning Behavior

This expression does not affect partitioning behavior:

- Preserves existing partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be evaluated independently on each partition

## Edge Cases

- **Null handling**: If all expressions evaluate to null, returns null. Non-null values are always considered "smaller" than null values in the comparison.

- **Empty input**: Compilation error is thrown if fewer than 2 expressions are provided.

- **Type mismatch**: Returns DataTypeMismatch error if input expressions cannot be coerced to compatible types.

- **Non-orderable types**: Returns type check error for data types that don't support ordering (e.g., MapType, StructType).

## Code Generation

This expression supports full code generation (Tungsten). It generates optimized Java code using:

- `ctx.reassignIfSmaller()` for efficient comparison logic
- Expression splitting for handling large numbers of arguments
- Mutable state management for null tracking
- Avoids boxing/unboxing overhead in generated code

## Examples

```sql
-- Basic numeric comparison
SELECT LEAST(10, 9, 2, 4, 3);
-- Returns: 2

-- String comparison
SELECT LEAST('apple', 'banana', 'cherry');
-- Returns: 'apple'

-- With null values
SELECT LEAST(5, NULL, 3, 7);
-- Returns: 3

-- Date comparison
SELECT LEAST('2023-01-15', '2023-01-10', '2023-01-20');
-- Returns: '2023-01-10'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.least

df.select(least(col("price1"), col("price2"), col("price3")))

// With literal values
df.select(least(lit(100), col("value"), lit(50)))
```

## See Also

- `Greatest` - Returns the largest value among expressions
- `Min` - Aggregate function to find minimum in a group
- `Coalesce` - Returns first non-null value
- `When/Case` - Conditional expressions for complex comparisons