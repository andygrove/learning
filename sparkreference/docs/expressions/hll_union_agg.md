# HllUnionAgg

## Overview
The `HllUnionAgg` expression implements a typed imperative aggregate function that merges multiple HyperLogLog (HLL) sketches using the Apache DataSketches library. It accepts binary-encoded HLL sketches and combines them into a single unified sketch for approximate set operations across partitions.

## Syntax
```sql
hll_union_agg(sketch_column)
hll_union_agg(sketch_column, allow_different_lg_config_k)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| sketch_column | BinaryType | Binary-encoded HLL sketch data to be merged |
| allow_different_lg_config_k | BooleanType | Optional flag to allow merging sketches with different lgConfigK values (default: false) |

## Return Type
Returns `BinaryType` - a binary-encoded HLL sketch representing the union of all input sketches.

## Supported Data Types

- Input sketches must be of `BinaryType` containing valid HLL sketch byte arrays
- Configuration parameter must be `BooleanType`

## Algorithm

- Defers Union instance creation until the first valid HLL sketch is processed
- Extracts lgConfigK from the first sketch to initialize the Union with matching configuration
- Validates lgConfigK compatibility between sketches based on the allowDifferentLgConfigK flag
- Updates the Union instance with each input HLL sketch using HLL_8 target type
- Serializes the final Union result as an updatable byte array

## Partitioning Behavior
This aggregate function requires data movement for final aggregation:

- Does not preserve partitioning as it needs to combine sketches across partitions
- Requires shuffle operations during the aggregation phase to merge partial results
- Uses imperative aggregation with custom serialization/deserialization for efficient data transfer

## Edge Cases

- Null sketch inputs are skipped without affecting the union result
- Invalid or corrupted sketch buffers throw `hllInvalidInputSketchBuffer` exceptions
- Mismatched lgConfigK values between sketches throw `hllUnionDifferentLgK` exceptions when allowDifferentLgConfigK is false
- Empty aggregation buffers return a new empty Union's byte array representation
- Zero-length byte arrays during deserialization return None for the Union option

## Code Generation
This expression does not support Tungsten code generation and operates in interpreted mode due to its imperative aggregate nature and complex state management with the DataSketches Union object.

## Examples
```sql
-- Basic HLL sketch union aggregation
SELECT hll_union_agg(hll_sketch_column) as merged_sketch
FROM sketches_table;

-- Allow merging sketches with different configurations
SELECT hll_union_agg(hll_sketch_column, true) as merged_sketch
FROM mixed_config_sketches;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("hll_union_agg(sketch_data)").as("union_result"))

// With configuration parameter
df.select(expr("hll_union_agg(sketch_data, true)").as("union_result"))
```

## See Also

- HLL sketch creation functions for generating input sketches
- Other DataSketches aggregate functions for probabilistic data structures
- Set aggregation functions for exact distinct counting operations