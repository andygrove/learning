# SecondsToTimestamp

## Overview
The `SecondsToTimestamp` expression converts numeric values representing seconds since Unix epoch (1970-01-01 00:00:00 UTC) into timestamp values. It supports various numeric data types and handles the conversion by multiplying the input value by the number of microseconds per second to produce a timestamp in Spark's internal microsecond representation.

## Syntax
```sql
timestamp_seconds(seconds)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
col("seconds_column").cast(TimestampType)
// or using the function name
expr("timestamp_seconds(seconds_column)")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| seconds | Numeric | The number of seconds since Unix epoch (1970-01-01 00:00:00 UTC) to convert to timestamp |

## Return Type
`TimestampType` - Returns a timestamp value representing the specified number of seconds since Unix epoch.

## Supported Data Types

- IntegralType (Byte, Short, Integer, Long)
- DecimalType 
- FloatType
- DoubleType

## Algorithm

- For integral types: Multiplies the input value by `MICROS_PER_SECOND` using `Math.multiplyExact()` for overflow protection
- For decimal types: Converts to `BigDecimal`, multiplies by `MICROS_PER_SECOND`, and extracts the long value with exact precision
- For float types: Checks for NaN/Infinite values, converts to double, multiplies by `MICROS_PER_SECOND`, and converts to long
- For double types: Checks for NaN/Infinite values, multiplies by `MICROS_PER_SECOND`, and converts to long
- All conversions target Spark's internal timestamp representation in microseconds since Unix epoch

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffling
- Can be applied within existing partitions
- Does not change the distribution of data across partitions

## Edge Cases

- **Null handling**: Expression is null-intolerant, meaning null inputs produce null outputs
- **Float/Double special values**: NaN and Infinite values in float/double inputs return null instead of throwing exceptions
- **Overflow protection**: Integral types use `Math.multiplyExact()` and decimal types use `longValueExact()` to detect arithmetic overflow
- **Precision handling**: Decimal inputs maintain precision through `BigDecimal` arithmetic before final conversion
- **Nullable behavior**: Float and Double inputs make the result nullable due to potential NaN/Infinite handling; other numeric types inherit nullability from the child expression

## Code Generation
This expression supports Tungsten code generation with optimized paths for different numeric types:

- Integral types generate direct `Math.multiplyExact()` calls
- Decimal types generate `BigDecimal` multiplication with exact conversion
- Float and Double types generate null-safe code with NaN/Infinite checks

## Examples
```sql
-- Convert integer seconds to timestamp
SELECT timestamp_seconds(1640995200) as converted_timestamp;
-- Result: 2021-12-31 16:00:00

-- Convert decimal seconds to timestamp  
SELECT timestamp_seconds(1640995200.123) as converted_timestamp;
-- Result: 2021-12-31 16:00:00.123

-- Handle null input
SELECT timestamp_seconds(null) as converted_timestamp;
-- Result: null
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Convert seconds column to timestamp
df.select(expr("timestamp_seconds(epoch_seconds)").as("converted_timestamp"))

// Using with literal values
df.select(expr("timestamp_seconds(1640995200)").as("converted_timestamp"))

// Handle floating point seconds
df.select(expr("timestamp_seconds(1640995200.123)").as("converted_timestamp"))
```

## See Also

- `TimestampToSeconds` - Converts timestamps back to seconds since epoch
- `UnixTimestamp` - Similar functionality with different precision handling
- `FromUnixTime` - Converts Unix timestamp to formatted string
- `ToTimestamp` - Converts string to timestamp with format parsing