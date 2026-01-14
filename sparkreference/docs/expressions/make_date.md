# MakeDate

## Overview
The MakeDate expression creates a date value from separate integer year, month, and day components. It validates the input values and returns a DateType value representing the constructed date, with configurable error handling based on ANSI SQL compliance mode.

## Syntax
```sql
make_date(year, month, day)
```

```scala
// DataFrame API
col("year_col").make_date(col("month_col"), col("day_col"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| year | Expression (IntegerType) | The year component as an integer |
| month | Expression (IntegerType) | The month component as an integer (1-12) |
| day | Expression (IntegerType) | The day component as an integer (1-31, depending on month) |
| failOnError | Boolean | Internal parameter controlling error handling behavior (defaults to SQLConf.ansiEnabled) |

## Return Type
DateType - Returns a date value representing the constructed date.

## Supported Data Types

- Input types: All three arguments must be IntegerType or expressions that can be implicitly cast to IntegerType
- Output type: DateType

## Algorithm

- Accepts three integer expressions representing year, month, and day components
- Uses Java's LocalDate.of() method to construct and validate the date
- Converts the LocalDate to internal Spark date representation using localDateToDays()
- Handles invalid date combinations (like February 30th) through DateTimeException catching
- Returns null or throws exception based on failOnError flag when invalid dates are provided

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it operates row-by-row without requiring data redistribution
- Does not require shuffle operations
- Can be used safely in partition-by clauses and WHERE conditions

## Edge Cases

- Null handling: Returns null if any input argument is null (nullIntolerant = true)
- Invalid dates: When ANSI mode is enabled (failOnError = true), throws QueryExecutionErrors.ansiDateTimeArgumentOutOfRange for invalid dates
- Invalid dates: When ANSI mode is disabled, returns null for invalid date combinations
- Date range: Limited by Java LocalDate supported range (Year.MIN_VALUE to Year.MAX_VALUE)
- Nullable behavior: In failOnError mode, nullable only if children are nullable; otherwise always nullable

## Code Generation
This expression supports Tungsten code generation through the doGenCode method. It generates optimized Java code that directly calls DateTimeUtils.localDateToDays() and handles exceptions inline, avoiding the overhead of interpreted evaluation.

## Examples
```sql
-- Create a date from components
SELECT make_date(2023, 12, 25) AS christmas_2023;

-- Handle invalid dates (returns NULL in non-ANSI mode)
SELECT make_date(2023, 2, 30) AS invalid_date;

-- Use with table columns
SELECT make_date(birth_year, birth_month, birth_day) AS birth_date
FROM people;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Create date from literal values
df.select(expr("make_date(2023, 12, 25)").as("christmas"))

// Create date from column values
df.select(expr("make_date(year_col, month_col, day_col)").as("constructed_date"))
```

## See Also

- MakeTimestamp - Creates timestamp values from date and time components
- DateAdd - Adds days to a date
- DateSub - Subtracts days from a date
- Year, Month, Day - Extract components from existing dates