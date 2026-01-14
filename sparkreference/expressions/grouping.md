# Grouping

## Overview
The Grouping expressions in Spark Catalyst provide support for advanced aggregation operations including CUBE, ROLLUP, and GROUPING SETS. These expressions are placeholders that get replaced by the analyzer during query planning to generate multiple grouping combinations for aggregation operations.

## Syntax
```sql
-- CUBE operation
SELECT col1, col2, aggregate_func(col3) FROM table GROUP BY CUBE(col1, col2)

-- ROLLUP operation  
SELECT col1, col2, aggregate_func(col3) FROM table GROUP BY ROLLUP(col1, col2)

-- GROUPING SETS operation
SELECT col1, col2, aggregate_func(col3) FROM table GROUP BY GROUPING SETS ((col1), (col2), (col1, col2))

-- GROUPING function
SELECT col1, GROUPING(col1), aggregate_func(col2) FROM table GROUP BY CUBE(col1)

-- GROUPING_ID function
SELECT col1, col2, GROUPING_ID(col1, col2), aggregate_func(col3) FROM table GROUP BY CUBE(col1, col2)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| groupingSetIndexes | Seq[Seq[Int]] | Indexes mapping to flattened grouping expressions |
| children/flatGroupingSets | Seq[Expression] | The actual grouping expressions |
| userGivenGroupByExprs | Seq[Expression] | User-specified GROUP BY expressions (GroupingSets only) |
| groupByExprs | Seq[Expression] | Expressions used for grouping in GroupingID |
| child | Expression | Single column expression for Grouping function |

## Return Type
- **BaseGroupingSets (Cube, Rollup, GroupingSets)**: These are placeholder expressions that don't return values directly
- **Grouping**: Returns `ByteType` (0 for not aggregated, 1 for aggregated)  
- **GroupingID**: Returns `IntegerType` or `LongType` based on `SQLConf.get.integerGroupingIdEnabled` configuration

## Supported Data Types
- **BaseGroupingSets**: Supports any expression type as grouping columns
- **Grouping**: Accepts any expression type as input, returns ByteType
- **GroupingID**: Accepts any expression type as input, returns IntegerType/LongType

## Algorithm
- **CUBE**: Generates all possible combinations (2^N subsets) of the grouping expressions using recursive subset generation
- **ROLLUP**: Generates hierarchical combinations by taking prefixes of grouping expressions (N+1 combinations)
- **GROUPING SETS**: Uses user-specified combinations of grouping expressions
- **Grouping**: References a virtual `groupingIdAttribute` to determine if a column is aggregated in the current row
- **GroupingID**: Computes grouping level as `(grouping(c1) << (n-1)) + (grouping(c2) << (n-2)) + ... + grouping(cn)`

## Partitioning Behavior
- These expressions typically require shuffle operations as they generate multiple grouping combinations
- Each grouping set combination may require data redistribution based on different grouping keys
- The analyzer replaces these placeholder expressions before physical planning, so partitioning decisions are made at that stage

## Edge Cases
- **Null Handling**: `Grouping` is not nullable (returns 0 or 1), `GroupingID` is also not nullable
- **Empty Input**: Empty grouping sets result in a single empty grouping (equivalent to global aggregation)
- **Semantic Equality**: `distinctGroupByExprs` uses semantic equality to deduplicate expressions like `(a * b)` and `(b * a)`
- **Resolution**: All BaseGroupingSets expressions have `resolved = false` and must be replaced by the analyzer
- **Configuration Dependency**: GroupingSets child ordering depends on `groupingIdWithAppendedUserGroupByEnabled` configuration

## Code Generation
- **BaseGroupingSets**: Extends `CodegenFallback`, indicating these expressions fall back to interpreted mode
- **Grouping/GroupingID**: Extend `Unevaluable`, meaning they don't support direct evaluation and must be resolved during analysis

## Examples
```sql
-- CUBE example: generates (a,b,c), (a,b), (a,c), (b,c), (a), (b), (c), ()
SELECT name, age, COUNT(*) FROM people GROUP BY CUBE(name, age);

-- ROLLUP example: generates (a,b,c), (a,b), (a), ()  
SELECT year, month, day, SUM(sales) FROM sales_data GROUP BY ROLLUP(year, month, day);

-- GROUPING SETS example with specific combinations
SELECT col1, col2, SUM(amount) FROM table 
GROUP BY GROUPING SETS ((col1), (col2), (col1, col2));

-- GROUPING function to identify aggregated rows
SELECT name, GROUPING(name), SUM(age) FROM people GROUP BY CUBE(name);

-- GROUPING_ID for multi-level grouping identification
SELECT name, age, GROUPING_ID(name, age), COUNT(*) FROM people GROUP BY CUBE(name, age);
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// CUBE
df.cube($"col1", $"col2").agg(sum($"amount"))

// ROLLUP  
df.rollup($"year", $"month").agg(avg($"sales"))

// Using grouping function
df.cube($"category").agg(
  sum($"amount"), 
  grouping($"category").alias("is_total")
)
```

## See Also
- **Aggregate Functions**: Used in conjunction with these grouping operations
- **Window Functions**: Alternative approach for hierarchical aggregations
- **VirtualColumn**: Provides the underlying `groupingIdAttribute` mechanism
- **TreePattern.GROUPING_ANALYTICS**: Tree pattern used for matching these expressions during analysis