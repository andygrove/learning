# DateAddInterval

## Overview

The `DateAddInterval` expression adds a calendar interval to a date value and returns the resulting date. It supports both ANSI-compliant mode for strict error handling and optimized evaluation paths based on the interval's microsecond component.

## Syntax

```sql
date_column + interval_expression
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| start | DateType | The starting date to which the interval will be added |
| interval | CalendarIntervalType | The calendar interval containing months, days, and microseconds |
| timeZoneId | Option[String] | Optional timezone identifier for timestamp conversions (defaults to None) |
| ansiEnabled | Boolean | Flag indicating whether ANSI mode is enabled (defaults to SQLConf setting) |

## Return Type

`DateType` - Returns a date value representing the sum of the input date and interval.

## Supported Data Types

- **Input**: `DateType` for the start date, `CalendarIntervalType` for the interval
- **Output**: `DateType`

## Algorithm

- Extracts the calendar interval components (months, days, microseconds) from the input
- In ANSI mode or when microseconds are zero, performs direct date arithmetic using `dateAddInterval`
- When ANSI mode is off and microseconds are non-zero, converts the date to timestamp, performs interval addition, then converts back to date
- Uses timezone-aware conversions when dealing with timestamp intermediates
- Applies timezone information for accurate date-to-timestamp conversions when necessary

## Partitioning Behavior

This expression does not affect partitioning behavior:

- Preserves existing partitioning schemes
- Does not require data shuffle operations
- Can be evaluated locally on each partition

## Edge Cases

- **Null handling**: Null-intolerant - returns null if either input is null
- **ANSI mode**: Throws `IllegalArgumentException` for invalid date arithmetic operations
- **Microsecond precision**: Automatically handles conversion between date and timestamp representations based on interval precision
- **Timezone sensitivity**: Uses specified timezone for intermediate timestamp calculations when microseconds are present
- **Overflow**: Delegates overflow handling to underlying `DateTimeUtils` methods

## Code Generation

This expression supports Tungsten code generation through the `doGenCode` method:

- Generates optimized bytecode for both ANSI and non-ANSI execution paths
- Creates conditional code branches based on microsecond component presence
- Efficiently handles timezone references in generated code

## Examples

```sql
-- Add 1 month to a date
SELECT DATE '2023-01-15' + INTERVAL '1' MONTH;

-- Add complex interval to date
SELECT DATE '2023-01-15' + INTERVAL '2 months 10 days';
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("date_column") + expr("INTERVAL '1' MONTH"))

// Using interval literal
df.select(col("date_column") + lit(CalendarInterval.fromString("1 month 5 days")))
```

## See Also

- `DatetimeSub` - Subtracts intervals from dates
- `TimestampAddInterval` - Adds intervals to timestamps
- `CalendarInterval` - Represents calendar intervals with months, days, and microseconds