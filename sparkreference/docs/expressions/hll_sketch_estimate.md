# HllSketchEstimate

## Overview
The `HllSketchEstimate` expression extracts the cardinality estimate from a HyperLogLog (HLL) sketch binary representation. It takes a serialized HLL sketch as input and returns the estimated distinct count as a long integer, providing approximate cardinality estimation with high efficiency and low memory usage.

## Syntax
```sql
hll_sketch_estimate(sketch_binary)
```

```scala
// DataFrame API
df.select(expr("hll_sketch_estimate(hll_column)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| sketch_binary | BinaryType | Serialized HyperLogLog sketch as a byte array |

## Return Type
`LongType` - Returns the cardinality estimate as a long integer, rounded to the nearest whole number.

## Supported Data Types
- **Input**: `BinaryType` only - expects serialized HLL sketch data
- **Output**: `LongType` - estimated distinct count

## Algorithm
- Deserializes the input byte array using Apache DataSketches `HllSketch.heapify()` method
- Wraps the byte array in a `Memory` object for efficient processing
- Calls `getEstimate()` on the deserialized HLL sketch to obtain the cardinality estimate
- Rounds the floating-point estimate to the nearest long integer using `Math.round()`
- Throws `QueryExecutionErrors.hllInvalidInputSketchBuffer()` if deserialization fails due to invalid sketch data

## Partitioning Behavior
- **Preserves partitioning**: Yes, this is a deterministic function that operates row-by-row
- **Requires shuffle**: No, evaluation is local to each partition
- Can be pushed down to individual partitions without affecting correctness

## Edge Cases
- **Null handling**: Returns null if input is null (null-intolerant behavior)
- **Invalid sketch data**: Throws `QueryExecutionErrors.hllInvalidInputSketchBuffer` for corrupted or invalid binary data
- **Memory errors**: Catches `SketchesArgumentException` and `java.lang.Error` during deserialization
- **Empty sketches**: Valid empty HLL sketches return estimate of 0
- **Precision bounds**: Estimate accuracy depends on the original HLL sketch configuration parameters

## Code Generation
This expression uses **CodegenFallback**, meaning it does not support Tungsten code generation and falls back to interpreted evaluation mode. The `nullSafeEval` method is called directly during query execution.

## Examples
```sql
-- Estimate distinct count from HLL sketch
SELECT hll_sketch_estimate(hll_sketch_agg(col)) FROM VALUES (1), (1), (2), (2), (3) tab(col);
-- Result: 3

-- Use with pre-computed HLL sketches
SELECT customer_segment, hll_sketch_estimate(user_sketch) 
FROM customer_analytics 
WHERE date_partition = '2023-01-01';
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Estimate from aggregated sketch
df.select(expr("hll_sketch_estimate(hll_sketch_agg(user_id))"))

// Estimate from stored sketch column
df.select($"segment", expr("hll_sketch_estimate(stored_hll_sketch)"))
```

## See Also
- `HllSketchAgg` - Creates HLL sketches from input data
- `HllUnion` - Merges multiple HLL sketches
- `approx_count_distinct` - Alternative approximate cardinality function
- Apache DataSketches HLL implementation for algorithm details