# Count

## Overview
The Count expression is a declarative aggregate function that counts the number of non-null rows in a group. It extends DeclarativeAggregate and implements a standard SQL COUNT operation with support for both parameterless COUNT(*) and COUNT(column) variants.

## Syntax
```sql
COUNT(*)
COUNT(expression)
COUNT(column_name)
```

```scala
// DataFrame API
df.agg(count("*"))
df.agg(count("column_name"))
df.groupBy("key").agg(count("value"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | Zero or more expressions to count non-null values for. Empty sequence represents COUNT(*) |

## Return Type
LongType (64-bit signed integer) - always non-nullable.

## Supported Data Types
All data types are supported as input expressions since the function only checks for null values rather than evaluating the actual data content.

## Algorithm

- Initializes an internal counter to 0L
- For each input row, checks if any of the child expressions evaluate to null
- If no child expressions are null (or no children for COUNT(*)), increments counter by 1
- During merge operations, sums counters from different partitions
- Returns the final count as a Long value

## Partitioning Behavior
This expression requires data shuffling for grouping operations:

- Does not preserve partitioning when used as a standalone aggregate
- Requires shuffle when combined with GROUP BY operations
- Can be partially computed on each partition before final merge

## Edge Cases

- Null handling: Only counts rows where all child expressions are non-null
- Empty input: Returns 0L as the default result when no rows match
- Parameterless COUNT(): Requires SQLConf.ALLOW_PARAMETERLESS_COUNT to be enabled, otherwise throws QueryCompilationError
- No overflow behavior since it uses Long type with practical dataset size limits

## Code Generation
This expression uses DeclarativeAggregate framework which supports Tungsten code generation through expression trees rather than custom codegen implementation.

## Examples
```sql
-- Count all rows
SELECT COUNT(*) FROM table1;

-- Count non-null values in a column
SELECT COUNT(column1) FROM table1;

-- Count with grouping
SELECT key, COUNT(value) FROM table1 GROUP BY key;
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions.count

// Count all rows
df.agg(count("*"))

// Count non-null values
df.agg(count("column1"))

// Grouped count
df.groupBy("key").agg(count("value"))
```

## See Also

- Sum - for summing numeric values
- Avg - for computing averages  
- Min/Max - for finding extreme values
- CollectList/CollectSet - for collecting values into arrays