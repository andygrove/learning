# BitmapOrAgg

## Overview
BitmapOrAgg is an imperative aggregate function that performs a bitwise OR operation across multiple bitmap values. It combines binary-encoded bitmaps by merging them using bitwise OR logic, producing a single bitmap that represents the union of all input bitmaps.

## Syntax
```sql
bitmap_or_agg(bitmap_column)
```

```scala
// DataFrame API
df.agg(expr("bitmap_or_agg(bitmap_column)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Binary | A binary expression representing a bitmap to be aggregated |

## Return Type
`BinaryType` - Returns a binary array representing the merged bitmap result.

## Supported Data Types

- **Input**: `BinaryType` only
- **Output**: `BinaryType`

The expression strictly requires binary input and will fail type checking for any other data type.

## Algorithm

- Initializes an aggregation buffer with a fixed-size binary array filled with zeros
- For each input bitmap, performs bitwise OR merge with the current buffer using `BitmapExpressionUtils.bitmapMerge`
- During merge operations, combines two bitmap buffers using the same bitwise OR logic
- Returns the final merged bitmap from the aggregation buffer
- Uses a fixed bitmap size defined by `BitmapExpressionUtils.NUM_BYTES`

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve partitioning as it's an aggregate function that reduces multiple rows to a single result
- Requires shuffle operation for distributed aggregation across partitions
- Each partition computes partial bitmap aggregates that are then merged in the final aggregation phase

## Edge Cases

- **Null handling**: Null input bitmaps are skipped during aggregation without affecting the result
- **Empty input**: Returns a zero-filled bitmap of fixed size (`BitmapExpressionUtils.NUM_BYTES`)
- **Non-nullable result**: The expression always returns a non-null binary result, even with all-null inputs
- **Fixed size constraint**: All bitmaps must conform to the predefined size specified by `BitmapExpressionUtils.NUM_BYTES`

## Code Generation
This expression uses interpreted mode execution as it extends `ImperativeAggregate`. It does not support Tungsten code generation due to its imperative nature and complex bitmap manipulation logic that requires custom utility functions.

## Examples
```sql
-- Aggregate bitmaps representing user activity across different days
SELECT bitmap_or_agg(daily_activity_bitmap) as combined_activity
FROM user_activity_logs
WHERE user_id = 12345;

-- Combine department-level access permissions
SELECT dept_name, bitmap_or_agg(permission_bitmap) as dept_permissions
FROM employee_permissions
GROUP BY dept_name;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Aggregate bitmaps for user segments
df.groupBy("segment_id")
  .agg(expr("bitmap_or_agg(user_bitmap)").alias("segment_users"))

// Combine feature flags across environments
df.agg(expr("bitmap_or_agg(feature_flags)").alias("all_features"))
```

## See Also

- `BitmapAndAgg` - Bitwise AND aggregation for bitmaps
- `BitmapXorAgg` - Bitwise XOR aggregation for bitmaps
- `BitmapExpressionUtils` - Utility functions for bitmap operations