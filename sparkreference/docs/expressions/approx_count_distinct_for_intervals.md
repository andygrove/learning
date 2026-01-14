# ApproxCountDistinctForIntervals

## Overview

ApproxCountDistinctForIntervals is a Spark SQL aggregate expression that computes the approximate number of distinct values within specified intervals using the HyperLogLog++ algorithm. It partitions input values into intervals defined by endpoints and returns an array of approximate distinct counts for each interval.

## Syntax

```sql
approx_count_distinct_for_intervals(column, array_of_endpoints, relative_sd)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The column or expression to count distinct values for |
| endpointsExpression | Expression | Array of endpoints defining intervals (must be foldable/constant) |
| relativeSD | Double | Maximum relative standard deviation for HyperLogLog++ algorithm (default: 0.05) |
| mutableAggBufferOffset | Int | Offset for mutable aggregation buffer (internal parameter) |
| inputAggBufferOffset | Int | Offset for input aggregation buffer (internal parameter) |

## Return Type

ArrayType(LongType) - Returns an array of Long values representing approximate distinct counts for each interval.

## Supported Data Types

Input column supports:

- All numeric types (IntegerType, LongType, FloatType, DoubleType, DecimalType)
- TimestampType and TimestampNTZType
- DateType
- YearMonthIntervalType and DayTimeIntervalType

Endpoints array supports:

- Array of numeric types
- Array of DateType
- Array of TimestampType or TimestampNTZType
- Array of AnsiIntervalType

## Algorithm

- Converts input values to double precision for interval searching
- Uses binary search to locate which interval each value belongs to
- Maintains separate HyperLogLog++ sketches for each interval defined by consecutive endpoints
- Intervals are defined as (endpoint[i-1], endpoint[i]] - left-exclusive, right-inclusive
- Values outside the entire range are ignored
- For duplicate endpoints, the corresponding interval gets a distinct count of 1

## Partitioning Behavior

- This is an aggregate function that requires grouping all data
- Requires shuffle operations when used in distributed computing
- Does not preserve input partitioning as it needs to aggregate across partitions
- Uses merge operations to combine partial aggregates from different partitions

## Edge Cases

- Null values in the input column are ignored during computation
- Values outside the range [endpoints.first, endpoints.last] are ignored
- Duplicate endpoints are allowed and result in intervals with NDV = 1
- Endpoints array must contain at least 2 elements
- Endpoints expression must be foldable (constant/literal)
- Empty input results in zero counts for all intervals

## Code Generation

This expression does not support code generation and uses interpreted evaluation mode. It extends TypedImperativeAggregate which typically falls back to interpreted execution due to the complexity of the HyperLogLog++ algorithm implementation.

## Examples

```sql
-- Count distinct values in salary ranges
SELECT approx_count_distinct_for_intervals(
  salary, 
  array(30000, 50000, 80000, 120000),
  0.05
) as salary_range_counts
FROM employees;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.agg(
  expr("approx_count_distinct_for_intervals(salary, array(30000, 50000, 80000, 120000), 0.05)")
    .alias("salary_range_counts")
).show()
```

## See Also

- approx_count_distinct - Standard approximate distinct count
- HyperLogLogPlusPlus - Underlying algorithm implementation
- count(distinct) - Exact distinct count aggregate function