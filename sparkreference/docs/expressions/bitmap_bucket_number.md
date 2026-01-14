# BitmapBucketNumber

## Overview
The `BitmapBucketNumber` expression computes the bucket number for a given long value in bitmap operations. This function is typically used in bitmap-based analytics to determine which bucket or segment a particular value belongs to within a bitmap structure.

## Syntax
```sql
bitmap_bucket_number(value)
```

```scala
// DataFrame API
col("column_name").bitmap_bucket_number()
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| value | BIGINT | The long value for which to calculate the bucket number |

## Return Type
Returns `BIGINT` (LongType) representing the calculated bucket number.

## Supported Data Types

- BIGINT (LongType) - primary input type

- Other numeric types are implicitly cast to BIGINT due to `ImplicitCastInputTypes` trait

## Algorithm

- Accepts a long integer input value

- Delegates computation to `BitmapExpressionUtils.bitmapBucketNumber()` method

- Performs bucket number calculation using static invocation for optimized execution

- Returns the computed bucket number as a long value

- Does not return null values (`returnNullable = false`)

## Partitioning Behavior
This expression has minimal impact on partitioning:

- Does not preserve existing partitioning schemes

- Does not require data shuffle operations

- Can be executed locally on each partition independently

## Edge Cases

- **Null handling**: Input nulls are handled by the underlying `BitmapExpressionUtils` implementation

- **Non-null guarantee**: The expression is marked as non-nullable, meaning it always produces a valid result

- **Implicit casting**: Non-long numeric inputs are automatically cast to long type

- **Overflow behavior**: Depends on the underlying bucket calculation algorithm in `BitmapExpressionUtils`

## Code Generation
This expression uses runtime replacement pattern:

- Implements `RuntimeReplaceable` trait for optimized execution

- Replaced with `StaticInvoke` during query planning phase

- Leverages direct method invocation rather than interpreted expression evaluation

- Supports Catalyst's code generation optimizations through static method calls

## Examples
```sql
-- Calculate bucket number for a specific value
SELECT bitmap_bucket_number(12345) AS bucket;

-- Use in WHERE clause for filtering
SELECT * FROM table WHERE bitmap_bucket_number(user_id) = 5;

-- Group by bucket numbers
SELECT bitmap_bucket_number(value_col) AS bucket, COUNT(*) 
FROM data_table 
GROUP BY bitmap_bucket_number(value_col);
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Calculate bucket numbers
df.select(expr("bitmap_bucket_number(user_id)").as("bucket"))

// Filter by bucket number
df.filter(expr("bitmap_bucket_number(user_id) = 5"))

// Aggregate by bucket
df.groupBy(expr("bitmap_bucket_number(value_col)").as("bucket"))
  .count()
```

## See Also

- Bitmap-related expressions for complementary bitmap operations

- Hash partitioning functions for alternative data distribution strategies

- Bucketing functions in Spark SQL for similar partitioning concepts