# Sequence

## Overview
The Sequence expression generates an array of values from a start value to a stop value with an optional step increment. It supports integral types (byte, short, int, long), date, and timestamp data types with appropriate step types for each.

## Syntax
```sql
sequence(start, stop [, step])
```

```scala
// DataFrame API
sequence(start_col, stop_col)
sequence(start_col, stop_col, step_col)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| start | Expression | The starting value of the sequence |
| stop | Expression | The ending value of the sequence (inclusive) |
| step | Expression (optional) | The increment step; defaults to 1 for ascending sequences, -1 for descending |

## Return Type
Returns `ArrayType` with the same element type as the start/stop expressions and `containsNull = false`.

## Supported Data Types

- **Integral types**: `ByteType`, `ShortType`, `IntegerType`, `LongType`
  - Step must be of the same integral type
- **Timestamp types**: `TimestampType`, `TimestampNTZType`
  - Step can be `CalendarIntervalType`, `YearMonthIntervalType`, or `DayTimeIntervalType`
- **Date type**: `DateType`
  - Step can be `CalendarIntervalType`, `YearMonthIntervalType`, or `DayTimeIntervalType`

## Algorithm

- Validates that start and stop expressions have the same data type
- Determines appropriate step value based on data type and optional step parameter
- Uses specialized implementation classes based on element type:
  - `IntegralSequenceImpl` for integral types
  - `TemporalSequenceImpl` for date/timestamp with calendar intervals
  - `PeriodSequenceImpl` for date/timestamp with year-month intervals
  - `DurationSequenceImpl` for date/timestamp with day-time intervals
- Generates array elements by incrementing from start to stop by step amount

## Partitioning Behavior
This expression does not affect partitioning as it operates on individual row values:

- Preserves existing partitioning
- Does not require shuffle operations

## Edge Cases

- **Null handling**: Returns null if any input (start, stop, or step) is null
- **Empty sequences**: Generated when start > stop with positive step or start < stop with negative step
- **Default step behavior**: Automatically determines step as +1 or -1 based on start/stop relationship when step is omitted
- **Type coercion**: Non-interval expressions are cast to wider types when necessary for compatibility
- **Runtime errors**: May throw exceptions when step parameter creates invalid sequences (when `stepOpt.isDefined` and step constraints are violated)

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, generating optimized Java code for array creation and element population using `UnsafeArrayData.fromPrimitiveArray()`.

## Examples
```sql
-- Generate integer sequence
SELECT sequence(1, 5);
-- Result: [1, 2, 3, 4, 5]

-- Generate sequence with step
SELECT sequence(1, 10, 2);
-- Result: [1, 3, 5, 7, 9]

-- Generate date sequence
SELECT sequence(date '2018-01-01', date '2018-03-01', interval 1 month);
-- Result: [2018-01-01, 2018-02-01, 2018-03-01]
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(sequence(lit(1), lit(5)))
df.select(sequence(col("start_col"), col("end_col"), lit(2)))
df.select(sequence(lit(Date.valueOf("2018-01-01")), lit(Date.valueOf("2018-03-01"))))
```

## See Also

- Array functions: `array`, `array_contains`, `explode`
- Range generation: `range` (for DataFrames)
- Date/time functions: `date_add`, `date_sub`