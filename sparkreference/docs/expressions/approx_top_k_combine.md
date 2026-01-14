# ApproxTopKCombine

## Overview
ApproxTopKCombine is an internal aggregation expression used to combine intermediate results from ApproxTopK operations during the merge phase of distributed aggregation. It processes sketch data structures to maintain approximate counts of the top-K most frequent items across multiple partitions.

## Syntax
This is an internal expression not directly callable from SQL or DataFrame API. It's automatically used during the combine phase of `approx_top_k` aggregation.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | Input expression containing serialized sketch data from partial aggregations |
| k | Int | Maximum number of top items to track |
| maxMapSize | Int | Maximum size of the internal frequency map to prevent excessive memory usage |

## Return Type
Returns a binary representation of the combined frequency sketch containing item-count pairs.

## Supported Data Types
Accepts binary data type containing serialized sketch structures from the map phase of ApproxTopK aggregation.

## Algorithm

- Deserializes multiple frequency sketches from input binary data
- Merges frequency maps from different partitions by summing counts for identical items  
- Maintains only the top-K items by frequency after merging
- Applies maxMapSize limit to prevent memory exhaustion during processing
- Serializes the combined result back to binary format for final aggregation phase

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve partitioning as it's used in shuffle-based aggregation
- Operates during the combine phase before final reduce step
- Requires shuffle to collect partial results from different partitions

## Edge Cases

- Null input sketches are skipped during the merge process
- Empty sketches contribute no items to the final result
- When combined item count exceeds maxMapSize, lower frequency items are discarded
- Identical items from different partitions have their frequencies summed
- If fewer than K distinct items exist, returns all available items

## Code Generation
This expression typically falls back to interpreted mode due to the complexity of sketch deserialization and merging operations that don't benefit significantly from code generation.

## Examples
```sql
-- Not directly callable - used internally by:
SELECT approx_top_k(column_name, 5) FROM table_name;
```

```scala
// Not directly callable - used internally during:
df.agg(expr("approx_top_k(column_name, 5)"))
```

## See Also

- ApproxTopK - The main user-facing aggregation function
- ApproxTopKMerge - Final merge phase expression  
- Other approximate aggregation functions like approx_count_distinct