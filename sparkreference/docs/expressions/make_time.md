# MakeTime

## Overview
The `MakeTime` expression creates a time value from separate hour, minute, and second components. It constructs a time of day by combining integer hour and minute values with a decimal seconds value that can include microsecond precision.

## Syntax
```sql
make_time(hours, minutes, seconds)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| hours | IntegerType | The hour component (0-23) |
| minutes | IntegerType | The minute component (0-59) |
| secsAndMicros | DecimalType(16, 6) | The seconds component with microsecond precision (0-59.999999) |

## Return Type
Returns `TimeType` with microsecond precision (`TimeType.MICROS_PRECISION`).

## Supported Data Types

- Hours: Integer types that can be cast to `IntegerType`

- Minutes: Integer types that can be cast to `IntegerType`

- Seconds: Numeric types that can be cast to `DecimalType(16, 6)`

## Algorithm

- Accepts three input parameters representing time components

- Delegates the actual time construction to `DateTimeUtils.makeTime` method via `StaticInvoke`

- Uses `DecimalType(16, 6)` for seconds to preserve microsecond precision without losing fractional components

- Performs implicit casting of inputs to match the required types (`IntegerType`, `IntegerType`, `DecimalType(16, 6)`)

- Returns a time value with microsecond-level precision

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require shuffle operations

- Can be evaluated independently per partition

- Does not affect data distribution or partitioning scheme

## Edge Cases

- **Null handling**: If any input parameter is NULL, the result is NULL

- **Invalid time components**: Behavior depends on the underlying `DateTimeUtils.makeTime` implementation for out-of-range values

- **Precision handling**: The `DecimalType(16, 6)` ensures microsecond precision is maintained for the seconds component

- **Type casting**: Integer seconds values are safely cast to decimal without precision loss due to the wide decimal type used

## Code Generation
This expression uses `StaticInvoke` for code generation, which means it generates efficient bytecode that directly calls the `DateTimeUtils.makeTime` method rather than using interpreted evaluation.

## Examples
```sql
-- Create a time for 14:30:45.123456
SELECT make_time(14, 30, 45.123456);

-- Create midnight
SELECT make_time(0, 0, 0);

-- Create a time with microsecond precision
SELECT make_time(23, 59, 59.999999);
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("make_time(14, 30, 45.123456)"))

// Using column references
df.select(expr("make_time(hour_col, minute_col, second_col)"))
```

## See Also

- `MakeDate` - Creates date values from components

- `MakeTimestamp` - Creates timestamp values from date and time components

- Time extraction functions like `hour()`, `minute()`, `second()`