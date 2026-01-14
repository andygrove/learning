# TimeWindow

## Overview
TimeWindow is a Spark Catalyst expression that creates time-based windows for streaming and batch data processing. It transforms timestamp columns into window structures with start and end times, enabling time-based grouping and aggregation operations.

## Syntax
```sql
window(timeColumn, windowDuration, slideDuration, startTime)
window(timeColumn, windowDuration, slideDuration)
window(timeColumn, windowDuration)
```

```scala
// DataFrame API
df.select(window($"timestamp", "10 minutes", "5 minutes"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| timeColumn | Expression | The timestamp column to create windows from |
| windowDuration | Long/Expression | Length of each window in microseconds |
| slideDuration | Long/Expression | Slide interval between windows in microseconds (defaults to windowDuration) |
| startTime | Long/Expression | Offset for window start time in microseconds (defaults to 0) |

## Return Type
Returns a StructType with two fields:

- `start`: TimestampType or TimestampNTZType (matches input column type)
- `end`: TimestampType or TimestampNTZType (matches input column type)

## Supported Data Types
The time column supports:

- TimestampType
- TimestampNTZType  
- StructType with start/end timestamp fields (for nested window operations)

## Algorithm
The TimeWindow expression follows these evaluation principles:

- Creates sliding or tumbling windows based on duration and slide parameters
- Window boundaries are calculated using the startTime offset
- Each timestamp maps to one or more overlapping windows
- Window start/end times are computed deterministically for consistent results
- Expression is replaced during analysis phase (marked as Unevaluable)

## Partitioning Behavior
TimeWindow has the following partitioning characteristics:

- Preserves existing partitioning schemes
- Does not require data shuffling by itself
- Window boundaries are computed locally per partition
- Subsequent groupBy operations on windows may trigger shuffling

## Edge Cases

- Null timestamp values produce null window structures
- windowDuration must be positive (> 0), otherwise throws DataTypeMismatch error
- slideDuration must be positive (> 0), otherwise throws DataTypeMismatch error  
- slideDuration cannot exceed windowDuration, otherwise throws constraint violation
- Absolute startTime must be less than slideDuration, otherwise throws constraint violation
- Expression remains unresolved until analyzer replacement occurs

## Code Generation
This expression does not support code generation as it is marked as Unevaluable. The TimeWindow expression is replaced by the analyzer with concrete window generation logic before execution, so it never reaches the code generation phase.

## Examples
```sql
-- Tumbling 10-minute windows
SELECT window(timestamp, '10 minutes'), count(*)
FROM events
GROUP BY window(timestamp, '10 minutes')

-- Sliding 10-minute windows every 5 minutes  
SELECT window(timestamp, '10 minutes', '5 minutes'), avg(value)
FROM metrics
GROUP BY window(timestamp, '10 minutes', '5 minutes')
```

```scala
// DataFrame API - tumbling windows
df.groupBy(window($"timestamp", "10 minutes"))
  .count()

// DataFrame API - sliding windows with start offset
df.select(window($"timestamp", "1 hour", "30 minutes", "15 minutes"))
  .groupBy($"window")
  .avg("value")
```

## See Also

- SessionWindow - for session-based windowing
- UnaryExpression - parent expression type
- ImplicitCastInputTypes - for automatic type casting behavior