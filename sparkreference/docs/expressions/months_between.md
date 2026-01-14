# MonthsBetween

## Overview
The `MonthsBetween` expression calculates the number of months between two timestamp values. It returns a double precision number representing the fractional months difference, with optional rounding behavior controlled by a boolean parameter.

## Syntax
```sql
months_between(date1, date2[, roundOff])
```

```scala
months_between(date1, date2)
months_between(date1, date2, roundOff)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| date1 | TimestampType | The first timestamp value (end date) |
| date2 | TimestampType | The second timestamp value (start date) |
| roundOff | BooleanType | Optional. Whether to round the result (defaults to true) |

## Return Type
`DoubleType` - Returns a double precision floating point number representing the number of months between the two dates.

## Supported Data Types

- Input: TimestampType for date arguments, BooleanType for roundOff parameter
- Implicit casting is supported through `ImplicitCastInputTypes` trait
- Output: Always returns DoubleType regardless of input precision

## Algorithm

- Calculates the difference between two timestamp values in months using `DateTimeUtils.monthsBetween`
- Takes timezone information into account when performing the calculation
- Applies rounding logic based on the roundOff boolean parameter
- Returns positive values when date1 > date2, negative when date1 < date2

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it's a row-level transformation
- Does not require shuffle operations
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null if any input argument is null (nullIntolerant = true)
- **Timezone sensitivity**: Results depend on the configured timezone through TimeZoneAwareExpression
- **Fractional months**: Returns fractional values for partial month differences
- **Rounding behavior**: When roundOff is true, applies specific rounding rules defined in DateTimeUtils

## Code Generation
This expression supports Tungsten code generation. It generates optimized Java code that directly calls `DateTimeUtils.monthsBetween` with the timezone reference, avoiding interpreted evaluation overhead.

## Examples
```sql
-- Basic usage
SELECT months_between('2023-06-15', '2023-01-15') as months_diff;
-- Result: 5.0

-- With rounding disabled
SELECT months_between('2023-06-20', '2023-01-10', false) as exact_months;
-- Result: 5.322580645161290

-- Negative result (date1 < date2)
SELECT months_between('2023-01-15', '2023-06-15') as months_diff;
-- Result: -5.0
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.months_between

df.select(months_between($"end_date", $"start_date").as("duration_months"))

// With explicit rounding parameter
df.select(months_between($"end_date", $"start_date", lit(false)).as("exact_duration"))
```

## See Also

- `datediff` - Calculate difference in days between dates
- `add_months` - Add months to a timestamp
- `date_sub` / `date_add` - Add or subtract days from dates
- Other datetime functions in the `datetime_funcs` group