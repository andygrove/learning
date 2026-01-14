# WidthBucket

## Overview
The `width_bucket` function assigns values to histogram buckets of equal width, returning the bucket number (1-indexed) where the input value falls. It partitions a range from `minValue` to `maxValue` into `numBucket` equal-width buckets and determines which bucket contains the input `value`.

## Syntax
```sql
width_bucket(value, min_value, max_value, num_buckets)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.expr
df.select(expr("width_bucket(value, min_value, max_value, num_buckets)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `value` | Double, YearMonthIntervalType, DayTimeIntervalType | The input value to be assigned to a bucket |
| `minValue` | Double, YearMonthIntervalType, DayTimeIntervalType | The minimum value of the histogram range |
| `maxValue` | Double, YearMonthIntervalType, DayTimeIntervalType | The maximum value of the histogram range |
| `numBucket` | Long | The number of buckets to create (must be positive) |

## Return Type
`LongType` - Returns the bucket number as a long integer.

## Supported Data Types

- **Numeric**: DoubleType for all three value parameters (value, minValue, maxValue)
- **Interval Types**: YearMonthIntervalType or DayTimeIntervalType (all three value parameters must be the same interval type)
- **Bucket Count**: LongType for the number of buckets parameter

All three value parameters (value, minValue, maxValue) must be of the same data type.

## Algorithm

- Divides the range [minValue, maxValue] into `numBucket` equal-width intervals
- Calculates which bucket the input value falls into using the formula: bucket = floor((value - minValue) / bucket_width) + 1
- Returns bucket numbers from 1 to `numBucket` for values within the range
- Values below minValue return bucket 0, values above maxValue return bucket `numBucket + 1`
- Uses double precision arithmetic internally, converting interval types to numeric values for computation

## Partitioning Behavior
This expression does not affect data partitioning:

- Preserves existing partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be applied as a projection or filter predicate without repartitioning

## Edge Cases

- **Null handling**: Returns null if any input parameter is null (nullIntolerant = true)
- **Invalid bucket count**: Behavior depends on the companion object implementation for non-positive bucket counts
- **Equal min/max values**: May result in division by zero, handled by the companion object logic
- **Out of range values**: Values outside [minValue, maxValue] return bucket 0 or numBucket + 1
- **Type consistency**: All three value parameters must be compatible types (same interval type or all numeric)

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method. It generates optimized Java code that calls static methods in the `WidthBucket` companion object for both null checking and bucket computation, avoiding interpreted evaluation overhead.

## Examples
```sql
-- Numeric example: Distribute sales amounts into 10 buckets
SELECT width_bucket(sales_amount, 0.0, 1000.0, 10) as bucket
FROM sales_data;

-- Interval example: Categorize time intervals
SELECT width_bucket(INTERVAL '5' DAY, INTERVAL '0' DAY, INTERVAL '30' DAY, 6) as time_bucket;

-- Result: 2 (falls in the second bucket of 6 buckets spanning 0-30 days)
```

```scala
// DataFrame API example
import org.apache.spark.sql.functions.expr

val df = spark.table("sales_data")
df.select(
  col("sales_amount"),
  expr("width_bucket(sales_amount, 0.0, 1000.0, 10)").as("bucket")
).show()
```

## See Also

- `ntile` - Distributes rows into a specified number of ranked groups
- `percentile_approx` - Computes approximate percentiles
- Mathematical functions for range and statistical operations