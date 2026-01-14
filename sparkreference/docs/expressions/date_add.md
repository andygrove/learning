# DateAdd

## Overview
The `DateAdd` expression adds a specified number of days to a given date value. It is a binary expression that takes a date and an integer representing the number of days to add, returning a new date value.

## Syntax
```sql
date_add(start_date, num_days)
```

```scala
// DataFrame API usage
df.select(date_add(col("date_column"), lit(5)))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| startDate | DateType | The base date to which days will be added |
| days | IntegerType, ShortType, ByteType | The number of days to add (can be negative for subtraction) |

## Return Type
`DateType` - Returns a date value representing the original date plus the specified number of days.

## Supported Data Types

- **Input**: DateType for the first argument, numeric types (IntegerType, ShortType, ByteType) for the second argument
- **Output**: DateType

## Algorithm

- Takes the input date as an internal integer representation (days since epoch)
- Converts the days parameter to an integer value using `intValue()`
- Performs simple integer addition: `start.asInstanceOf[Int] + d.asInstanceOf[Number].intValue()`
- Returns the result as a date value
- Uses null-safe evaluation to handle null inputs properly

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows without requiring data movement:

- Does not require shuffle operations
- Maintains existing data distribution
- Can be executed locally on each partition

## Edge Cases

- **Null handling**: Returns null if either input argument is null (null-intolerant behavior)
- **Negative values**: Supports negative day values to subtract days from the date
- **Overflow**: May produce unexpected results if the calculation exceeds valid date ranges
- **Type conversion**: Automatically converts ShortType and ByteType to integers for calculation

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which generates optimized Java code for better performance rather than falling back to interpreted evaluation.

## Examples
```sql
-- Add 1 day to a specific date
SELECT date_add('2016-07-30', 1);
-- Result: 2016-07-31

-- Subtract 5 days using negative value
SELECT date_add('2023-01-15', -5);
-- Result: 2023-01-10

-- Use with table columns
SELECT date_add(order_date, 30) as due_date FROM orders;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Add days to a date column
df.select(date_add(col("start_date"), lit(7)).alias("end_date"))

// Use with variable days
df.select(date_add(col("order_date"), col("processing_days")))
```

## See Also

- `date_sub` - Subtract days from a date
- `add_months` - Add months to a date
- `datediff` - Calculate difference between two dates