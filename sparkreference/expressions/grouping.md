# Grouping

## Overview
The `Grouping` expression is used in SQL aggregation queries with `GROUP BY GROUPING SETS`, `CUBE`, or `ROLLUP` to determine whether a specific column is aggregated (grouped) in the current result row. It returns 1 if the column is aggregated (null in super-aggregate rows) and 0 if the column contains an actual grouped value.

## Syntax
```sql
GROUPING(column_expression)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.groupBy().agg(grouping(col("column_name")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The column expression to check for grouping status |

## Return Type
`ByteType` - Returns a byte value (0 or 1) indicating grouping status.

## Supported Data Types
Accepts any data type as input since it evaluates the grouping metadata rather than the actual column values. The input expression type is not restricted.

## Algorithm
- Accesses the virtual `groupingId` attribute that Spark maintains internally during CUBE/ROLLUP/GROUPING SETS operations
- Extracts the bit corresponding to the specified column from the grouping ID bitmask
- Returns 1 if the bit indicates the column is aggregated (grouped out)
- Returns 0 if the bit indicates the column contains actual grouped values
- The expression is marked as `Unevaluable`, meaning evaluation is handled specially during query planning

## Partitioning Behavior
- Does not directly affect partitioning as it's a metadata accessor
- Inherits partitioning behavior from the underlying GROUP BY operation
- Typically used in contexts that may require shuffle for grouping operations (CUBE/ROLLUP)

## Edge Cases
- **Null handling**: Returns non-null results even when the referenced column contains nulls, as it reports grouping metadata
- **Non-nullable**: The expression itself never returns null (`nullable = false`)
- **Invalid context**: Can only be used within GROUP BY GROUPING SETS, CUBE, or ROLLUP contexts
- **Missing grouping ID**: Relies on the presence of `VirtualColumn.groupingIdAttribute` in the query plan

## Code Generation
This expression does **not** support Tungsten code generation. It extends `Unevaluable`, meaning it's resolved and replaced during query planning rather than being evaluated at runtime through generated code.

## Examples
```sql
-- Example with CUBE
SELECT col1, col2, SUM(amount), GROUPING(col1), GROUPING(col2)
FROM sales 
GROUP BY CUBE(col1, col2);

-- Example with ROLLUP  
SELECT year, quarter, SUM(revenue), GROUPING(year), GROUPING(quarter)
FROM financial_data
GROUP BY ROLLUP(year, quarter);

-- Example with GROUPING SETS
SELECT category, region, COUNT(*), GROUPING(category), GROUPING(region)  
FROM products
GROUP BY GROUPING SETS ((category), (region), ());
```

```scala
// DataFrame API usage with CUBE
import org.apache.spark.sql.functions._

df.cube("col1", "col2")
  .agg(
    sum("amount"),
    grouping("col1").alias("grouping_col1"),  
    grouping("col2").alias("grouping_col2")
  )
```

## See Also
- `GroupingID` - Returns the complete grouping identifier as a bitmask
- `CUBE` - Creates grouping sets for all combinations of specified columns
- `ROLLUP` - Creates hierarchical grouping sets
- `GROUPING SETS` - Explicitly specifies which grouping combinations to compute