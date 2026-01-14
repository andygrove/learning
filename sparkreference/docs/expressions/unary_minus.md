# UnaryMinus

## Overview
The `UnaryMinus` expression represents the unary minus operator that negates numeric values and intervals in Spark SQL. It supports both overflow-safe ANSI mode and standard negation behavior, handling various numeric types including decimals and calendar intervals.

## Syntax
```sql
-expression
NEGATIVE(expression)
```

```scala
// DataFrame API
col("column").unary_-
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The expression to negate |
| failOnError | Boolean | Whether to fail on arithmetic overflow (defaults to ANSI mode setting) |

## Return Type
Returns the same data type as the input expression. The negated value maintains the original precision and scale for decimal types.

## Supported Data Types

- Numeric types: ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType
- DecimalType (arbitrary precision)
- CalendarIntervalType
- DayTimeIntervalType
- YearMonthIntervalType

## Algorithm

- For decimal types, uses the built-in `unary_$minus()` method
- For integer types in ANSI mode, applies overflow checking via `MathUtils.negateExact()`
- For standard numeric types, performs basic negation with careful code generation to avoid compilation issues
- For calendar intervals, uses `IntervalUtils.negate()` or `IntervalUtils.negateExact()` based on error handling mode
- For ANSI interval types, applies `IntervalMathUtils.negateExact()` for overflow protection

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require shuffle operations
- Maintains existing partitioning schemes
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null for null input (null intolerant behavior)
- **Integer overflow**: In ANSI mode, throws exception on overflow (e.g., negating Long.MIN_VALUE)
- **Decimal precision**: Maintains original precision and scale without loss
- **Interval overflow**: Calendar and ANSI intervals check for overflow when `failOnError` is enabled
- **Code generation edge case**: Uses temporary variables to avoid compiler issues with direct negation of literals

## Code Generation
Supports full code generation (Tungsten) with optimized paths:

- Uses `nullSafeCodeGen` for most numeric types
- Special handling for decimal types via `defineCodeGen`
- Generates overflow-safe code when ANSI mode is enabled
- Falls back to interpreted evaluation only for unsupported data types

## Examples
```sql
-- Basic negation
SELECT -42;
-- Result: -42

-- With column reference
SELECT -price FROM products;

-- Using function alias
SELECT NEGATIVE(quantity) FROM inventory;

-- With intervals
SELECT -INTERVAL '2' DAY;
-- Result: -2 days
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(-col("amount"))
df.select(col("value").unary_-)

// With expressions
df.select(expr("-price"))
```

## See Also

- `Add` - Addition operator
- `Subtract` - Subtraction operator  
- `Abs` - Absolute value function
- `UnaryPositive` - Unary plus operator