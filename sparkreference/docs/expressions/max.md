# Max

## Overview
The Max aggregate function returns the maximum value from a group of rows. It is a declarative aggregate expression that maintains a running maximum value during aggregation and supports distributed computation through merge operations.

## Syntax
```sql
SELECT MAX(column) FROM table
SELECT MAX(column) FROM table GROUP BY grouping_column
```

```scala
// DataFrame API
df.agg(max("column"))
df.groupBy("grouping_column").agg(max("column"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The expression or column to find the maximum value from |

## Return Type
Returns the same data type as the input expression. The return type is determined by `child.dataType`.

## Supported Data Types
Supports any data type that has an ordering defined, as validated by `TypeUtils.checkForOrderingExpr()`. This includes:

- Numeric types (IntegerType, LongType, DoubleType, FloatType, DecimalType)
- String types (StringType)
- Date and timestamp types (DateType, TimestampType)
- Binary types (BinaryType)

## Algorithm
The Max aggregate function uses the following evaluation strategy:

- Initializes the aggregation buffer with a null value of the child's data type
- For each input row, updates the maximum using the `greatest()` function between current max and new value
- During merge operations (for distributed computation), combines partial results using `greatest()` between left and right max values
- Returns the final maximum value stored in the aggregation buffer
- Uses lazy evaluation for all expressions to optimize performance

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve partitioning as it requires combining values across partitions
- Requires a shuffle operation when used without grouping columns (global aggregation)
- When used with GROUP BY, may require shuffle depending on grouping key distribution

## Edge Cases

- **Null handling**: Returns null if all input values are null; null values are ignored during comparison
- **Empty input**: Returns null when applied to an empty result set or group
- **Single value**: Returns that single value even if it's null
- **Mixed nulls and values**: Ignores null values and returns the maximum of non-null values
- **Overflow behavior**: Inherits overflow behavior from the underlying data type's comparison operations

## Code Generation
This expression extends `DeclarativeAggregate`, which supports Tungsten code generation. The aggregate operations (greatest function calls) are code-generated for optimal performance rather than using interpreted evaluation.

## Examples
```sql
-- Basic maximum
SELECT MAX(col) FROM VALUES (10), (50), (20) AS tab(col);
-- Result: 50

-- Maximum with grouping
SELECT category, MAX(price) FROM products GROUP BY category;

-- Maximum with null handling
SELECT MAX(col) FROM VALUES (10), (NULL), (20) AS tab(col);
-- Result: 20
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.max

df.agg(max("salary"))
df.groupBy("department").agg(max("salary").alias("max_salary"))

// With null values
df.select(max(when($"value" > 0, $"value")))
```

## See Also

- Min - finds minimum values
- Greatest - compares multiple expressions and returns the maximum
- First - returns first value in a group
- Last - returns last value in a group