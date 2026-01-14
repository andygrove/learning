# MakeDTInterval

## Overview

The `MakeDTInterval` expression creates a day-time interval value from separate day, hour, minute, and second components. This expression is used to construct `DayTimeIntervalType` values programmatically by combining individual time unit values into a single interval representation.

## Syntax

```sql
make_dt_interval(days, hours, minutes, seconds)
make_dt_interval(days, hours, minutes)
make_dt_interval(days, hours)
make_dt_interval(days)
make_dt_interval()
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `days` | IntegerType | Number of days in the interval (optional, defaults to 0) |
| `hours` | IntegerType | Number of hours in the interval (optional, defaults to 0) |
| `minutes` | IntegerType | Number of minutes in the interval (optional, defaults to 0) |
| `seconds` | DecimalType(MAX_LONG_DIGITS, 6) | Number of seconds including microsecond precision (optional, defaults to 0) |

## Return Type

Returns a `DayTimeIntervalType()` representing the constructed interval.

## Supported Data Types

- **days**: Integer values
- **hours**: Integer values  
- **minutes**: Integer values
- **seconds**: Decimal values with up to 6 decimal places for microsecond precision

## Algorithm

- Accepts up to 4 parameters with multiple constructor overloads for flexibility
- Validates input types through implicit casting to ensure proper data types
- Uses `IntervalUtils.makeDayTimeInterval()` to perform the actual interval construction
- Preserves microsecond precision by accepting seconds as DecimalType rather than losing precision through conversion
- Incorporates query context for proper error reporting during interval creation

## Partitioning Behavior

- **Preserves partitioning**: Yes, this is a deterministic expression that does not require data movement
- **Requires shuffle**: No, the expression operates on individual rows independently

## Edge Cases

- **Null handling**: Expression is null-intolerant (`nullIntolerant = true`), meaning if any input is null, the result is null
- **Default values**: Missing parameters default to 0 (literal values)
- **Precision handling**: Seconds parameter uses DecimalType with 6 decimal places to preserve microsecond precision
- **Overflow behavior**: Delegates to `IntervalUtils.makeDayTimeInterval()` for overflow validation and error handling
- **Error context**: Includes query context information for meaningful error messages when interval construction fails

## Code Generation

This expression supports Tungsten code generation through the `doGenCode` method. It generates efficient Java code that directly calls `IntervalUtils.makeDayTimeInterval()` with the provided parameters, avoiding interpreted evaluation overhead.

## Examples

```sql
-- Create a 5-day, 3-hour, 30-minute, 45.5-second interval
SELECT make_dt_interval(5, 3, 30, 45.5);

-- Create a 2-day interval
SELECT make_dt_interval(2);

-- Create a 1-day, 12-hour interval  
SELECT make_dt_interval(1, 12);

-- Create an empty interval
SELECT make_dt_interval();
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Create interval from literal values
df.select(expr("make_dt_interval(5, 3, 30, 45.5)"))

// Create interval from column values
df.select(expr("make_dt_interval(day_col, hour_col, min_col, sec_col)"))
```

## See Also

- `MakeYMInterval` - Creates year-month intervals
- `IntervalUtils` - Utility class for interval operations
- `DayTimeIntervalType` - The data type returned by this expression
- `Extract` - Extracts components from interval values