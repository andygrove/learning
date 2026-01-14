# ApproxTopKEstimate

## Overview
The `ApproxTopKEstimate` expression extracts the top K most frequent items from an approximate top-K state object. This expression works in conjunction with approximate counting algorithms to efficiently retrieve the most frequently occurring items without requiring exact counts across large datasets.

## Syntax
```sql
approx_top_k_estimate(state, k)
```

```scala
// DataFrame API
col("state").approxTopKEstimate(k)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| state | Expression | The approximate top-K state object containing frequency estimates |
| k | Expression | The number of top items to retrieve from the state |

## Return Type
Returns an array of structs with the following schema:
- `item`: The actual item value
- `count`: The estimated frequency count for that item

## Supported Data Types

- **state**: Binary or complex state object (produced by approximate top-K aggregation functions)
- **k**: Integer types (TINYINT, SMALLINT, INT, BIGINT)
- **item types**: Any data type that was used in the original approximate top-K aggregation

## Algorithm

- Deserializes the approximate top-K state object to access internal frequency estimates
- Sorts items by their estimated frequency counts in descending order  
- Selects the top K items based on the provided k parameter
- Returns structured results with both item values and their estimated counts
- Uses probabilistic data structures for memory-efficient approximation

## Partitioning Behavior
How this expression affects partitioning:

- Preserves existing partitioning as it operates on individual state objects
- Does not require shuffle operations since it processes state locally
- Can be applied per partition independently

## Edge Cases

- **Null state**: Returns null when the state parameter is null
- **Null k**: Returns null when k parameter is null  
- **k larger than available items**: Returns all available items when k exceeds the number of distinct items in the state
- **k = 0**: Returns an empty array
- **Negative k**: Behavior depends on implementation but typically returns empty array
- **Empty state**: Returns empty array when state contains no items

## Code Generation
This expression likely falls back to interpreted mode due to the complexity of deserializing state objects and performing sorting operations, which are not easily amenable to simple code generation patterns.

## Examples
```sql
-- Extract top 3 items from an approximate top-K state
SELECT approx_top_k_estimate(topk_state, 3) as top_items
FROM aggregated_results;

-- Result format:
-- [{"item":"a","count":10},{"item":"b","count":8},{"item":"c","count":4}]
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(
  approx_top_k_estimate(col("topk_state"), lit(5)).as("top_5_items")
)

// Extracting items and counts separately
df.select(
  approx_top_k_estimate(col("state"), lit(3)).as("top_items")
).select(
  col("top_items.item").as("items"),
  col("top_items.count").as("counts")
)
```

## See Also

- `approx_top_k` - Aggregate function for building approximate top-K states
- `approx_count_distinct` - Related approximate counting function
- `collect_list` - Exact alternative for smaller datasets
- `count` - Exact counting functions