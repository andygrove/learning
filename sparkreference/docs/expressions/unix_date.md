# UnixDate

## Overview
The `UnixDate` expression converts a date value to its Unix date representation, which is the number of days since the Unix epoch (1970-01-01). This expression provides a way to get the integer representation of a date for numerical operations or storage optimization.

## Syntax
```sql
unix_date(date_expr)
```

```scala
// DataFrame API
col("date_column").expr("unix_date(date_column)")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| date_expr | DATE | The date value to convert to Unix date representation |

## Return Type
`INTEGER` - Returns the number of days since 1970-01-01 as an integer value.

## Supported Data Types

- `DateType` - Only date type inputs are supported

## Algorithm

- Takes the internal date representation (already stored as days since epoch)
- Performs a direct cast to integer without any transformation
- Returns the integer value representing days since Unix epoch
- Uses null-safe evaluation to handle null inputs appropriately
- Implements code generation for optimized execution

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require shuffle operations
- Maintains deterministic output for the same input
- Can be used safely in partitioning schemes
- Preserves data locality during processing

## Edge Cases

- **Null handling**: Returns null when input date is null (null-safe evaluation)
- **Negative dates**: Dates before 1970-01-01 will return negative integer values
- **Type enforcement**: Only accepts DATE type inputs, other types will cause compilation errors
- **Integer overflow**: Extremely large date values could theoretically cause integer overflow

## Code Generation
This expression fully supports Tungsten code generation:

- Implements `doGenCode` method for compiled code paths
- Uses direct value passing without complex transformations
- Generates efficient native code for high-performance execution
- Falls back gracefully to interpreted mode if code generation fails

## Examples
```sql
-- Convert specific date to Unix date
SELECT unix_date(DATE('1970-01-02'));
-- Returns: 1

-- Convert date column
SELECT unix_date(birth_date) FROM users;

-- Use in calculations
SELECT unix_date(end_date) - unix_date(start_date) AS duration_days FROM events;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("unix_date(date_column)"))

// In transformations
df.withColumn("unix_date", expr("unix_date(original_date)"))

// Calculate date differences
df.select(
  expr("unix_date(end_date) - unix_date(start_date)").alias("duration")
)
```

## See Also

- `to_date()` - Convert strings or timestamps to date type
- `date_add()` - Add days to a date
- `date_sub()` - Subtract days from a date
- `unix_timestamp()` - Convert timestamp to Unix timestamp (seconds since epoch)