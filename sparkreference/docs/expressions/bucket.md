# Bucket

## Overview
The Bucket expression implements the v2 partition transform for bucketing data into a fixed number of buckets. It distributes rows across buckets based on a hash of the child expression, enabling efficient data organization for query performance and parallelization.

## Syntax
```sql
BUCKET(num_buckets, column_expression)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.catalyst.expressions.Bucket
import org.apache.spark.sql.catalyst.expressions.Literal
Bucket(Literal(10), col("id"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| numBuckets | Literal | The number of buckets to distribute data into (must be a literal integer value) |
| child | Expression | The expression whose value will be hashed to determine bucket assignment |

## Return Type
IntegerType - Returns an integer value representing the bucket number (0 to numBuckets-1).

## Supported Data Types
The child expression can be of any data type that supports hashing, including:

- Numeric types (IntegerType, LongType, DoubleType, etc.)
- String types (StringType, VarcharType, CharType)
- Binary types
- Date and timestamp types
- Complex types (arrays, structs, maps)

## Algorithm
The bucket assignment is computed using the following process:

- Extract the value from the child expression
- Compute a hash code of the value using Spark's internal hash functions
- Apply modulo operation with numBuckets to determine final bucket
- Handle negative hash values to ensure non-negative bucket numbers
- Return the bucket number as an integer

## Partitioning Behavior
This expression is specifically designed for partitioning behavior:

- Creates hash-based partitioning with a fixed number of partitions
- Ensures uniform distribution of data across buckets (assuming good hash distribution)
- Enables co-location of rows with the same bucket value
- Does not require shuffle when used as a partition transform in v2 data sources
- Preserves bucketing for join optimizations when matching bucket schemes are used

## Edge Cases

- Null values: Null inputs are hashed consistently, typically assigned to bucket 0
- numBuckets must be positive: Zero or negative bucket counts will cause errors
- numBuckets validation: The constructor validates that numBuckets is a proper Literal through `expressionToNumBuckets`
- Hash collision handling: Multiple different values may map to the same bucket (expected behavior)
- Large numBuckets values: Very large bucket counts may create many empty buckets

## Code Generation
This expression extends PartitionTransformExpression and supports Catalyst code generation for optimal performance in the Tungsten execution engine. The hash computation and modulo operations are generated as efficient Java bytecode.

## Examples
```sql
-- Bucket customer data into 16 buckets based on customer_id
SELECT *, BUCKET(16, customer_id) as bucket_num 
FROM customers;

-- Use in table partitioning (DDL context)
CREATE TABLE bucketed_sales 
USING DELTA
PARTITIONED BY (BUCKET(10, customer_id))
AS SELECT * FROM sales;
```

```scala
// DataFrame API usage for bucketing
import org.apache.spark.sql.catalyst.expressions.{Bucket, Literal}
import org.apache.spark.sql.functions.col

val bucketExpr = Bucket(Literal(8), col("user_id").expr)
df.select(col("*"), Column(bucketExpr).alias("bucket"))

// Usage in partitioning scheme
val partitionTransforms = Array(BucketTransform(LiteralValue(16, IntegerType), "product_id"))
```

## See Also

- PartitionTransformExpression - Base class for partition transforms
- Hash expressions - Underlying hash computation methods  
- Murmur3Hash - Hash function used internally for bucket computation
- Dataset partitioning and bucketing operations