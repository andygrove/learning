# ApproxTopKAccumulate

## Overview
ApproxTopKAccumulate is an aggregate expression that efficiently computes the approximate top-K most frequent items in a dataset. It uses probabilistic data structures to maintain a compact representation of item frequencies while providing good approximation guarantees for the most frequent elements.

## Syntax
```sql
-- Used internally by approx_top_k aggregate function
SELECT approx_top_k(column_name, k, accuracy) FROM table_name
```

```scala
// DataFrame API usage
df.agg(expr("approx_top_k(column_name, k, accuracy)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression to find top-K items from |
| k | Integer | Number of top frequent items to return |
| accuracy | Integer | Accuracy parameter controlling memory usage and precision trade-off |

## Return Type
Returns an array of structs, where each struct contains:

- `item`: The frequent item (same type as input)
- `count`: Estimated frequency count (Long)

## Supported Data Types

- String types
- Numeric types (Integer, Long, Double, Float, etc.)
- Binary data
- Date and Timestamp types
- Any data type that can be serialized and compared

## Algorithm

- Uses Count-Min Sketch or similar probabilistic counting structure for frequency estimation
- Maintains a heap of top-K candidates based on estimated frequencies  
- Performs incremental updates during accumulation phase
- Merges partial results from different partitions during combine phase
- Provides approximate results with configurable accuracy guarantees

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve input partitioning as it requires global aggregation
- Requires shuffle operation to combine partial results across partitions
- Each partition maintains local top-K estimates that are merged globally
- Final merge operation determines global top-K from all partition results

## Edge Cases

- Null values are ignored during aggregation (not counted)
- Empty input returns an empty array
- When k exceeds total distinct items, returns all items with their counts
- Accuracy parameter must be positive; invalid values may cause exceptions
- Very low accuracy settings may produce highly approximate results
- Duplicate items across partitions are properly merged during combine phase

## Code Generation
This expression uses interpreted evaluation mode and does not support Tungsten code generation due to the complexity of the probabilistic data structures and dynamic memory allocation required for maintaining the top-K heap.

## Examples
```sql
-- Find top 5 most frequent products
SELECT approx_top_k(product_name, 5, 1000) as top_products
FROM sales_data;

-- Result format:
-- [{"item":"ProductA","count":1500},{"item":"ProductB","count":1200}]
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val topItems = df
  .agg(expr("approx_top_k(item_column, 10, 2000)").alias("frequent_items"))
  .collect()
```

## See Also

- `collect_list` - For exact collection of all values
- `count` - For exact counting
- `approx_count_distinct` - For approximate distinct counting
- Other approximate aggregate functions in the `agg_funcs` group