# MakeInterval

## Overview
The `MakeInterval` expression creates a calendar interval from separate year, month, week, day, hour, minute, and second components. It supports flexible argument lists allowing omission of trailing components, which default to zero.

## Syntax
```sql
make_interval(years, months, weeks, days, hours, mins, secs)
make_interval(years, months, weeks, days, hours, mins)
make_interval(years, months, weeks, days, hours)
-- ... (supports up to 0 arguments with overloaded constructors)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| years | IntegerType | Number of years in the interval |
| months | IntegerType | Number of months in the interval |
| weeks | IntegerType | Number of weeks in the interval |
| days | IntegerType | Number of days in the interval |
| hours | IntegerType | Number of hours in the interval |
| mins | IntegerType | Number of minutes in the interval |
| secs | DecimalType(MAX_LONG_DIGITS, 6) | Number of seconds with microsecond precision |

## Return Type
`CalendarIntervalType` - Returns a calendar interval object containing the specified time components.

## Supported Data Types
- **Integer types**: years, months, weeks, days, hours, minutes
- **Decimal type**: seconds (with scale 6 for microsecond precision)
- All arguments support implicit casting to their required types

## Algorithm
- Validates all input components are within valid ranges for their respective time units
- Combines all time components using `IntervalUtils.makeInterval()` 
- Handles potential arithmetic overflow during interval construction
- Preserves microsecond precision by accepting seconds as decimal with 6-digit scale
- Returns null on overflow when ANSI mode is disabled, throws exception when enabled

## Partitioning Behavior
- **Preserves partitioning**: This expression does not affect data partitioning
- **No shuffle required**: Operates on individual rows independently
- Can be pushed down to individual partitions without cross-partition dependencies

## Edge Cases
- **Null handling**: Returns null if any input argument is null (null intolerant)
- **Overflow behavior**: 
  - When `failOnError=true` (ANSI mode): Throws `QueryExecutionErrors.arithmeticOverflowError`
  - When `failOnError=false`: Returns null on arithmetic overflow
- **Default values**: Missing trailing arguments default to `Literal(0)` except seconds which defaults to `Decimal(0, MAX_LONG_DIGITS, 6)`
- **Nullable result**: When `failOnError=false`, result is always nullable; when `true`, nullable only if any child is nullable

## Code Generation
Supports Tungsten code generation via `doGenCode()` method. Generates optimized Java code that:
- Calls `IntervalUtils.makeInterval()` directly in generated code
- Includes inline exception handling for arithmetic overflow
- Avoids interpreted evaluation overhead for better performance

## Examples
```sql
-- Create interval with all components
SELECT make_interval(1, 2, 3, 4, 5, 6, 7.123456);
-- Result: 1 years 2 months 25 days 5 hours 6 minutes 7.123456 seconds

-- Create interval with partial components
SELECT make_interval(0, 1, 0, 1);  
-- Result: 1 months 1 days

-- Handle overflow in non-ANSI mode
SELECT make_interval(999999999, 0, 0, 0, 0, 0, 0);
-- Result: NULL (on overflow)
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("make_interval(1, 1, 0, 1, 0, 1, 40.000001)"))

// Using literal expressions
df.select(lit(1).alias("years"), lit(1).alias("months"))
  .select(expr("make_interval(years, months, 0, 1, 0, 1, 40.000001)"))
```

## See Also
- `IntervalUtils.makeInterval()` - Underlying utility method
- Calendar interval arithmetic expressions
- `extract()` function for decomposing intervals
- Date/time interval operations