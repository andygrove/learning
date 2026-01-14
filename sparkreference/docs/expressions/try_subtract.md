# TrySubtract

## Overview
`TrySubtract` is a safe subtraction expression that performs subtraction operations without throwing exceptions on overflow or other arithmetic errors. It returns NULL instead of failing when arithmetic operations would normally cause runtime exceptions. This expression is implemented as a `RuntimeReplaceable` that delegates to either the native `Subtract` expression with TRY evaluation mode for numeric types, or wraps the ANSI `Subtract` expression in a `TryEval` for other data types.

## Syntax
```sql
try_subtract(left_expr, right_expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("try_subtract(col1, col2)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The minuend (value to subtract from) |
| right | Expression | The subtrahend (value to subtract) |
| replacement | Expression | Internal replacement expression used for evaluation |

## Return Type
The return type depends on the input data types:
- For numeric types: follows standard Spark type promotion rules for subtraction
- For interval types: appropriate interval type
- For date/timestamp arithmetic: appropriate temporal type
- Returns NULL when operations would cause exceptions

## Supported Data Types
- **Numeric types**: All numeric types (IntegerType, LongType, FloatType, DoubleType, DecimalType, etc.)
- **Interval types**: YearMonthIntervalType, DayTimeIntervalType
- **Temporal types**: DateType, TimestampType (when combined with intervals)
- **Mixed arithmetic**: Date/timestamp with intervals

## Algorithm
- For numeric types, uses `Subtract` expression with `EvalMode.TRY` for native safe arithmetic
- For non-numeric types, wraps standard `Subtract` with `EvalMode.ANSI` in a `TryEval` container
- `TryEval` catches any runtime exceptions and converts them to NULL results
- Inherits analysis rules from the underlying `Subtract` expression
- Performs standard type checking and promotion during analysis phase

## Partitioning Behavior
- **Preserves partitioning**: Yes, this is a row-level transformation that doesn't change data distribution
- **Requires shuffle**: No, operates independently on each row
- **Partition pruning**: Not applicable, this is not a predicate expression
- **Bucketing**: Preserves existing bucketing as it doesn't affect partition keys

## Edge Cases
- **Null handling**: Returns NULL if either operand is NULL (standard SQL null propagation)
- **Overflow behavior**: Returns NULL instead of throwing arithmetic overflow exceptions
- **Underflow behavior**: Returns NULL for underflow conditions that would cause exceptions
- **Type mismatch**: Analysis-time error for incompatible types (e.g., string - boolean)
- **Division by zero**: Not applicable for subtraction operations
- **Interval edge cases**: Handles interval arithmetic edge cases by returning NULL on invalid operations

## Code Generation
This expression supports Catalyst code generation through its replacement mechanism:
- **Numeric types**: Delegates to `Subtract` with TRY mode, which supports full code generation
- **Non-numeric types**: Uses `TryEval` wrapper, which may fall back to interpreted evaluation for exception handling
- **Tungsten integration**: Full integration when underlying `Subtract` supports code generation

## Examples
```sql
-- Basic numeric subtraction
SELECT try_subtract(10, 3);
-- Result: 7

-- Overflow handling
SELECT try_subtract(-9223372036854775808, 1);
-- Result: NULL (instead of overflow exception)

-- Interval arithmetic
SELECT try_subtract(interval 2 year, interval 1 year);
-- Result: 1-0

-- Null handling
SELECT try_subtract(NULL, 5);
-- Result: NULL

-- Date arithmetic
SELECT try_subtract(date '2023-01-15', interval 10 days);
-- Result: 2023-01-05
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic usage
df.select(expr("try_subtract(revenue, costs)").as("profit"))

// With column references
df.select(expr("try_subtract(end_date, start_date)").as("duration"))

// Handling potential overflows safely
df.select(expr("try_subtract(max_long_value, negative_value)").as("safe_result"))
```

## See Also
- `Subtract` - Standard subtraction expression with ANSI/LEGACY modes
- `TryAdd` - Safe addition expression
- `TryMultiply` - Safe multiplication expression
- `TryDivide` - Safe division expression
- `TryEval` - Generic try-catch wrapper for expressions