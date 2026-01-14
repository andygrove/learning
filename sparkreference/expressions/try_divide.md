# TryDivide

## Overview
`TryDivide` is a Spark Catalyst expression that performs division with error handling, returning `NULL` instead of throwing exceptions when encountering division errors (such as divide by zero). It acts as a runtime replaceable expression that delegates to optimized division implementations based on the input data types.

## Syntax
```sql
try_divide(dividend, divisor)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("try_divide(col1, col2)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left (dividend) | Expression | The numerator expression to be divided |
| right (divisor) | Expression | The denominator expression to divide by |
| replacement | Expression | Internal replacement expression used for actual evaluation |

## Return Type
Returns the same numeric type as the result of the division operation between the input types, or `NULL` when division errors occur.

## Supported Data Types
- **Numeric Types**: All Spark numeric types (ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType, DecimalType)
- **DateTime Types**: Supported through fallback mechanism with TryEval wrapper
- Mixed numeric type combinations follow standard Spark type promotion rules

## Algorithm
- For numeric type inputs: Delegates to `Divide(left, right, EvalMode.TRY)` for optimized execution
- For non-numeric types: Uses `TryEval(Divide(left, right, EvalMode.ANSI))` as fallback
- TRY evaluation mode captures division exceptions and returns `NULL` instead of failing
- Inherits analysis rules from the underlying division expression
- Acts as a runtime replaceable expression, substituting itself with the appropriate implementation during query planning

## Partitioning Behavior
- **Preserves Partitioning**: Yes, as it operates row-by-row without requiring data redistribution
- **Requires Shuffle**: No, the expression is evaluated locally on each partition
- Does not affect the partitioning scheme of the input data

## Edge Cases
- **Null Handling**: Returns `NULL` when either dividend or divisor is `NULL`
- **Division by Zero**: Returns `NULL` instead of throwing `ArithmeticException`
- **Overflow/Underflow**: For numeric types, overflow conditions return `NULL` in TRY mode
- **Type Compatibility**: Non-numeric datetime operations fall back to TryEval wrapper for error handling
- **Decimal Precision**: Follows Spark's decimal arithmetic rules with appropriate precision and scale

## Code Generation
- **Numeric Types**: Supports Tungsten code generation through the optimized `Divide` expression with `EvalMode.TRY`
- **Non-Numeric Types**: Falls back to interpreted mode via `TryEval` wrapper
- Code generation eligibility depends on the underlying replacement expression's capabilities

## Examples
```sql
-- Basic division with error handling
SELECT try_divide(10, 2) as result;  -- Returns 5.0
SELECT try_divide(10, 0) as result;  -- Returns NULL

-- Handling NULL inputs
SELECT try_divide(NULL, 5) as result;  -- Returns NULL
SELECT try_divide(10, NULL) as result; -- Returns NULL

-- Mixed numeric types
SELECT try_divide(100, 3.0) as result; -- Returns 33.333...
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("try_divide(revenue, quantity)").alias("unit_price"))

// Handling potential division by zero in aggregations
df.groupBy("category")
  .agg(expr("try_divide(sum(sales), sum(units))").alias("avg_unit_price"))
```

## See Also
- `Divide` - Standard division expression that throws exceptions on errors
- `TryEval` - Generic wrapper for converting exceptions to NULL values
- `SafeDivide` - Alternative safe division implementations
- **Math Functions**: Other mathematical expressions with TRY evaluation modes