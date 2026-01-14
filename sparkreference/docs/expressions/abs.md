# Abs

## Overview
The `Abs` expression computes the absolute value of a numeric expression or ANSI interval. It returns the magnitude of the input value without regard to its sign, effectively removing any negative sign from the input.

## Syntax
```sql
ABS(expr)
```

```scala
// DataFrame API
col("column_name").abs
abs(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression to compute the absolute value of |
| failOnError | Boolean | Whether to fail on arithmetic overflow (defaults to ANSI mode setting) |

## Return Type
Returns the same data type as the input expression. The output type exactly matches the input type for all supported numeric types and interval types.

## Supported Data Types

- All numeric types: `ByteType`, `ShortType`, `IntegerType`, `LongType`, `FloatType`, `DoubleType`
- `DecimalType` with any precision and scale
- `DayTimeIntervalType` (using `LongExactNumeric`)
- `YearMonthIntervalType` (using `IntegerExactNumeric`)

## Algorithm

- For decimal types: Uses the native `abs()` method of the decimal representation
- For integer types in ANSI mode: Uses `MathUtils.negateExact()` to handle overflow detection when negating negative values
- For ANSI interval types: Uses `MathUtils.negateExact()` with overflow protection
- For other numeric types: Uses `java.lang.Math.abs()` with appropriate type casting
- Leverages type-specific `Numeric` instances for evaluation in interpreted mode

## Partitioning Behavior
This expression preserves partitioning as it is a deterministic unary transformation:

- Does not require shuffle operations
- Maintains the same partitioning scheme as the input
- Can be pushed down to individual partitions independently

## Edge Cases

- **Null handling**: Returns `null` for `null` input (null intolerant behavior)
- **Overflow behavior**: In ANSI mode (`failOnError = true`), throws an exception on integer overflow (e.g., `abs(Long.MinValue)`)
- **Non-ANSI mode**: May silently overflow for integer edge cases like `Long.MinValue`
- **Decimal precision**: Maintains the same precision and scale as input, no precision loss
- **Floating point**: Handles `NaN`, positive/negative infinity according to `java.lang.Math.abs()` semantics

## Code Generation
This expression supports Tungsten code generation with optimized paths:

- Uses native decimal `abs()` method for decimal types
- Generates overflow-safe code using `MathUtils.negateExact()` for ANSI integer and interval types
- Falls back to `java.lang.Math.abs()` for standard numeric types
- Includes proper type casting in generated code

## Examples
```sql
-- Numeric examples
SELECT ABS(-42);           -- Returns: 42
SELECT ABS(3.14);          -- Returns: 3.14
SELECT ABS(-3.14);         -- Returns: 3.14

-- Interval examples
SELECT ABS(INTERVAL -'1-1' YEAR TO MONTH);  -- Returns: 1-1
SELECT ABS(INTERVAL -'2 3:4:5' DAY TO SECOND); -- Returns: 2 03:04:05

-- Null handling
SELECT ABS(NULL);          -- Returns: NULL
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

df.select(abs(col("amount")))
df.select(col("value").abs)
df.withColumn("abs_difference", abs(col("value1") - col("value2")))
```

## See Also

- `Sign` - Returns the sign of a numeric expression
- `Negative` - Returns the negation of a numeric expression
- Mathematical functions: `Floor`, `Ceil`, `Round`