# ApproxTopK

## Overview
ApproxTopK is an aggregate function that returns the approximate top-k most frequent items in a dataset along with their counts. It uses probabilistic data structures to efficiently compute the most frequent elements without requiring exact counts, making it suitable for large-scale data processing scenarios where memory efficiency is important.

## Syntax
```sql
approx_top_k(column, k)
```

```scala
df.agg(approx_top_k(col("column_name"), k))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| column | Any | The column containing items to find top-k frequencies for |
| k | Integer | The number of top frequent items to return |

## Return Type
Returns an array of structs, where each struct contains:

- `item`: The frequent item (same type as input column)
- `count`: The approximate count as Long

## Supported Data Types
Supports all data types that can be used as map keys:

- Numeric types (Integer, Long, Double, Float, etc.)
- String types
- Binary types  
- Date and Timestamp types
- Boolean types
- Complex types that are hashable

## Algorithm

- Uses a probabilistic counting algorithm (likely Count-Min Sketch or similar) to track item frequencies
- Maintains approximate counts in memory-efficient data structures
- Periodically updates the top-k candidates based on estimated frequencies
- Merges partial results from different partitions to produce final top-k list
- Returns results sorted by count in descending order

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve partitioning as it requires global aggregation
- Requires shuffle operation to merge partial top-k results across partitions
- Final stage combines all partial results to determine global top-k items

## Edge Cases

- Null values are typically ignored in the frequency counting
- Empty input returns an empty array
- If k is larger than the number of distinct items, returns all items with their counts
- Duplicate items in the same partition are counted appropriately
- Very large k values may impact memory usage and performance

## Code Generation
This expression likely falls back to interpreted mode due to the complexity of the probabilistic data structures and aggregation logic. The stateful nature of approximate counting algorithms makes them unsuitable for simple code generation optimizations.

## Examples
```sql
-- Find top 5 most frequent products
SELECT approx_top_k(product_name, 5) as top_products
FROM sales_data;

-- Result example:
-- [{"item":"ProductA","count":150}, {"item":"ProductB","count":120}, ...]
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val topCategories = df
  .agg(approx_top_k(col("category"), 10))
  .collect()

// With grouping
val topProductsByRegion = df
  .groupBy("region")
  .agg(approx_top_k(col("product"), 5).as("top_products"))
```

## See Also

- `collect_list` - Collects all values into an array
- `collect_set` - Collects distinct values into an array
- `count` - Exact count aggregation
- `approx_count_distinct` - Approximate distinct count