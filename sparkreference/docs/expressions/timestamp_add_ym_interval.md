# TimestampAddYMInterval

## Overview
The `TimestampAddYMInterval` expression adds a year-month interval to a timestamp value. This operation is timezone-aware and handles both `TimestampType` and `TimestampNTZType` inputs while preserving the original timestamp data type.

## Syntax
```sql
timestamp_column + INTERVAL 'value' YEAR TO MONTH
```

```scala
// DataFrame API usage
col("timestamp_column") + expr("INTERVAL '2-3' YEAR TO MONTH")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| timestamp | Expression | The timestamp expression to add the interval to |
| interval | Expression | The year-month interval expression to add |
| timeZoneId | Option[String] | Optional timezone identifier for timezone-aware operations |

## Return Type
Returns the same data type as the input timestamp expression (`TimestampType` or `TimestampNTZType`).

## Supported Data Types

- Input timestamp: `AnyTimestampType` (`TimestampType` or `TimestampNTZType`)
- Input interval: `YearMonthIntervalType`

## Algorithm

- Extracts the timestamp value in microseconds and the interval value in months
- Determines the appropriate timezone using `zoneIdForType()` based on the timestamp data type
- Delegates to `DateTimeUtils.timestampAddMonths()` for the actual arithmetic
- Preserves the original timestamp data type in the result
- Handles timezone conversions when necessary for `TimestampType` inputs

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle
- Maintains existing partitioning scheme
- Can be applied within partition boundaries

## Edge Cases

- **Null handling**: Returns null if either timestamp or interval input is null (null intolerant)
- **Timezone handling**: Uses session timezone for `TimestampType` and UTC for `TimestampNTZType`
- **Month overflow**: Handles month arithmetic that crosses year boundaries correctly
- **Day adjustment**: May adjust day values when adding months to dates like January 31st + 1 month

## Code Generation
This expression supports Tungsten code generation and generates optimized Java code using `defineCodeGen()`. The generated code directly calls `DateTimeUtils.timestampAddMonths()` with the timezone reference for efficient execution.

## Examples
```sql
-- Add 2 years and 3 months to a timestamp
SELECT timestamp_col + INTERVAL '2-3' YEAR TO MONTH FROM events;

-- Add 1 year to current timestamp
SELECT current_timestamp() + INTERVAL '1' YEAR;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("created_at") + expr("INTERVAL '1-6' YEAR TO MONTH"))

// Using interval column
df.select(col("timestamp_col") + col("interval_col"))
```

## See Also

- `DateAddYMInterval` - Adds year-month intervals to date values
- `TimestampAddDTInterval` - Adds day-time intervals to timestamps
- `DateTimeUtils.timestampAddMonths()` - Underlying implementation method