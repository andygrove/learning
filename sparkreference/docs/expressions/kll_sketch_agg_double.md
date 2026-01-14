# KllSketchAggDouble

## Overview
`KllSketchAggDouble` is a Spark Catalyst expression that implements a KLL (Kurtosis, Log-scale, and Logarithmic) sketch aggregation function for double-precision floating-point data. This aggregate function creates a compact probabilistic data structure that enables efficient approximate quantile computation and statistical analysis on large datasets. The expression extends `TypedImperativeAggregate` and produces a serialized byte array representation of the KLL sketch.

## Syntax
```sql
kll_sketch_agg_double(column_expr [, k_value])
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `child` | Expression | The input column or expression containing Float or Double values to be sketched |
| `kExpr` | Optional[Expression] | Optional integer parameter controlling sketch accuracy and size (higher k = better accuracy) |
| `mutableAggBufferOffset` | Int | Internal offset for mutable aggregation buffer (default: 0) |
| `inputAggBufferOffset` | Int | Internal offset for input aggregation buffer (default: 0) |

## Return Type
`BinaryType` - Returns a byte array containing the serialized KLL sketch data structure.

## Supported Data Types

- `FloatType` - 32-bit floating-point numbers (converted to double internally)
- `DoubleType` - 64-bit floating-point numbers

Note: Integer types are not supported to avoid precision loss during conversion. Use `kll_sketch_agg_bigint` for integer data types.

## Algorithm

- Creates a `KllDoublesSketch` instance with the specified k parameter controlling accuracy
- Processes input rows by evaluating the child expression and updating the sketch with non-null values
- Handles Float inputs by converting them to Double precision before sketch updates
- Merges multiple sketch instances during distributed aggregation phases
- Serializes the final sketch into a compact byte array representation for storage and transmission

## Partitioning Behavior
This expression affects partitioning behavior as follows:
- Does not preserve partitioning as it is an aggregate function that combines data across partitions
- Requires shuffle operations during the merge phase to combine partial sketches from different partitions

## Edge Cases

- **Null handling**: Null values are explicitly ignored and do not update the sketch
- **Empty input**: Returns an empty sketch buffer when no valid input values are processed
- **Invalid sketch merging**: Throws `QueryExecutionErrors.kllInvalidInputSketchBuffer` when sketch merge operations fail
- **Deserialization errors**: Throws `QueryExecutionErrors.kllInvalidInputSketchBuffer` when attempting to deserialize corrupted sketch data
- **Unsupported data types**: Throws `unexpectedInputDataTypeError` if input data types other than Float/Double are encountered

## Code Generation
This expression does not support Tungsten code generation and operates in interpreted mode. It extends `TypedImperativeAggregate` which uses imperative-style aggregation buffer management rather than code-generated evaluation paths.

## Examples
```sql
-- Basic usage with double column
SELECT kll_sketch_agg_double(price) FROM sales_data;

-- With custom k parameter for higher accuracy
SELECT kll_sketch_agg_double(revenue, 256) FROM financial_data;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic sketch aggregation
df.agg(expr("kll_sketch_agg_double(amount)"))

// With custom k parameter
df.agg(expr("kll_sketch_agg_double(value, 512)"))
```

## See Also

- `kll_sketch_agg_bigint` - KLL sketch aggregation for integer types
- Standard quantile functions like `percentile_approx`
- Other probabilistic data structure functions in Spark SQL