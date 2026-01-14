# TimeAddInterval

## Overview
TimeAddInterval is a Spark Catalyst expression that adds a day-time interval to a time value. It extends BinaryExpression and RuntimeReplaceable, meaning it is replaced with a StaticInvoke call to DateTimeUtils.timeAddInterval during expression optimization. The expression handles precision calculation to ensure the result maintains appropriate time precision based on both the input time and interval types.

## Syntax
```sql
time_expression + interval_expression
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| time | Expression | The base time value to which the interval will be added |
| interval | Expression | The day-time interval to add to the time |

## Return Type
Returns a `TimeType` with precision calculated as the maximum of the input time precision and the interval precision. The interval precision is determined by the interval's end field - if less than SECOND, uses MIN_PRECISION, otherwise uses MICROS_PRECISION.

## Supported Data Types

- **time**: `AnyTimeType` - accepts time values with any precision
- **interval**: `DayTimeIntervalType` - accepts day-time intervals with any start and end fields

## Algorithm

- Extracts precision from the input time type and end field from the interval type
- Calculates interval precision based on the end field (MIN_PRECISION if < SECOND, otherwise MICROS_PRECISION)  
- Determines target precision as the maximum of time precision and interval precision
- Creates a StaticInvoke expression calling DateTimeUtils.timeAddInterval with the calculated precisions
- Passes time, time precision, interval, interval end field, and target precision as arguments

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be evaluated independently for each partition

## Edge Cases

- **Null handling**: The expression is null intolerant (nullIntolerant = true), meaning null inputs produce null outputs with proper null propagation
- **Type validation**: Throws SparkException.internalError if unexpected input types are encountered during replacement
- **Precision handling**: Automatically adjusts precision to accommodate both time and interval precision requirements
- **Overflow behavior**: Relies on underlying DateTimeUtils.timeAddInterval implementation for overflow handling

## Code Generation
This expression uses RuntimeReplaceable pattern and does not directly support Tungsten code generation. It is replaced with a StaticInvoke expression during optimization, which calls the interpreted DateTimeUtils.timeAddInterval method.

## Examples
```sql
-- Add 2 hours to a time value
SELECT TIME '10:30:00' + INTERVAL '2' HOUR;

-- Add days and hours to a time (days component wraps around)
SELECT TIME '14:15:30' + INTERVAL '1 5' DAY TO HOUR;
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("time_col") + expr("INTERVAL '30' MINUTE"))

// Using interval literal
df.select(col("time_col") + lit(Duration.ofHours(3)))
```

## See Also

- TimeSubInterval - for subtracting intervals from time values
- TimestampAddInterval - for adding intervals to timestamp values  
- DateTimeUtils.timeAddInterval - the underlying implementation method
- DayTimeIntervalType - for day-time interval data type details