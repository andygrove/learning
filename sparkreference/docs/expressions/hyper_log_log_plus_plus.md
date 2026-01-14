# HyperLogLogPlusPlus

## Overview
HyperLogLogPlusPlus implements the HyperLogLog++ algorithm for approximate distinct counting in Spark SQL. It provides a memory-efficient way to estimate the number of distinct values in a dataset with configurable accuracy, making it suitable for large-scale data processing where exact distinct counts would be prohibitively expensive.

## Syntax
```sql
approx_count_distinct(column [, relativeSD])
```

```scala
// DataFrame API
df.agg(approx_count_distinct(col("column_name")))
df.agg(approx_count_distinct(col("column_name"), lit(0.02)))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The column or expression to count distinct values for |
| relativeSD | Double | Relative standard deviation controlling accuracy (default: 0.05, meaning ~5% error) |
| mutableAggBufferOffset | Int | Internal offset for mutable aggregation buffer (default: 0) |
| inputAggBufferOffset | Int | Internal offset for input aggregation buffer (default: 0) |

## Return Type
`LongType` - Returns a long integer representing the estimated count of distinct values.

## Supported Data Types
Supports all Spark SQL data types as input:

- Numeric types (IntegerType, LongType, DoubleType, DecimalType, etc.)
- String types (StringType)
- Binary types (BinaryType)
- Date and timestamp types
- Complex types (ArrayType, MapType, StructType)

## Algorithm
The expression uses the HyperLogLog++ algorithm with the following key steps:

- Hash input values and extract leading zeros plus additional bits for register assignment
- Maintain an array of registers (stored as long words) to track maximum leading zero counts
- Use bias correction and interpolation techniques specific to HyperLogLog++ for improved accuracy
- Apply cardinality estimation formula during final evaluation phase
- Merge operations combine registers by taking maximum values across corresponding positions

## Partitioning Behavior
This expression affects partitioning as follows:
- Does not preserve partitioning (requires global aggregation)
- Requires shuffle operation to combine partial results from all partitions
- Implements proper merge logic to combine HyperLogLog++ sketches from different partitions

## Edge Cases

- Null values are ignored and do not contribute to the distinct count estimation
- Empty input datasets return 0 as the default result
- Very small datasets (< 40 distinct values) may use linear counting for better accuracy
- Maximum estimation capacity depends on the precision parameter derived from relativeSD
- Duplicate values within the same partition are handled correctly by the probabilistic data structure

## Code Generation
This expression does not support Tungsten code generation and falls back to interpreted mode. The implementation uses `ImperativeAggregate`, which operates through interpreted `update`, `merge`, and `eval` methods rather than generated code.

## Examples
```sql
-- Basic usage
SELECT approx_count_distinct(user_id) FROM user_events;

-- With custom accuracy (2% relative standard deviation)
SELECT approx_count_distinct(product_id, 0.02) FROM sales;

-- Example from source code documentation
SELECT approx_count_distinct(col1) FROM VALUES (1), (1), (2), (2), (3) tab(col1);
-- Returns: 3
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic distinct count estimation
df.agg(approx_count_distinct(col("user_id"))).show()

// Higher precision estimation
df.agg(approx_count_distinct(col("session_id"), lit(0.01))).show()

// Multiple columns
df.groupBy("category")
  .agg(approx_count_distinct(col("product_id")).alias("distinct_products"))
  .show()
```

## See Also

- `count(DISTINCT column)` - Exact distinct count (more expensive)
- `HyperLogLogPlusPlusHelper` - Internal helper class implementing the algorithm
- `ImperativeAggregate` - Base class for aggregation functions
- `approx_percentile` - Another approximate aggregation function