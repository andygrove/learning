# BitmapAndAgg

## Overview
BitmapAndAgg is an imperative aggregate function that performs a bitwise AND operation across multiple bitmap values. It combines binary bitmap representations by performing element-wise AND operations on all input bitmaps, effectively computing the intersection of bits across all aggregated values.

## Syntax
```sql
SELECT bitmap_and_agg(bitmap_column) FROM table_name;
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The bitmap expression to aggregate, must evaluate to binary data |
| mutableAggBufferOffset | Int | Internal offset for mutable aggregation buffer (default: 0) |
| inputAggBufferOffset | Int | Internal offset for input aggregation buffer (default: 0) |

## Return Type
`BinaryType` - Returns a fixed-size binary array representing the aggregated bitmap.

## Supported Data Types

- **Input**: `BinaryType` only - the expression strictly validates that the child expression returns binary data
- **Output**: `BinaryType` - fixed-size binary array

## Algorithm

- Initialize aggregation buffer with all bits set to 1 (filled with -1 bytes)
- For each input bitmap, perform bitwise AND operation between current buffer and input
- Merge partial aggregates by performing bitwise AND between buffer contents
- Null input values are skipped during aggregation
- Final result is the accumulated bitmap buffer

## Partitioning Behavior
As an aggregate function, BitmapAndAgg has the following partitioning characteristics:

- Does not preserve input partitioning
- Requires shuffle for global aggregation across partitions
- Supports partial aggregation with merge capability for distributed processing

## Edge Cases

- **Null handling**: Null input bitmaps are ignored and do not affect the aggregation result
- **Empty input**: Returns a bitmap with all bits set to 1 (default result of all -1 bytes)
- **Non-nullable result**: The function always returns a non-null bitmap result
- **Fixed size**: All bitmaps must conform to `BitmapExpressionUtils.NUM_BYTES` size requirement
- **Type validation**: Throws `DataTypeMismatch` error if input is not BinaryType

## Code Generation
This expression does not support code generation and operates in interpreted mode only, as it extends `ImperativeAggregate` which uses the imperative aggregation framework rather than Tungsten code generation.

## Examples
```sql
-- Aggregate bitmap intersection across user groups
SELECT bitmap_and_agg(user_permissions_bitmap) 
FROM user_groups 
WHERE group_type = 'admin';
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("bitmap_and_agg(permission_bitmap)"))
  .collect()
```

## See Also

- `BitmapOrAgg` - Bitwise OR aggregation for bitmap union operations
- `BitmapXorAgg` - Bitwise XOR aggregation for bitmap difference operations
- Other bitmap manipulation expressions in the bitmap expression family