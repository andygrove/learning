# ApproximatePercentile

## Overview
ApproximatePercentile is a Spark Catalyst aggregate expression that computes approximate percentiles of numeric data using the t-digest algorithm. It provides a memory-efficient way to estimate percentiles for large datasets without requiring exact sorting, trading precision for performance and memory usage.

## Syntax
```sql
percentile_approx(col, percentage [, accuracy])
percentile_approx(col, array_of_percentages [, accuracy])
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.agg(expr("percentile_approx(column, 0.5, 10000)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The column or expression to compute percentiles for |
| percentageExpression | Expression | Single percentile (0.0-1.0) or array of percentiles to compute |
| accuracyExpression | Expression | Optional accuracy parameter (default: 10000). Higher values = more accuracy |

## Return Type
Returns the same data type as the input column. If an array of percentiles is provided, returns an array of the input data type with `containsNull = false`.

## Supported Data Types

- **Numeric types**: ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType, DecimalType
- **Temporal types**: DateType, TimestampType, TimestampNTZType
- **Interval types**: YearMonthIntervalType, DayTimeIntervalType

## Algorithm

- Uses the PercentileDigest class which implements the t-digest algorithm for approximate percentile computation
- Converts all input values to double precision for internal processing
- Maintains a compressed representation of the data distribution with configurable accuracy
- Supports incremental updates and merging of partial results across partitions
- Final evaluation converts results back to the original input data type

## Partitioning Behavior
This is an aggregate function that requires data movement:

- Does not preserve partitioning as it needs to aggregate across all partitions
- Requires shuffle operations to merge partial aggregates from different partitions
- Uses TypedImperativeAggregate which supports partial aggregation to minimize data movement

## Edge Cases

- **Null handling**: Ignores null input values during computation
- **Empty input**: Returns null when no non-null values are processed
- **Invalid percentages**: Validates that percentages are between 0.0 and 1.0 inclusive
- **Invalid accuracy**: Requires accuracy to be positive and ≤ Int.MaxValue
- **Non-foldable expressions**: Percentage and accuracy parameters must be compile-time constants

## Code Generation
This expression uses TypedImperativeAggregate which does not support full code generation. It falls back to interpreted mode for the aggregate buffer operations, though individual expression evaluations within update/merge may use code generation.

## Examples
```sql
-- Single percentile (median)
SELECT percentile_approx(salary, 0.5) as median_salary FROM employees;

-- Multiple percentiles with custom accuracy
SELECT percentile_approx(response_time, array(0.25, 0.5, 0.75, 0.95), 50000) as quartiles 
FROM web_requests;

-- Using with GROUP BY
SELECT department, percentile_approx(salary, 0.9) as p90_salary 
FROM employees 
GROUP BY department;
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Single percentile
df.agg(expr("percentile_approx(amount, 0.5)").as("median"))

// Multiple percentiles
df.agg(expr("percentile_approx(latency, array(0.5, 0.95, 0.99))").as("percentiles"))

// With custom accuracy
df.agg(expr("percentile_approx(value, 0.95, 100000)").as("p95"))
```

## See Also

- **Percentile**: Exact percentile computation (more expensive but precise)
- **ApproxQuantile**: Similar approximate quantile functionality in DataFrame API
- Other aggregate functions: Count, Sum, Avg, Min, Max