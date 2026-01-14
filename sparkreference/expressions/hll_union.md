# HllUnion

## Overview
The `HllUnion` expression merges two HyperLogLog (HLL) sketches into a single unified sketch. This function is used to combine cardinality estimation sketches from different data sources or partitions, enabling distributed approximate distinct counting operations.

## Syntax
```sql
hll_union(sketch1, sketch2, allow_different_lg_k)
hll_union(sketch1, sketch2)  -- allow_different_lg_k defaults to false
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `sketch1` | BinaryType | First HLL sketch as binary data |
| `sketch2` | BinaryType | Second HLL sketch as binary data |
| `allow_different_lg_k` | BooleanType | Optional. Whether to allow union of sketches with different log configuration K values. Defaults to `false` |

## Return Type
Returns `BinaryType` - a binary representation of the unified HLL sketch.

## Supported Data Types
- **Input sketches**: Binary data containing serialized HLL sketches
- **Configuration flag**: Boolean values only

## Algorithm
- Deserializes both input binary arrays into HLL sketch objects using Apache DataSketches library
- Validates sketch buffer format and throws errors for invalid sketches
- Checks log configuration K compatibility between sketches if `allow_different_lg_k` is false
- Creates a Union object with the minimum log configuration K from both sketches
- Updates the union with both sketches sequentially
- Returns the result as an updatable byte array with target type HLL_8

## Partitioning Behavior
- **Preserves partitioning**: No, this is a data transformation operation
- **Requires shuffle**: No direct shuffle requirement, but typically used in aggregation contexts that may require shuffling
- The expression itself is stateless and can be evaluated on any partition

## Edge Cases
- **Null handling**: Expression is null-intolerant; returns null if any input is null
- **Invalid sketch buffers**: Throws `QueryExecutionErrors.hllInvalidInputSketchBuffer` for corrupted or invalid binary data
- **Mismatched configurations**: Throws `QueryExecutionErrors.hllUnionDifferentLgK` when sketches have different log K values and `allow_different_lg_k` is false
- **Memory errors**: Catches and re-throws Java errors during sketch deserialization as query execution errors

## Code Generation
This expression uses **CodegenFallback**, meaning it does not support Tungsten code generation and falls back to interpreted evaluation mode for all operations.

## Examples
```sql
-- Union two HLL sketches with same configuration
SELECT hll_union(sketch_col1, sketch_col2) FROM table1;

-- Union sketches allowing different log K configurations  
SELECT hll_union(sketch_a, sketch_b, true) FROM sketches_table;

-- Typical aggregation pattern
SELECT hll_union(hll_sketch) FROM (
  SELECT hll_sketch(user_id) as hll_sketch FROM events GROUP BY partition_id
);
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("hll_union(sketch1, sketch2)"))
df.select(expr("hll_union(sketch1, sketch2, true)"))
```

## See Also
- `hll_sketch` - for creating HLL sketches from raw data
- `hll_sketch_estimate` - for extracting cardinality estimates from HLL sketches
- Other DataSketches expressions for approximate analytics