# MultiplyDTInterval

## Overview
The `MultiplyDTInterval` expression multiplies a day-time interval by a numeric value, scaling the duration proportionally. This is a binary expression that performs null-safe multiplication between interval and numeric types with proper overflow handling and rounding.

## Syntax
```sql
-- SQL syntax
day_time_interval * numeric_value

-- Function form
INTERVAL '1 2:3:4.567' DAY TO SECOND * 2.5
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `interval` | DayTimeIntervalType | The day-time interval to be multiplied (left operand) |
| `num` | NumericType | The numeric multiplier value (right operand) |

## Return Type
Returns `DayTimeIntervalType()` - a day-time interval representing the scaled duration.

## Supported Data Types
- **Left operand**: `DayTimeIntervalType` only
- **Right operand**: All numeric types including:
  - Integral types (Byte, Short, Int, Long)
  - Fractional types (Float, Double)
  - Decimal types with arbitrary precision

## Algorithm
- Intervals are internally stored as microsecond values (Long)
- For integral types: Uses `Math.multiplyExact()` to detect overflow
- For decimal types: Converts to Decimal, multiplies, then rounds using `HALF_UP` mode
- For fractional types: Uses `DoubleMath.roundToLong()` with `HALF_UP` rounding
- All operations preserve microsecond precision in the final result

## Partitioning Behavior
- **Preserves partitioning**: Yes, this is a row-level transformation
- **Requires shuffle**: No, operates independently on each row
- **Partition-wise operation**: Can be executed within each partition without data movement

## Edge Cases
- **Null handling**: Null-intolerant expression - returns null if either operand is null
- **Overflow behavior**: 
  - Integral multiplication throws `ArithmeticException` on overflow via `Math.multiplyExact()`
  - Decimal operations may throw `ArithmeticException` on scale conversion
  - Fractional operations may produce `Infinity` or lose precision
- **Rounding**: Non-integral results are rounded to nearest microsecond using `HALF_UP` mode
- **Zero multiplication**: Results in zero-duration interval
- **Negative multiplication**: Produces negative intervals (reverse direction)

## Code Generation
Supports full Tungsten code generation with type-specific optimizations:
- **Integral types**: Direct `java.lang.Math.multiplyExact()` call
- **Decimal types**: Inline Decimal arithmetic with precision handling  
- **Fractional types**: Optimized double arithmetic with `DoubleMath.roundToLong()`

## Examples
```sql
-- Basic interval multiplication
SELECT INTERVAL '2 10:30:45' DAY TO SECOND * 3;
-- Result: INTERVAL '7 07:32:15' DAY TO SECOND

-- Fractional multiplication with rounding
SELECT INTERVAL '1 12:00:00' DAY TO SECOND * 1.5;
-- Result: INTERVAL '2 06:00:00' DAY TO SECOND

-- Negative multiplication
SELECT INTERVAL '5 08:30:00' DAY TO SECOND * -0.5;
-- Result: INTERVAL '-2 -12:-15:00' DAY TO SECOND
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("day_interval") * lit(2.5))

// With explicit casting if needed
df.select(col("day_interval") * col("multiplier").cast("double"))
```

## See Also
- `MultiplyYMInterval` - Year-month interval multiplication
- `DivideYMInterval` - Year-month interval division  
- `DivideDTInterval` - Day-time interval division
- Interval arithmetic expressions in Apache Spark SQL