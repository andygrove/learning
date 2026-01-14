# SessionWindow

## Overview
SessionWindow is a Catalyst expression that creates session-based time windows for grouping events. It groups consecutive events that occur within a specified gap duration into the same session window, where each session starts with the first event and extends until there's a gap longer than the specified duration.

## Syntax
```sql
session_window(time_column, gap_duration)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.groupBy(session_window($"timestamp", "10 minutes"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| timeColumn | Expression | The timestamp column or window struct to use for session windowing |
| gapDuration | Expression | The maximum gap duration between events in the same session |

## Return Type
Returns a struct type with two fields:
- `start`: Timestamp marking the beginning of the session window
- `end`: Timestamp marking the end of the session window

The timestamp type (TimestampType or TimestampNTZType) matches the input time column type.

## Supported Data Types

**Time Column:**
- TimestampType (timestamp with timezone)
- TimestampNTZType (timestamp without timezone)  
- Struct with start/end timestamp fields (from previous windowing operations)

**Gap Duration:**
- Any data type (AnyDataType) - typically string intervals like "10 minutes"

## Algorithm
The SessionWindow expression implements session-based windowing logic:

- Groups events into sessions where consecutive events are within the gap duration
- Creates a new session when the gap between events exceeds the specified duration
- Each session window spans from the first event timestamp to the last event timestamp in that session
- The expression is replaced during query analysis phase and doesn't perform direct evaluation
- Uses the Unevaluable trait indicating it's transformed before execution

## Partitioning Behavior
SessionWindow affects data partitioning behavior:

- Requires data to be ordered by timestamp within partitions for correct session detection
- May require shuffle operations to ensure proper temporal ordering
- Session boundaries are computed within each partition independently
- Does not preserve existing partitioning schemes due to temporal grouping requirements

## Edge Cases

**Null Handling:**
- The expression itself is marked as non-nullable (nullable = false)
- Null timestamp values would be handled by the underlying windowing implementation

**Resolution Behavior:**
- Always returns resolved = false as it's replaced during analysis phase
- Input time column may not be fully resolved when expression is created

**Window Chaining:**
- Supports chaining with other windowing operations through struct input types
- Can accept output from previous time_window or session_window operations

## Code Generation
This expression does not support code generation (Tungsten). It uses the Unevaluable trait, meaning:

- The expression is transformed/replaced during the analysis phase
- No direct bytecode generation occurs for this expression
- Falls back to the underlying session windowing implementation after transformation

## Examples

```sql
-- Group events into sessions with 30-minute gaps
SELECT session_window(timestamp, '30 minutes') as session, 
       count(*) as event_count
FROM events 
GROUP BY session_window(timestamp, '30 minutes')
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val sessionWindows = df
  .groupBy(session_window($"timestamp", "30 minutes"))
  .agg(count("*").as("event_count"))

// Chaining with existing window columns
val nestedWindows = df
  .groupBy(session_window($"existing_window", "1 hour"))
  .agg(sum("value"))
```

## See Also
- TimeWindow - for fixed-duration time windows
- Window functions - for sliding window operations  
- Tumbling/sliding window operations in structured streaming