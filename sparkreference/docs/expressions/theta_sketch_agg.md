# ThetaSketchAgg

## Overview
ThetaSketchAgg is a Spark SQL aggregate function that creates a Theta sketch for approximate distinct counting and set operations. It builds a probabilistic data structure that can estimate cardinality with configurable accuracy while using fixed memory space.

## Syntax
```sql
theta_sketch_agg(column [, lg_nom_entries])
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| column | Various | The input column or expression to sketch (supports multiple data types) |
| lg_nom_entries | Integer | Optional. Log base-2 of nominal entries (default: 12). Controls sketch accuracy and memory usage |

## Return Type
Returns `BinaryType` - a serialized compact Theta sketch as a byte array.

## Supported Data Types

- `IntegerType` (promoted to Long)
- `LongType` 
- `FloatType` (promoted to Double)
- `DoubleType`
- `StringType` (with collation support)
- `BinaryType`
- `ArrayType(IntegerType)`
- `ArrayType(LongType)`

## Algorithm

- Creates an UpdateSketch with configurable nominal entries parameter
- Updates the sketch with input values, handling type-specific conversions
- Merges partial sketches using Union operations when combining partitions
- Uses lazy Union creation for efficient merging across partitions
- Serializes final result as a compact binary sketch

## Partitioning Behavior
How this expression affects partitioning:

- Requires shuffle for final aggregation across partitions
- Does not preserve input partitioning
- Creates partial sketches per partition, then merges during shuffle phase

## Edge Cases

- Null values are ignored and do not update the sketch
- Empty byte arrays are ignored
- Empty arrays of supported element types are ignored  
- Strings that are collation-equal to empty string are ignored
- Invalid lg_nom_entries values throw QueryExecutionErrors
- Non-constant lg_nom_entries expressions are rejected
- Unsupported data types throw SparkUnsupportedOperationException

## Code Generation
This expression does not support Tungsten code generation and falls back to interpreted mode, as it extends TypedImperativeAggregate which requires custom object handling.

## Examples
```sql
-- Basic usage with default parameters
SELECT theta_sketch_agg(user_id) FROM events;

-- With custom nominal entries for higher accuracy
SELECT theta_sketch_agg(user_id, 14) FROM events;

-- Sketching string values
SELECT theta_sketch_agg(email_domain) FROM users;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.agg(expr("theta_sketch_agg(user_id)"))

// With custom parameters  
df.agg(expr("theta_sketch_agg(user_id, 16)"))
```

## See Also

- `theta_sketch_estimate` - Extract cardinality estimate from Theta sketch
- `theta_sketch_union` - Union multiple Theta sketches
- `approx_count_distinct` - Alternative approximate distinct counting