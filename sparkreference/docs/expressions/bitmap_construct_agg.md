# BitmapConstructAgg

## Overview
BitmapConstructAgg is an imperative aggregate function that constructs a bitmap by setting bits at positions specified by input long values. It accumulates multiple bit positions into a single binary bitmap structure during aggregation.

## Syntax
```sql
bitmap_construct_agg(position)
```

```scala
// DataFrame API
df.agg(expr("bitmap_construct_agg(position_column)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression (Long) | The bit position to set in the bitmap (must evaluate to LongType) |
| mutableAggBufferOffset | Int | Offset for mutable aggregation buffer (internal) |
| inputAggBufferOffset | Int | Offset for input aggregation buffer (internal) |

## Return Type
BinaryType - Returns a fixed-size binary array representing the constructed bitmap.

## Supported Data Types

- Input: LongType only (implicit casting supported via ImplicitCastInputTypes)
- Output: BinaryType (binary array)

## Algorithm

- Initializes a fixed-size binary buffer filled with zeros using `BitmapExpressionUtils.NUM_BYTES`
- For each input position, validates the bit position is within valid range (0 to 8 * bitmap.length - 1)
- Calculates byte position using integer division (position / 8) and bit offset using modulo (position % 8)
- Sets the corresponding bit using bitwise OR operation: `bitmap(bytePosition) | (1 << bit)`
- Merges bitmaps during aggregation using `BitmapExpressionUtils.bitmapMerge`

## Partitioning Behavior
This expression affects partitioning as follows:

- Does not preserve partitioning due to aggregation nature
- Requires shuffle for global aggregation across partitions
- Partial aggregation can occur within partitions before shuffle

## Edge Cases

- Null handling: Null input positions are ignored (skipped without error)
- Empty input: Returns a bitmap filled with all zeros as the default result
- Invalid positions: Throws `QueryExecutionErrors.invalidBitmapPositionError` for positions < 0 or >= (8 * bitmap.length)
- Buffer overflow: Fixed-size bitmap prevents dynamic expansion beyond `BitmapExpressionUtils.NUM_BYTES`

## Code Generation
This expression uses interpreted mode execution as it extends ImperativeAggregate, which does not support Tungsten code generation. All operations fall back to the eval() method implementation.

## Examples
```sql
-- Construct bitmap from user IDs
SELECT bitmap_construct_agg(user_id) FROM events GROUP BY session_id;

-- Create bitmap of active days (0-6 for week days)
SELECT bitmap_construct_agg(day_of_week) FROM user_activity GROUP BY user_id;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Construct bitmap of product categories
df.groupBy("store_id")
  .agg(expr("bitmap_construct_agg(category_id)").alias("category_bitmap"))

// Create user activity bitmap
userEvents.groupBy("user_id")
  .agg(expr("bitmap_construct_agg(event_type_id)").alias("activity_bitmap"))
```

## See Also

- BitmapExpressionUtils.bitmapMerge - Used internally for merging bitmaps
- Other bitmap-related expressions in the bitmap functions group
- ImperativeAggregate - Base class for aggregation expressions