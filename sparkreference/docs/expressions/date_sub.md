# DateSub

## Overview
The DateSub expression subtracts a specified number of days from a given date. It operates on date values and returns a new date that is the specified number of days earlier than the input date.

## Syntax
```sql
date_sub(start_date, num_days)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| startDate | DateType | The starting date from which to subtract days |
| days | IntegerType, ShortType, ByteType | The number of days to subtract from the start date |

## Return Type
DateType - Returns a date value representing the result of the subtraction operation.

## Supported Data Types

- **Input date**: DateType only
- **Days parameter**: IntegerType, ShortType, or ByteType (any integer numeric type in the TypeCollection)

## Algorithm

- Converts the start date to its internal integer representation (days since epoch)
- Converts the days parameter to an integer value using `intValue()`
- Performs integer subtraction: `startDate - days`
- Returns the result as a date value
- Uses null-safe evaluation to handle null inputs properly

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null if either input parameter is null (null-intolerant behavior)
- **Negative days**: Subtracting negative days effectively adds days to the date
- **Integer overflow**: Uses standard integer arithmetic, so extremely large day values may cause overflow
- **Date boundaries**: Results outside valid date ranges may cause issues depending on the underlying date implementation

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which generates optimized Java code for the subtraction operation: `${ev.value} = $sd - $d;`

## Examples
```sql
-- Subtract 5 days from a specific date
SELECT date_sub('2016-07-30', 5);
-- Result: 2016-07-25

-- Subtract 1 day from a date column
SELECT date_sub(order_date, 1) FROM orders;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(date_sub(col("start_date"), lit(7)))
df.withColumn("previous_week", date_sub(col("current_date"), 7))
```

## See Also

- DateAdd - for adding days to a date
- DateDiff - for calculating the difference between two dates
- Date and time functions in Spark SQL