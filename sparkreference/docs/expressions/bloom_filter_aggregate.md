# BloomFilterAggregate

## Overview
BloomFilterAggregate is a Catalyst aggregate expression that creates a Bloom filter from input values during aggregation. It builds a probabilistic data structure that can efficiently test set membership with no false negatives but possible false positives.

## Syntax
```sql
bloom_filter_agg(column [, estimated_num_items [, num_bits]])
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | Child expression producing values to add to the Bloom filter. Supports Long, Integer, Short, Byte, and String types |
| estimatedNumItemsExpression | Expression | The estimated number of distinct items (optional). Must be a foldable Long expression > 0 |
| numBitsExpression | Expression | The number of bits to use for the Bloom filter (optional). Must be a foldable Long expression > 0 |

## Return Type
BinaryType - Returns a serialized Bloom filter as a byte array, or null if no non-null values were processed.

## Supported Data Types

- LongType
- IntegerType  
- ShortType
- ByteType
- StringType (any string type)

## Algorithm

- Creates a Bloom filter with specified estimated items and bit size parameters
- For each non-null input value, uses a type-specific updater to add the value to the filter
- Merges Bloom filters from different partitions using the mergeInPlace operation
- Serializes the final Bloom filter to a byte array for storage/transmission
- Returns null if the filter has zero cardinality (no bits set)

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve partitioning as it performs aggregation
- Requires shuffle for global aggregation across partitions
- Supports partial aggregation with merge capability for distributed computation

## Edge Cases

- Null values are ignored during processing and do not affect the Bloom filter
- Returns null when no non-null values are processed (filter cardinality is 0)
- estimatedNumItems and numBits are capped by configuration limits (RUNTIME_BLOOM_FILTER_MAX_NUM_ITEMS and RUNTIME_BLOOM_FILTER_MAX_NUM_BITS)
- Default values are taken from SQLConf when parameters are not specified
- Requires estimatedNumItems and numBits to be foldable (constant) expressions

## Code Generation
This expression extends TypedImperativeAggregate and does not support Tungsten code generation. It falls back to interpreted mode using the imperative aggregation buffer approach.

## Examples
```sql
-- Basic usage with default parameters
SELECT bloom_filter_agg(user_id) FROM users;

-- With estimated number of items
SELECT bloom_filter_agg(product_id, 1000) FROM products;

-- With both estimated items and bit size
SELECT bloom_filter_agg(session_id, 10000, 80000) FROM sessions;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic usage
df.agg(expr("bloom_filter_agg(user_id)"))

// With parameters
df.agg(expr("bloom_filter_agg(product_id, 1000, 8000)"))

// Multiple Bloom filters
df.groupBy("category")
  .agg(expr("bloom_filter_agg(product_id, 500)").as("product_filter"))
```

## See Also

- BloomFilter data structure
- bloom_filter_might_contain function for querying Bloom filters
- Probabilistic data structures for set membership testing