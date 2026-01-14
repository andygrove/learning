# MultiplyYMInterval

## Overview
The `MultiplyYMInterval` expression multiplies a year-month interval by a numeric value, returning a new year-month interval. This expression supports various numeric data types and handles precision conversions appropriately for each type.

## Syntax
```sql
year_month_interval * numeric_value
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `interval` | YearMonthIntervalType | The year-month interval to be multiplied |
| `num` | NumericType | The numeric multiplier (byte, short, int, long, float, double, or decimal) |

## Return Type
`YearMonthIntervalType()` - Returns a year-month interval representing the multiplication result.

## Supported Data Types
- **Interval**: YearMonthIntervalType only
- **Numeric**: All numeric types including:
  - Integer types: ByteType, ShortType, IntegerType, LongType
  - Floating-point types: FloatType, DoubleType
  - DecimalType (arbitrary precision)

## Algorithm
- Internally represents year-month intervals as integer months
- Uses type-specific multiplication logic based on the numeric operand type
- For integer types: Uses `Math.multiplyExact()` for overflow detection
- For floating-point types: Uses `DoubleMath.roundToInt()` with HALF_UP rounding
- For decimal types: Performs decimal multiplication then rounds to integer months
- Applies exact conversion methods to prevent silent overflow/underflow

## Partitioning Behavior
- **Preserves partitioning**: Yes, this is a deterministic transformation that doesn't require data redistribution
- **Requires shuffle**: No, the operation is performed locally on each partition

## Edge Cases
- **Null handling**: Returns null if either operand is null (nullIntolerant = true)
- **Overflow behavior**: 
  - Integer multiplication uses `Math.multiplyExact()` throwing ArithmeticException on overflow
  - Long results converted using `Math.toIntExact()` throwing exception if out of int range
  - Decimal results use `intValueExact()` throwing exception if fractional part exists after rounding
- **Floating-point precision**: Uses HALF_UP rounding mode for consistent behavior
- **Zero multiplication**: Results in zero-month interval (valid)

## Code Generation
Supports full Tungsten code generation for all numeric types:
- Integer types: Direct `Math.multiplyExact()` calls
- Long type: Nested `Math.toIntExact(Math.multiplyExact())` calls  
- Floating-point types: `DoubleMath.roundToInt()` with rounding mode
- Decimal types: Inline decimal arithmetic with rounding and exact conversion

## Examples
```sql
-- Multiply interval by integer
SELECT INTERVAL '2-6' YEAR TO MONTH * 3;  -- Results in '7-6' (7 years 6 months)

-- Multiply interval by decimal
SELECT INTERVAL '1-0' YEAR TO MONTH * 2.5;  -- Results in '2-6' (2 years 6 months)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("year_month_interval") * lit(2))
df.select(col("year_month_interval") * col("multiplier"))
```

## See Also
- `MultiplyDTInterval` - For day-time interval multiplication
- `DivideYMInterval` - For year-month interval division
- `AddYMInterval` - For year-month interval addition
- `SubtractYMInterval` - For year-month interval subtraction