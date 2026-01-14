# DivideYMInterval

## Overview
The `DivideYMInterval` expression divides a year-month interval by a numeric value, returning a new year-month interval. This operation supports division by various numeric types including integral, decimal, and fractional types, with proper rounding using the HALF_UP rounding mode.

## Syntax
```sql
year_month_interval / numeric_value
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| interval | YearMonthIntervalType | The year-month interval to be divided |
| num | NumericType | The numeric divisor (IntegralType, DecimalType, or FractionalType) |

## Return Type
Returns `YearMonthIntervalType()` - a year-month interval with the same structure as the input interval.

## Supported Data Types
**Left operand (interval):**
- YearMonthIntervalType

**Right operand (num):**
- LongType
- IntegralType (IntegerType, ShortType, ByteType)
- DecimalType
- FractionalType (DoubleType, FloatType)

## Algorithm
- Extracts the internal month representation from the year-month interval (stored as Int)
- Applies type-specific division logic based on the numeric divisor type:
  - **LongType**: Uses `LongMath.divide()` with HALF_UP rounding, then casts to Int
  - **IntegralType**: Uses `IntMath.divide()` with HALF_UP rounding
  - **DecimalType**: Converts to Decimal, performs division, then rounds to nearest integer
  - **FractionalType**: Uses `DoubleMath.roundToInt()` with HALF_UP rounding
- Performs overflow and divide-by-zero checks before computation

## Partitioning Behavior
This expression preserves partitioning:
- Does not require data shuffle
- Operates on individual rows independently
- Maintains existing partition boundaries

## Edge Cases
- **Null handling**: Expression is null-intolerant - returns null if either operand is null
- **Divide by zero**: Throws `QueryExecutionErrors` when divisor is zero
- **Overflow behavior**: 
  - Checks for `Int.MinValue / -1` overflow condition
  - Throws `QueryExecutionErrors.overflowInIntegralDivideError` on overflow
  - Uses `intValueExact()` for Decimal results to ensure no precision loss
- **Rounding**: All division operations use `RoundingMode.HALF_UP` for consistent behavior

## Code Generation
Supports full Tungsten code generation with type-specific optimizations:
- Generates inline division code based on divisor data type
- Includes compile-time overflow and divide-by-zero checks
- Uses appropriate math libraries (`LongMath`, `IntMath`, `DoubleMath`) in generated code
- Avoids interpreted evaluation overhead

## Examples
```sql
-- Divide a 2-year 6-month interval by 2
SELECT INTERVAL '2-6' YEAR TO MONTH / 2;
-- Result: INTERVAL '1-3' YEAR TO MONTH

-- Divide by decimal value
SELECT INTERVAL '5-0' YEAR TO MONTH / 2.5;
-- Result: INTERVAL '2-0' YEAR TO MONTH
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("year_month_interval") / lit(3))

// Using expression directly
val divideExpr = DivideYMInterval(
  interval = col("ym_interval").expr,
  num = lit(2).expr
)
```

## See Also
- `MultiplyYMInterval` - Multiplication of year-month intervals
- `DivideDTInterval` - Division of day-time intervals  
- `ExtractIntervalYears` - Extracting years from intervals
- `ExtractIntervalMonths` - Extracting months from intervals