# DecimalAddNoOverflowCheck

## Overview
`DecimalAddNoOverflowCheck` is a binary arithmetic expression that performs addition of two decimal values without checking for overflow conditions. This expression is specifically designed for use in aggregation operations like Sum and Avg where overflow checking is handled at the UnsafeRowWriter level.

## Syntax
This expression is used internally by Spark's aggregation framework and is not directly accessible through SQL syntax. It is generated during the optimization phase for decimal addition in aggregation contexts.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | Left operand expression that evaluates to a decimal value |
| right | Expression | Right operand expression that evaluates to a decimal value |
| dataType | DataType | The result decimal data type (must be DecimalType) |

## Return Type
Returns a `DecimalType` with precision and scale determined by the provided `dataType` parameter.

## Supported Data Types

- Input types: `DecimalType` only
- Both left and right expressions must evaluate to decimal values
- Output type: `DecimalType`

## Algorithm

- Evaluates both left and right child expressions to obtain decimal values
- Uses the `TypeUtils.getNumeric()` method to get the appropriate numeric handler for the result data type
- Performs addition using the numeric handler's `plus()` method without overflow validation
- For code generation, uses the decimal's `$plus` method directly
- Null safety is handled at the BinaryOperator level

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning as it operates on individual row values
- Does not require shuffle operations
- Can be evaluated locally within each partition

## Edge Cases

- **Null handling**: If either operand is null, the result is null (inherited from BinaryOperator)
- **Overflow behavior**: No overflow checking is performed, which may result in incorrect results for values that exceed the target decimal precision
- **Precision handling**: Relies on the provided dataType parameter to determine result precision and scale
- **Type validation**: Requires that the dataType parameter is an instance of DecimalType

## Code Generation
This expression supports Spark's Tungsten code generation through the `doGenCode` method, which generates optimized Java code using the decimal's native `$plus` method for better performance.

## Examples
```sql
-- This expression is not directly accessible in SQL
-- It's used internally during aggregation optimization
SELECT SUM(decimal_column) FROM table_name;
```

```scala
// Not directly constructible via DataFrame API
// Used internally by Spark's Catalyst optimizer
// Example of where it might be generated:
df.agg(sum($"decimal_column")).collect()
```

## See Also

- `Add` - Standard addition expression with overflow checking
- `Sum` - Aggregation function that may use this expression internally
- `Average` - Aggregation function that may use this expression internally
- `BinaryOperator` - Parent class providing common binary operation functionality