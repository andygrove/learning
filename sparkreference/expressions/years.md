# Partition Transform Expressions

## Overview

Partition transform expressions are abstract expressions that represent v2 partition transforms in Apache Spark SQL. These expressions are used to pass partitioning transformations from the DataFrame API to data source implementations and are unevaluable since their concrete implementations are determined by the data source.

## Syntax

```scala
// DataFrame API usage
df.writeTo("catalog.db.table")
  .partitionedBy(years($"timestamp"), months($"date"), days($"created_at"), 
                hours($"event_time"), bucket(10, $"user_id"))
  .create()
```

## Arguments

### Time-based Transforms (Years, Months, Days, Hours)
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression, typically a timestamp or date column |

### Bucket Transform
| Argument | Type | Description |
|----------|------|-------------|
| numBuckets | Literal | A literal integer expression specifying the number of buckets |
| child | Expression | The input expression to be bucketed |

## Return Type

All partition transform expressions return `IntegerType`.

## Supported Data Types

The supported data types depend on the data source implementation since these are abstract transforms:
- **Time-based transforms**: Typically timestamp and date types
- **Bucket transform**: Any hashable data type (strings, numbers, etc.)

## Algorithm

- Partition transform expressions are **unevaluable** and cannot be directly executed
- They serve as abstract representations passed to data source implementations
- Each data source provides concrete implementations for these transforms
- The transforms are resolved during write operations to partitioned tables
- Actual partitioning logic is delegated to the underlying data source (e.g., Iceberg, Delta Lake)

## Partitioning Behavior

These expressions are specifically designed for partitioning:
- **Creates physical partitions**: Each transform creates partition boundaries in the target table
- **No shuffle required**: Transforms are applied during write operations
- **Partition pruning enabled**: Allows efficient query pruning based on partition values
- **Immutable partitioning**: Once applied, the partitioning scheme becomes part of the table schema

## Edge Cases

- **Null handling**: Returns `nullable = true`, indicating null values are permitted
- **Evaluation attempts**: Throws `SparkException` with error class `PARTITION_TRANSFORM_EXPRESSION_NOT_IN_PARTITIONED_BY` if evaluated outside partitioning context
- **Code generation**: Throws the same exception if code generation is attempted
- **Invalid bucket numbers**: `Bucket` transform validates that `numBuckets` is a literal integer, throwing `QueryCompilationErrors.invalidBucketsNumberError` otherwise
- **Type safety**: Each transform maintains type safety through `withNewChildInternal` methods

## Code Generation

**No code generation support**. These expressions throw `SparkException` in `doGenCode()` method since they are abstract transforms that should never be directly evaluated or code-generated.

## Examples

```scala
// Time-based partitioning
df.writeTo("events_table")
  .partitionedBy(years($"event_timestamp"), months($"event_timestamp"))
  .create()

// Daily partitioning
df.writeTo("daily_logs")
  .partitionedBy(days($"log_date"))
  .create()

// Hourly partitioning for high-frequency data
df.writeTo("metrics")
  .partitionedBy(days($"metric_time"), hours($"metric_time"))
  .create()

// Bucket partitioning for even distribution
df.writeTo("user_data")
  .partitionedBy(bucket(100, $"user_id"))
  .create()

// Combined partitioning strategy
df.writeTo("comprehensive_table")
  .partitionedBy(years($"created_at"), bucket(50, $"category"))
  .create()
```

## See Also

- **Expression**: Base class for all Catalyst expressions
- **Unevaluable**: Trait for expressions that cannot be directly evaluated
- **UnaryLike**: Trait for expressions with a single child expression
- **DataSourceV2**: Interface for data sources that support these partition transforms
- **Partitioning expressions**: `HashPartitioning`, `RangePartitioning` for DataFrame partitioning