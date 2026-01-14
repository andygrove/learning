# CountMinSketchAgg

## Overview
CountMinSketchAgg is a Spark Catalyst expression that implements a Count-Min Sketch probabilistic data structure for approximate frequency counting. It builds a space-efficient sketch of the input data that can later be queried to estimate the frequency of any element with bounded error guarantees.

## Syntax
```sql
count_min_sketch(column, eps, confidence, seed)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| column | IntegralType, StringType, or BinaryType | The column values to add to the Count-Min Sketch |
| eps | DoubleType | Relative error parameter, must be positive (> 0.0) |
| confidence | DoubleType | Confidence parameter, must be positive and less than 1.0 (0.0 < confidence < 1.0) |
| seed | IntegerType or LongType | Random seed for hash functions |

## Return Type
BinaryType - Returns a serialized byte array representation of the Count-Min Sketch data structure.

## Supported Data Types

- **IntegralType**: All integer types (ByteType, ShortType, IntegerType, LongType)
- **StringType**: String values (optimized using UTF8String byte representation)
- **BinaryType**: Binary data

## Algorithm

- Creates a Count-Min Sketch with dimensions determined by the eps and confidence parameters
- For each non-null input value, adds it to the sketch using appropriate hash functions
- String values are optimized by directly using UTF8String bytes to avoid conversion overhead
- Multiple sketches can be merged using the mergeInPlace operation for distributed aggregation
- Final result is serialized to a byte array for storage and transmission

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning during the update phase as it processes rows locally
- Requires shuffle during the merge phase to combine sketches from different partitions
- The final sketch represents the global frequency estimates across all partitions

## Edge Cases

- **Null handling**: Null input values are ignored and not added to the sketch
- **Empty input**: Returns an empty Count-Min Sketch initialized with the specified parameters
- **Parameter validation**: All parameters (eps, confidence, seed) must be foldable (compile-time constants)
- **Range validation**: eps must be > 0.0, confidence must be in range (0.0, 1.0)
- **Seed conversion**: Long seed values are converted to Int using toInt

## Code Generation
This expression does not support Tungsten code generation and falls back to interpreted mode, as it extends TypedImperativeAggregate which uses interpreted evaluation for complex aggregation logic.

## Examples
```sql
-- Create a Count-Min Sketch for user_id column
SELECT count_min_sketch(user_id, 0.01, 0.99, 1) as sketch
FROM user_events;

-- Use in a GROUP BY aggregation
SELECT category, count_min_sketch(product_id, 0.05, 0.95, 42) as product_sketch  
FROM purchases
GROUP BY category;
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._

df.agg(expr("count_min_sketch(user_id, 0.01, 0.99, 1)").alias("sketch"))

// With column references
df.groupBy("category")
  .agg(expr("count_min_sketch(product_id, 0.05, 0.95, 42)").alias("product_sketch"))
```

## See Also

- **ApproximatePercentile**: Another probabilistic aggregation for quantile estimation
- **HyperLogLogPlusPlus**: Probabilistic cardinality estimation
- **BloomFilter**: Probabilistic membership testing