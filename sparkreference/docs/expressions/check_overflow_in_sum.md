# CheckOverflowInSum

## Overview
`CheckOverflowInSum` is a specialized variant of `CheckOverflow` designed specifically for sum aggregation operations. Unlike the standard `CheckOverflow`, this expression treats null input values as overflow conditions, making it essential for proper decimal precision handling in `Sum` aggregations where null propagation needs special treatment.

## Syntax
This is an internal Catalyst expression used within sum aggregations and is not directly accessible via SQL syntax. It's automatically applied during decimal sum operations.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The child expression to evaluate and check for overflow |
| dataType | DecimalType | Target decimal type with specific precision and scale |
| nullOnOverflow | Boolean | Whether to return null on overflow (true) or throw exception (false) |
| context | QueryContext | Query execution context for error reporting |

## Return Type
Returns `DecimalType` with the precision and scale specified in the `dataType` parameter. The expression is always nullable regardless of the child expression's nullability.

## Supported Data Types
Supports decimal input types only. The child expression must evaluate to a `Decimal` value that can be converted to the target precision and scale.

## Algorithm

- Evaluates the child expression first
- If child result is null, treats it as an overflow condition
- For null overflow: returns null if `nullOnOverflow` is true, otherwise throws `overflowInSumOfDecimalError`
- For non-null values: calls `Decimal.toPrecision()` with `ROUND_HALF_UP` rounding mode
- Returns the precision-adjusted decimal value or null if conversion overflows

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning as it's a unary transformation
- Does not require shuffle operations
- Operates independently on each partition

## Edge Cases

- **Null Input**: Treated as overflow condition, behavior depends on `nullOnOverflow` flag
- **Precision Overflow**: When target precision is insufficient, returns null or throws exception based on configuration
- **Scale Adjustment**: Uses `ROUND_HALF_UP` mode when adjusting scale during precision conversion
- **Error Context**: Provides detailed error information including suggestion to use `try_sum` function

## Code Generation
Supports full code generation (Tungsten). The generated code includes:

- Inline null checking and overflow handling
- Direct calls to `Decimal.toPrecision()` method
- Conditional error throwing based on `nullOnOverflow` flag
- Efficient boolean flag management for null tracking

## Examples
```sql
-- Not directly accessible in SQL
-- Automatically used in decimal sum operations:
SELECT SUM(decimal_column) FROM table;
```

```scala
// Internal usage in Catalyst expressions
// Not directly exposed in DataFrame API
// Automatically applied during sum aggregation planning
val result = df.agg(sum($"decimal_col"))
```

## See Also

- `CheckOverflow` - Standard overflow checking for decimal operations
- `Sum` - Aggregation function that utilizes this expression
- `DecimalType` - The decimal data type system
- `UnaryExpression` - Base class for single-child expressions