# SubtractTimes

## Overview
The `SubtractTimes` expression calculates the day-time interval between two time values by subtracting the right operand from the left operand. It is implemented as a runtime-replaceable expression that delegates to the `DateTimeUtils.subtractTimes` method for the actual computation.

## Syntax
```sql
time_expression1 - time_expression2
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The left time expression (minuend) |
| right | Expression | The right time expression (subtrahend) |

## Return Type
Returns a `DayTimeIntervalType` with precision from `HOUR` to `SECOND` representing the interval between the two time values.

## Supported Data Types
This expression accepts any time-related data types as defined by `AnyTimeType`, which typically includes:

- TimestampType
- DateType  
- TimeType (if supported by the SQL dialect)

## Algorithm
The expression evaluation follows these steps:

- Validates that both input expressions are of compatible time types
- Delegates the actual subtraction computation to `DateTimeUtils.subtractTimes`
- Converts the result to a day-time interval with hour-to-second precision
- Preserves null values when either input is null due to `nullIntolerant = true`
- Uses static method invocation for runtime replacement to optimize performance

## Partitioning Behavior
This expression has neutral partitioning behavior:

- Does not affect existing partitioning schemes
- Does not require data shuffling
- Can be evaluated locally on each partition

## Edge Cases

- **Null handling**: Returns null if either the left or right expression evaluates to null (null-intolerant behavior)
- **Type compatibility**: Both operands must be convertible to time types, otherwise compilation fails
- **Negative intervals**: When the right operand represents a later time than the left operand, the result will be a negative interval
- **Precision**: Results are limited to day-time intervals with hour-to-second precision, losing any sub-second precision beyond what the interval type supports

## Code Generation
This expression supports code generation through the `RuntimeReplaceable` trait. It generates a `StaticInvoke` call to `DateTimeUtils.subtractTimes` rather than using interpreted evaluation, providing better performance in Tungsten-generated code.

## Examples
```sql
-- Calculate time difference between timestamps
SELECT TIMESTAMP '2023-01-02 15:30:00' - TIMESTAMP '2023-01-01 10:15:30'
-- Returns: INTERVAL '1 05:14:30' DAY TO SECOND

-- Using with column references
SELECT end_time - start_time AS duration FROM events
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select($"end_time" - $"start_time" as "duration")

// Using expr() for complex expressions
df.select(expr("end_time - start_time") as "time_diff")
```

## See Also
- `DateAdd` - Adding intervals to dates/timestamps
- `DateSub` - Subtracting intervals from dates/timestamps  
- `DayTimeIntervalType` - The return type for day-time intervals
- `DateTimeUtils` - Utility class containing the underlying subtraction logic