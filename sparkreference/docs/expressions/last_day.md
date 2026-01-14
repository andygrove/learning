# LastDay

## Overview

The `LastDay` expression calculates the last day of the month for a given date. It takes a date as input and returns a new date representing the final day of that same month and year.

## Syntax

```sql
last_day(date_expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.last_day
df.select(last_day($"date_column"))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| startDate | DateType | The input date for which to find the last day of the month |

## Return Type

`DateType` - Returns a date representing the last day of the month containing the input date.

## Supported Data Types

- DateType (input will be implicitly cast to DateType if compatible)

## Algorithm

- Extracts the year and month components from the input date

- Determines the number of days in that specific month, accounting for leap years when necessary

- Constructs a new date using the same year and month but with the day set to the maximum day of that month

- Returns the resulting date as an integer representation (days since epoch)

- Delegates the actual calculation to `DateTimeUtils.getLastDayOfMonth()`

## Partitioning Behavior

- Preserves partitioning since it operates on individual rows without requiring data movement

- Does not require shuffle as the transformation is applied locally to each partition

## Edge Cases

- **Null handling**: Returns null if the input date is null (null intolerant behavior)

- **Leap years**: Correctly handles February in leap years (returns February 29) vs non-leap years (returns February 28)

- **Month boundaries**: Properly handles months with different numbers of days (30, 31, 28, or 29 days)

- **Date range limits**: Behavior depends on the underlying `DateTimeUtils.getLastDayOfMonth()` implementation for edge dates

## Code Generation

Supports Tungsten code generation through the `doGenCode` method. The generated code directly calls `DateTimeUtils.getLastDayOfMonth()` for optimal performance, avoiding interpretation overhead.

## Examples

```sql
-- Get the last day of January 2009
SELECT last_day('2009-01-12');
-- Result: 2009-01-31

-- Get the last day for multiple dates
SELECT last_day('2020-02-15'), last_day('2021-02-15');
-- Result: 2020-02-29, 2021-02-28 (leap year vs non-leap year)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.last_day

// Calculate last day of month for a date column
df.select(last_day($"order_date").alias("month_end"))

// Use in filtering
df.filter(last_day($"date_col") === lit("2023-12-31"))
```

## See Also

- `date_add()` - Add days to a date
- `date_sub()` - Subtract days from a date
- `trunc()` - Truncate date to specified unit
- `add_months()` - Add months to a date