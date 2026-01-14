# KllSketchAggBigint

## Overview
`KllSketchAggBigint` is a typed imperative aggregate function that builds KLL (K-Linear-Linear) sketches for approximate quantile computation on integer-like data types. It creates a compact probabilistic data structure that can efficiently estimate quantiles, ranks, and histograms from large datasets with configurable accuracy guarantees.

## Syntax
```sql
kll_sketch_agg_bigint(expression [, k])
```

```scala
// DataFrame API
df.agg(expr("kll_sketch_agg_bigint(column_name)"))
df.agg(expr("kll_sketch_agg_bigint(column_name, 200)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expression | Byte, Short, Int, Long | The column or expression to build the sketch from |
| k | Int (optional) | The sketch accuracy parameter controlling memory usage and precision |

## Return Type
`BinaryType` - Returns a serialized byte array representation of the KLL sketch that can be stored or transmitted.

## Supported Data Types

- `ByteType` - converted to Long internally
- `ShortType` - converted to Long internally  
- `IntegerType` - converted to Long internally
- `LongType` - used directly

## Algorithm

- Creates a heap-based KllLongsSketch instance with the specified k parameter for accuracy control
- Processes input rows by evaluating the child expression and updating the sketch with non-null values
- Converts all supported numeric types to Long before sketch update operations
- Supports merging multiple sketch instances during distributed aggregation phases
- Serializes the final sketch state to a compact byte array format for storage and transmission

## Partitioning Behavior
This expression affects partitioning as follows:

- Does not preserve input partitioning due to its aggregate nature
- Requires shuffle operations during the aggregation phase to combine partial sketches
- Supports partial aggregation with merge operations for distributed computation

## Edge Cases

- Null values are completely ignored and do not affect the sketch state
- Empty input results in an empty sketch buffer rather than null
- Invalid sketch data during deserialization throws QueryExecutionErrors.kllInvalidInputSketchBuffer
- Merge failures with incompatible sketches throw QueryExecutionErrors.kllInvalidInputSketchBuffer
- Unsupported input data types throw unexpectedInputDataTypeError

## Code Generation
This expression does not support Tungsten code generation and falls back to interpreted mode due to its TypedImperativeAggregate base class, which requires complex object state management that cannot be easily code-generated.

## Examples
```sql
-- Build a sketch from integer column with default k parameter
SELECT kll_sketch_agg_bigint(user_id) FROM users;

-- Build a sketch with custom accuracy parameter
SELECT kll_sketch_agg_bigint(transaction_amount, 400) FROM transactions;

-- Group by aggregation
SELECT region, kll_sketch_agg_bigint(sales_amount) 
FROM sales 
GROUP BY region;
```

```scala
// DataFrame API usage with default parameters
import org.apache.spark.sql.functions._
df.agg(expr("kll_sketch_agg_bigint(amount)"))

// With custom k parameter
df.select(expr("kll_sketch_agg_bigint(user_id, 256)"))

// Grouped aggregation
df.groupBy("category")
  .agg(expr("kll_sketch_agg_bigint(price)").as("price_sketch"))
```

## See Also

- `kll_sketch_agg_double` - KLL sketch aggregation for floating-point types
- `percentile_approx` - Alternative approximate quantile function
- Other sketch-based aggregate functions for cardinality estimation