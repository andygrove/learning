# BitmapCount

## Overview
The `BitmapCount` expression counts the number of set bits (1s) in a binary bitmap representation. This function is designed to work with bitmap data structures stored as binary data, providing efficient cardinality counting for sets represented as bitmaps.

## Syntax
```sql
bitmap_count(bitmap_binary)
```

```scala
// DataFrame API
df.select(expr("bitmap_count(bitmap_column)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| bitmap_binary | BinaryType | The binary representation of a bitmap whose set bits should be counted |

## Return Type
Returns `LongType` - a 64-bit signed integer representing the count of set bits.

## Supported Data Types

- **Input**: Only `BinaryType` is supported
- **Output**: `LongType`

## Algorithm

- Validates that the input expression is of `BinaryType`, returning a type mismatch error for any other data type
- Delegates the actual bit counting operation to `BitmapExpressionUtils.bitmapCount()` method
- Uses `StaticInvoke` to call the utility method, indicating this is implemented as a runtime-replaceable expression
- The replacement expression is marked as non-nullable (`returnNullable = false`)
- Performs direct binary data processing to count set bits in the bitmap

## Partitioning Behavior
This expression preserves partitioning behavior since:

- It operates on individual rows without requiring data movement across partitions
- No shuffle operations are required as it's a deterministic function on single column values
- Each partition can independently process its bitmap data

## Edge Cases

- **Null input**: The expression handles null inputs according to standard Spark null propagation rules
- **Invalid binary format**: Behavior depends on the underlying `BitmapExpressionUtils.bitmapCount()` implementation
- **Empty binary data**: Will return 0 as there are no set bits to count
- **Large bitmaps**: Returns `LongType` which can handle counts up to 2^63-1, suitable for very large bitmaps

## Code Generation
This expression uses `RuntimeReplaceable` with `StaticInvoke`, which means:

- It does not generate direct bytecode but instead calls a static Java method
- Falls back to interpreted execution through the `BitmapExpressionUtils` utility class
- The static method invocation may be optimized by the JVM's JIT compiler during runtime

## Examples
```sql
-- Count bits in a bitmap column
SELECT bitmap_count(user_bitmap) FROM user_segments;

-- Use in aggregation context
SELECT segment_id, bitmap_count(combined_bitmap) as user_count 
FROM segment_bitmaps;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.expr

df.select(expr("bitmap_count(bitmap_column)").alias("bit_count"))

// With column reference
df.select(expr("bitmap_count(user_segments)"))
  .show()
```

## See Also

- Other bitmap-related expressions in the `misc_funcs` group
- `BitmapExpressionUtils` utility class for bitmap operations
- Binary data manipulation functions