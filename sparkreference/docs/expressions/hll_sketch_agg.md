# HllSketchAgg

## Overview

HllSketchAgg is an aggregate expression that creates HyperLogLog (HLL) sketches for approximate distinct counting. It uses the DataSketches library to maintain a probabilistic data structure that can estimate cardinality with configurable precision, making it efficient for large-scale distinct count operations.

## Syntax

```sql
hll_sketch_agg(column [, lgConfigK])
```

```scala
// DataFrame API
df.agg(expr("hll_sketch_agg(column, lgConfigK)"))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| column | IntegerType, LongType, StringType, BinaryType | The column or expression to create the HLL sketch from |
| lgConfigK | IntegerType | Optional. Log base 2 of the number of buckets (determines sketch precision). Defaults to HllSketch.DEFAULT_LG_K |

## Return Type

BinaryType - Returns a serialized HLL sketch as a byte array that can be stored, transmitted, or further processed.

## Supported Data Types

- IntegerType
- LongType  
- StringType (with collation support, trimming collations supported)
- BinaryType

Note: Floating point types are explicitly not supported due to precision issues. Array types and complex types are not implemented.

## Algorithm

- Creates an HLL sketch with configurable precision based on lgConfigK parameter
- Uses HLL_8 target type (8-bit registers) for memory efficiency
- Updates the sketch by hashing input values and updating corresponding buckets
- Merges sketches using Union operations during shuffle phases
- Serializes final sketch to updatable byte array format for storage

## Partitioning Behavior

How this expression affects partitioning:

- Does not preserve partitioning (this is an aggregate function)
- Requires shuffle operation to merge partial sketches from different partitions
- Uses Union-based merging to combine sketches across partitions

## Edge Cases

- Null values are ignored and do not contribute to the sketch
- Empty byte arrays are ignored during updates
- Strings that are collation-equal to empty string are ignored
- Non-constant lgConfigK parameter throws QueryExecutionError
- Unsupported data types throw SparkUnsupportedOperationException with error class "_LEGACY_ERROR_TEMP_3121"
- The expression is marked as non-nullable (always returns a result)

## Code Generation

This expression does not support Tungsten code generation and falls back to interpreted mode, as it extends TypedImperativeAggregate which uses imperative buffer management rather than code-generated aggregation.

## Examples

```sql
-- Basic HLL sketch with default precision
SELECT hll_sketch_agg(user_id) FROM events;

-- HLL sketch with custom precision (lgConfigK = 12)
SELECT hll_sketch_agg(user_id, 12) FROM events GROUP BY date;

-- Using with string data
SELECT hll_sketch_agg(email_domain, 10) FROM users;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Default precision
df.agg(expr("hll_sketch_agg(user_id)"))

// Custom precision
df.groupBy("category").agg(expr("hll_sketch_agg(product_id, 14)"))

// With binary data
df.select(expr("hll_sketch_agg(binary_column, 8)"))
```

## See Also

- HyperLogLog algorithm documentation
- DataSketches library HllSketch class
- Other approximate aggregation functions in Spark
- Union operations for sketch merging