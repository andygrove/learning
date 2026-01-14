# HistogramNumeric

## Overview
HistogramNumeric is an aggregate function that computes a histogram of numeric values by dividing the data range into a specified number of equal-width buckets. It returns an array of objects containing bucket boundaries and their corresponding frequencies, providing a distribution summary of the input data.

## Syntax
```sql
histogram_numeric(column, num_buckets)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| column | Numeric | The numeric column to compute the histogram for |
| num_buckets | Integer | The number of equal-width buckets to create (must be positive) |

## Return Type
Returns an array of structs with the following schema:
- `x`: Double - The lower bound of the histogram bucket
- `y`: Double - The frequency/count of values in that bucket

## Supported Data Types

- Integer types (TINYINT, SMALLINT, INT, BIGINT)
- Floating-point types (FLOAT, DOUBLE)
- Decimal types (DECIMAL)

## Algorithm

- Scans all input values to determine the minimum and maximum values in the dataset
- Divides the range [min, max] into the specified number of equal-width buckets
- Assigns each input value to its corresponding bucket based on its numeric value
- Counts the frequency of values in each bucket
- Returns bucket lower bounds with their corresponding frequencies

## Partitioning Behavior
This expression requires data shuffling and does not preserve partitioning:

- Requires a complete scan of all partitions to determine global min/max values
- Performs a shuffle operation to aggregate bucket counts across all partitions
- Final result is computed by combining partial histograms from all executors

## Edge Cases

- Null values are ignored and do not contribute to any bucket counts
- Empty input returns an empty array
- When all values are identical, creates buckets with the single value as boundary
- If num_buckets is less than or equal to 0, throws an analysis exception
- Handles floating-point precision issues when assigning values to bucket boundaries

## Code Generation
This expression does not support code generation (Tungsten) and operates in interpreted mode due to its complex aggregation logic requiring dynamic bucket management and global statistics computation.

## Examples
```sql
-- Create a 5-bucket histogram of numeric values
SELECT histogram_numeric(col, 5) FROM VALUES (0), (1), (2), (10) AS tab(col);
-- Result: [{"x":0,"y":1.0},{"x":1,"y":1.0},{"x":2,"y":1.0},{"x":10,"y":1.0}]

-- Histogram with salary data
SELECT histogram_numeric(salary, 3) FROM employees;

-- Using with different bucket counts
SELECT histogram_numeric(price, 10) FROM products WHERE category = 'electronics';
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._

df.agg(expr("histogram_numeric(value, 5)")).show()

// Using with groupBy
df.groupBy("category")
  .agg(expr("histogram_numeric(price, 8)").as("price_distribution"))
  .show()
```

## See Also

- `percentile_approx` - For computing approximate percentiles
- `approx_count_distinct` - For approximate cardinality estimation  
- `collect_list` - For collecting values into arrays
- Statistical aggregate functions for data distribution analysis