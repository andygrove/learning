# GroupingID

## Overview
The `GroupingID` expression computes a grouping identifier that indicates which columns are being grouped in GROUPING SETS, CUBE, and ROLLUP operations. It returns a bitmask where each bit represents whether a specific grouping column is included in the current grouping combination, enabling identification of different aggregation levels in hierarchical grouping operations.

## Syntax
```sql
GROUPING_ID(column1, column2, ...)
```

```scala
// DataFrame API - typically used internally with cube/rollup operations
df.cube("col1", "col2").agg(expr("grouping_id(col1, col2)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| groupByExprs | Seq[Expression] | The sequence of expressions that represent the grouping columns for which the grouping ID is calculated |

## Return Type
Integer data type - returns a bitmask as an integer value representing the grouping combination.

## Supported Data Types
The `GroupingID` expression itself works with any data types for the input columns since it operates on the grouping metadata rather than the actual column values. The input expressions can be of any supported Spark data type.

## Algorithm
- Maintains references to a virtual `groupingIdAttribute` column rather than the actual input columns
- Acts as an `Unevaluable` expression, meaning it cannot be directly evaluated in normal expression contexts
- The actual evaluation is handled by specialized grouping operators (Cube, Rollup, GroupingSets)
- Generates a bitmask where each bit position corresponds to a grouping expression
- Returns an integer representing which columns are active in the current grouping level

## Partitioning Behavior
- Does not preserve partitioning as it's typically used in aggregation contexts
- Requires shuffle operations when used with CUBE, ROLLUP, or GROUPING SETS
- The expression itself doesn't directly affect partitioning but is used within aggregation operators that do

## Edge Cases
- **Null handling**: The expression itself is marked as non-nullable (`nullable = false`) since it returns grouping metadata rather than data-dependent values
- **Empty input**: When used with empty grouping expressions, would return 0
- **Unevaluable context**: Throws evaluation exceptions if used outside of proper grouping contexts since it extends `Unevaluable`
- **Virtual column dependency**: Relies on the presence of the virtual `groupingIdAttribute` in the execution context

## Code Generation
This expression does **not** support direct code generation since it extends `Unevaluable`. The code generation is handled by the parent grouping operators (Aggregate with Cube/Rollup/GroupingSets) that replace this expression with actual computed values during physical plan execution.

## Examples
```sql
-- Example with CUBE - grouping_id identifies aggregation levels
SELECT col1, col2, SUM(value), GROUPING_ID(col1, col2)
FROM table
GROUP BY CUBE(col1, col2);

-- Example with ROLLUP
SELECT dept, category, SUM(sales), GROUPING_ID(dept, category)
FROM sales_table  
GROUP BY ROLLUP(dept, category);
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.cube("department", "category")
  .agg(
    sum("sales").as("total_sales"),
    expr("grouping_id(department, category)").as("grouping_level")
  )
```

## See Also
- `Grouping` - Related expression for checking individual column grouping status
- `Cube` - Physical operator that utilizes GroupingID
- `Rollup` - Physical operator that utilizes GroupingID  
- `GroupingSets` - Physical operator that utilizes GroupingID
- `VirtualColumn.groupingIdAttribute` - The virtual column reference used internally