# Trunc

## Overview
The `TruncDate` expression truncates a date to the unit specified by the format parameter. It returns the first day of the specified time unit (year, quarter, month, or week) for the given date. This is implemented as the `TruncDate` case class extending `TruncInstant` trait.

Unlike `date_trunc`, this function operates on dates (not timestamps) and does not support day-level or time-level truncation.

## Syntax
```sql
TRUNC(date, format)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
trunc(col("date_column"), "year")
trunc(col("date_column"), "month")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| date | DateType or StringType (castable to date) | The date value to truncate |
| format | StringType | The unit to truncate to (see supported units below) |

## Return Type
Returns DateType. The result is the first day of the specified unit period.

## Supported Format Units

| Unit | Aliases | Description |
|------|---------|-------------|
| year | 'YEAR', 'YYYY', 'YY' | Truncate to the first date of the year that the date falls in |
| quarter | 'QUARTER' | Truncate to the first date of the quarter that the date falls in |
| month | 'MONTH', 'MM', 'MON' | Truncate to the first date of the month that the date falls in |
| week | 'WEEK' | Truncate to the Monday of the week that the date falls in |

**Note:** Day-level truncation is NOT supported by `trunc()`. Use `date_trunc()` for day or time-level truncation.

## Internal Implementation

From `DateTimeUtils.truncDate()`:
```scala
def truncDate(days: Int, level: Int): Int = {
  level match {
    case TRUNC_TO_WEEK => getNextDateForDayOfWeek(days - 7, MONDAY)
    case TRUNC_TO_MONTH => days - getDayOfMonth(days) + 1
    case TRUNC_TO_QUARTER =>
      localDateToDays(daysToLocalDate(days).`with`(IsoFields.DAY_OF_QUARTER, 1L))
    case TRUNC_TO_YEAR => days - getDayInYear(days) + 1
    case _ => throw QueryExecutionErrors.unreachableError(...)
  }
}
```

## Algorithm

- Parses the format string using `parseTruncLevel()` to get the truncation level constant
- Delegates to `DateTimeUtils.truncDate(days, level)` which computes offset-based truncation
- For 'YEAR': subtracts day-of-year offset to get January 1st
- For 'QUARTER': uses `IsoFields.DAY_OF_QUARTER` to find first day of quarter
- For 'MONTH': subtracts day-of-month offset to get the 1st
- For 'WEEK': finds the previous Monday using `getNextDateForDayOfWeek`

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows:

- Does not require shuffle operations
- Maintains existing partitioning scheme
- Can be pushed down to individual partitions

## Edge Cases

- **Null handling**: Returns null if the date argument is null
- **Invalid format**: Returns null if the format string is not recognized
- **Day format**: Returns null when 'day' or 'dd' is used (not supported)
- **Case sensitivity**: Format string is case-insensitive
- **String dates**: String inputs are implicitly cast to DateType

## Examples

From Spark documentation:
```sql
-- Truncate to week (returns Monday of that week)
SELECT TRUNC('2019-08-04', 'week');
-- Returns: 2019-07-29

-- Truncate to quarter
SELECT TRUNC('2019-08-04', 'quarter');
-- Returns: 2019-07-01

-- Truncate to month
SELECT TRUNC('2009-02-12', 'MM');
-- Returns: 2009-02-01

-- Truncate to year
SELECT TRUNC('2015-10-27', 'YEAR');
-- Returns: 2015-01-01

-- Day truncation returns null (not supported by trunc)
SELECT TRUNC('2024-03-15', 'day');
-- Returns: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(trunc(col("date_col"), "year").alias("year_start"))
df.select(trunc(col("date_col"), "mon").alias("month_start"))
df.select(trunc($"date_col", "quarter").alias("quarter_start"))
```

## See Also

- `date_trunc` - Truncate timestamps to any unit including day and time components
- `time_trunc` - Truncate time values to time-level precision
- `last_day` - Returns the last day of the month
- `next_day` - Returns the next occurrence of a day of week
