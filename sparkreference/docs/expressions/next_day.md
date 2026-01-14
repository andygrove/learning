# NextDay

## Overview
The `NextDay` expression returns the first date after a given start date that falls on a specified day of the week. It advances from the start date to find the next occurrence of the target day, excluding the start date itself even if it matches the target day of week.

## Syntax
```sql
next_day(start_date, day_of_week)
```

```scala
// DataFrame API
col("date_column").next_day("Monday")
next_day(col("start_date"), col("day_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| startDate | DateType | The starting date from which to find the next occurrence |
| dayOfWeek | StringType (with collation support) | The target day of week as a string (e.g., "Monday", "Tue") |
| failOnError | Boolean | Internal parameter controlling ANSI mode behavior for invalid inputs |

## Return Type
Returns `DateType` - an integer representing days since epoch (1970-01-01).

## Supported Data Types

- **Input**: DateType for start date, StringType with collation support for day of week
- **Output**: DateType
- **Trimming**: Supports trim collation for the day of week string parameter

## Algorithm

- Parse the day of week string using `DateTimeUtils.getDayOfWeekFromString()` to get numeric day representation
- Convert the start date to internal integer representation (days since epoch)
- Calculate the next date that falls on the target day of week using `DateTimeUtils.getNextDateForDayOfWeek()`
- Handle invalid day of week strings by either throwing exception (ANSI mode) or returning null
- Return the result as a DateType value

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require shuffle operations
- Maintains existing data distribution
- Can be evaluated locally on each partition
- Safe for use in partitioned operations

## Edge Cases

- **Null handling**: Returns null if either input is null (null intolerant behavior)
- **Invalid day names**: Throws `SparkIllegalArgumentException` in ANSI mode, returns null otherwise
- **Case sensitivity**: Day of week parsing follows `DateTimeUtils` case handling rules
- **Abbreviations**: Supports abbreviated day names (implementation dependent on `DateTimeUtils`)
- **Same day exclusion**: Never returns the start date itself, always advances to next occurrence

## Code Generation
This expression supports full Tungsten code generation with optimizations:

- Generates efficient Java code for the evaluation logic
- Includes compile-time optimization for constant (foldable) day of week values
- Falls back to runtime evaluation for dynamic day of week expressions
- Handles exception generation in both ANSI and non-ANSI modes during code generation

## Examples
```sql
-- Find next Monday after January 1st, 2023
SELECT next_day('2023-01-01', 'Monday');
-- Returns: 2023-01-02

-- Using with column references
SELECT order_date, next_day(order_date, 'Friday') as next_friday
FROM orders;

-- Next Tuesday after current date
SELECT next_day(current_date(), 'Tue');
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Find next Monday for each date
df.select(col("start_date"), next_day(col("start_date"), lit("Monday")))

// Dynamic day of week from another column  
df.select(next_day(col("event_date"), col("target_day")))

// Using string interpolation
df.withColumn("next_sunday", next_day($"date_col", "Sunday"))
```

## See Also

- `date_add` - Add days to a date
- `date_sub` - Subtract days from a date  
- `dayofweek` - Extract day of week from date
- `last_day` - Get last day of month
- `DateTimeUtils` - Underlying utility class for date operations