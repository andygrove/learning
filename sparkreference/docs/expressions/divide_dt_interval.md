# DivideDTInterval

## Overview
The `DivideDTInterval` expression divides a day-time interval by a numeric value, returning a new day-time interval. This operation performs division with `HALF_UP` rounding mode and includes comprehensive overflow and divide-by-zero checks to ensure safe arithmetic operations.

## Syntax
```sql
day_time_interval / numeric_value
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `interval` | `DayTimeIntervalType` | The day-time interval to be divided |
| `num` | `NumericType` | The numeric divisor (integral, decimal, or fractional types) |

## Return Type
`DayTimeIntervalType()` - Returns a day-time interval representing the result of the division operation.

## Supported Data Types
- **Left operand (interval)**: `DayTimeIntervalType` only
- **Right operand (num)**: All numeric types including:
  - `IntegralType` (Byte, Short, Int, Long)
  - `DecimalType` 
  - `FractionalType` (Float, Double)

## Algorithm
- Converts the day-time interval to microseconds (Long representation)
- Performs type-specific division based on the divisor's data type:
  - **Integral types**: Uses `LongMath.divide()` with `HALF_UP` rounding
  - **Decimal types**: Converts to Decimal, performs division, then rounds to Long with `HALF_UP`
  - **Fractional types**: Uses `DoubleMath.roundToLong()` with `HALF_UP` rounding
- Validates for divide-by-zero and overflow conditions before computation
- Returns the result as a day-time interval in microseconds

## Partitioning Behavior
- **Preserves partitioning**: No, this is a value-transforming operation
- **Requires shuffle**: No, operates on individual rows independently
- Can be applied within existing partitions without data movement

## Edge Cases
- **Null handling**: Expression is null-intolerant (`nullIntolerant = true`) - returns null if either operand is null
- **Divide by zero**: Throws `QueryExecutionErrors` when divisor is zero
- **Overflow behavior**: 
  - Checks for `Long.MinValue / -1` overflow condition
  - Throws `QueryExecutionErrors.overflowInIntegralDivideError` on overflow
  - Uses `longValueExact()` for decimal operations to detect overflow
- **Precision**: All division operations use `HALF_UP` rounding mode for consistent behavior

## Code Generation
This expression supports full Tungsten code generation with type-specific optimized paths:
- **Integral types**: Generates inline overflow checks and `LongMath.divide()` calls
- **Decimal types**: Generates Decimal arithmetic with precision handling
- **Fractional types**: Generates optimized double division with `DoubleMath.roundToLong()`
- Includes generated divide-by-zero validation for all numeric types

## Examples
```sql
-- Divide a day-time interval by an integer
SELECT INTERVAL '2 12:30:45.123' DAY TO SECOND / 2;
-- Result: INTERVAL '1 06:15:22.561500' DAY TO SECOND

-- Divide by decimal value
SELECT INTERVAL '5 00:00:00' DAY TO SECOND / 2.5;
-- Result: INTERVAL '2 00:00:00' DAY TO SECOND
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._

// Divide interval column by numeric literal
df.select(col("day_time_interval") / lit(3))

// Divide interval by another numeric column
df.select(col("day_time_interval") / col("divisor"))
```

## See Also
- `DivideYMInterval` - Division operation for year-month intervals
- `MultiplyDTInterval` - Multiplication of day-time intervals
- `IntervalDivide` - Base trait for interval division operations
- `BinaryExpression` - Parent class for binary operations