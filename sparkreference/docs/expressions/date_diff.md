# DateDiff

## Overview
The DateDiff expression calculates the number of days between two date values. It computes the difference by subtracting the start date from the end date, returning a positive value when the end date is later than the start date, and a negative value when the end date is earlier.

## Syntax
```sql
DATEDIFF(endDate, startDate)
```

```scala
// DataFrame API
col("endDate") - col("startDate")  // Using DateDiff internally
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| endDate | DateType | The end date for the difference calculation |
| startDate | DateType | The start date for the difference calculation |

## Return Type
IntegerType - Returns the number of days as an integer value.

## Supported Data Types

- Input types: DateType only (other types are implicitly cast to DateType if possible)
- Both arguments must be convertible to DateType through implicit casting

## Algorithm

- Accepts two date expressions as input parameters
- Performs implicit type casting to ensure both inputs are DateType
- Internally represents dates as integers (days since epoch)
- Calculates difference using simple integer subtraction: `endDate - startDate`
- Returns the raw integer difference representing days

## Partitioning Behavior

- Preserves partitioning as it operates on individual rows
- Does not require data shuffle across partitions
- Can be executed locally on each partition independently

## Edge Cases

- **Null handling**: Returns null if either input is null (nullIntolerant = true)
- **Negative results**: Returns negative integers when endDate is earlier than startDate
- **Same date**: Returns 0 when both dates are identical
- **Integer overflow**: Theoretically possible with extreme date ranges, but unlikely in practical usage

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which generates optimized Java code performing simple integer subtraction for better performance.

## Examples
```sql
-- Basic date difference
SELECT DATEDIFF('2009-07-31', '2009-07-30');
-- Returns: 1

-- Negative difference (end date earlier than start date)
SELECT DATEDIFF('2009-07-30', '2009-07-31');
-- Returns: -1

-- Same dates
SELECT DATEDIFF('2009-07-30', '2009-07-30');
-- Returns: 0

-- With null values
SELECT DATEDIFF(NULL, '2009-07-30');
-- Returns: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(datediff(col("end_date"), col("start_date")).as("days_diff"))

// Using with literal dates
df.select(datediff(lit("2009-07-31"), lit("2009-07-30")).as("days_diff"))
```

## See Also

- DateAdd - Adds days to a date
- DateSub - Subtracts days from a date  
- MonthsBetween - Calculates months between two dates
- TimestampDiff - Calculates differences between timestamps