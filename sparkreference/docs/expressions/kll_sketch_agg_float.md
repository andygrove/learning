# KllSketchAggFloat

## Overview
KllSketchAggFloat is a typed imperative aggregate function that builds a KLL (K, L, L) sketch from float values. It creates a compact probabilistic data structure that can be used for approximate quantile calculations and percentile estimations on streaming or large datasets.

## Syntax
```sql
kll_sketch_agg_float(column [, k])
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| column | FloatType | The float column or expression to build the sketch from |
| k | IntegerType (optional) | The accuracy parameter controlling sketch size and precision (defaults to implementation-defined value) |

## Return Type
BinaryType - Returns a serialized byte array representation of the KLL sketch.

## Supported Data Types

- FloatType only - Integer types are explicitly not supported to avoid precision loss from integer-to-float conversion
- Users should use `kll_sketch_agg_bigint` for integer types

## Algorithm

- Creates a heap-based KllFloatsSketch instance with the specified k parameter
- Iterates through input rows, updating the sketch with each non-null float value
- Ignores null values during aggregation without affecting the sketch
- Merges multiple sketch instances during distributed computation phases
- Serializes the final sketch into a compact byte array format

## Partitioning Behavior
This expression requires data shuffling for final aggregation:

- Does not preserve input partitioning due to its aggregate nature
- Requires shuffle operation to merge partial sketches from different partitions
- Uses custom merge logic to combine KllFloatsSketch instances across executors

## Edge Cases

- Null values are completely ignored and do not affect the sketch construction
- Empty input results in an empty sketch buffer created via `createAggregationBuffer()`
- Invalid sketch buffers during merge operations throw `QueryExecutionErrors.kllInvalidInputSketchBuffer`
- Deserialization failures from corrupted byte arrays are caught and converted to error exceptions
- The function is marked as non-nullable, always returning a valid byte array

## Code Generation
This expression does not support Tungsten code generation and falls back to interpreted mode, as it extends `TypedImperativeAggregate` which requires custom object manipulation for the KLL sketch state.

## Examples
```sql
-- Basic usage with default k parameter
SELECT kll_sketch_agg_float(price) FROM sales;

-- Usage with custom accuracy parameter
SELECT kll_sketch_agg_float(temperature, 256) FROM weather_data;
```

```scala
// DataFrame API usage with default k
df.agg(expr("kll_sketch_agg_float(price)"))

// DataFrame API usage with custom k parameter  
df.agg(expr("kll_sketch_agg_float(temperature, 256)"))
```

## See Also

- `kll_sketch_agg_bigint` - KLL sketch aggregation for integer types
- Other quantile and percentile functions for exact calculations
- Histogram functions for alternative approximate summaries