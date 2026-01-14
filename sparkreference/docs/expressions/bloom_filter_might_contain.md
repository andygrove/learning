# BloomFilterMightContain

## Overview
The `BloomFilterMightContain` expression tests whether a long value might be contained in a Bloom filter. This expression is primarily used for Bloom filter join rewrites and optimization in Spark SQL, where it evaluates a binary Bloom filter data against a long value to determine potential membership.

## Syntax
```sql
might_contain(bloom_filter_binary, long_value)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| bloomFilterExpression | Binary | The binary data representation of a Bloom filter |
| valueExpression | Long | The long value to test for membership in the Bloom filter |

## Return Type
`Boolean` - Returns `true` if the value might be contained in the Bloom filter, `false` if it's definitely not contained, or `null` if either input is null.

## Supported Data Types

- **Left operand (Bloom filter)**: `BinaryType` or `NullType`
- **Right operand (Value)**: `LongType` or `NullType`

The bloom filter expression must be one of:

- A foldable expression (constant value)
- An uncorrelated scalar subquery
- A `GetStructField` from an uncorrelated subquery
- A `ScalarSubqueryReference`

## Algorithm

- Deserializes the binary bloom filter data using `BloomFilter.readFrom()`
- Evaluates the input long value from the value expression
- Calls `BloomFilter.mightContainLong()` to test membership
- Returns boolean result indicating potential membership
- Handles null inputs by returning null (nullable expression)

## Partitioning Behavior
This expression does not directly affect partitioning behavior as it's a predicate expression that operates on individual rows. However, when used in join conditions, it can enable Bloom filter join optimizations that may influence query execution plans and data shuffling strategies.

## Edge Cases

- **Null bloom filter**: Returns `null` if the bloom filter binary data is null
- **Null value**: Returns `null` if the test value is null
- **Invalid binary data**: May throw exceptions during deserialization if binary data is corrupted
- **Type validation**: Strict type checking ensures only valid combinations of BinaryType/LongType are accepted
- **Subquery restrictions**: Only accepts uncorrelated scalar subqueries for bloom filter expression

## Code Generation
This expression supports Tungsten code generation. When the bloom filter can be evaluated at compile time, it generates optimized Java code that:

- Adds the deserialized bloom filter as a reference object in the generated code
- Generates inline code for value evaluation and membership testing
- Falls back to interpreted evaluation if the bloom filter cannot be resolved at code generation time

## Examples
```sql
-- Test if value 12345 might be in a bloom filter from a subquery
SELECT * FROM table1 
WHERE might_contain(
  (SELECT bloom_filter_column FROM bloom_table WHERE id = 1), 
  table1.long_column
);
```

```scala
// DataFrame API usage with literal bloom filter
import org.apache.spark.sql.functions._
df.filter(expr("might_contain(bloom_filter_col, id_col)"))

// With column references
df.filter(col("bloom_filter_binary").contains(col("test_value")))
```

## See Also

- `BloomFilter` class for bloom filter operations
- Bloom filter aggregate functions for creating bloom filters
- Join optimization and runtime filtering expressions