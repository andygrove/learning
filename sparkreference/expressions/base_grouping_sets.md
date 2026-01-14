# BaseGroupingSets

## Overview
BaseGroupingSets is a placeholder expression trait for CUBE, ROLLUP, and GROUPING SETS operations in Apache Spark SQL. It serves as the base interface for advanced aggregation operations that generate multiple grouping combinations, and is replaced by the analyzer during query planning. This trait provides the foundation for SQL's advanced analytical grouping functions that create hierarchical aggregations.

## Syntax
```sql
-- CUBE syntax
GROUP BY CUBE(col1, col2, ...)

-- ROLLUP syntax  
GROUP BY ROLLUP(col1, col2, ...)

-- GROUPING SETS syntax
GROUP BY GROUPING SETS((col1), (col1, col2), ...)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | The grouping expressions that participate in the grouping sets |
| groupingSets | Seq[Seq[Expression]] | Abstract method defining the specific grouping combinations |
| selectedGroupByExprs | Seq[Seq[Expression]] | Abstract method defining the selected group by expressions for each grouping set |

## Return Type
Not applicable - this is a placeholder expression that throws `SparkUnsupportedOperationException` when evaluated. The actual return type depends on the concrete implementation (Cube, Rollup, or GroupingSets).

## Supported Data Types
Supports all data types that can be used in GROUP BY clauses, including:
- Primitive types (numeric, string, boolean, binary)
- Complex types (arrays, maps, structs) 
- Temporal types (date, timestamp)

## Algorithm
- Maintains `groupingSets` representing different grouping combinations
- Provides `groupByExprs` that returns distinct expressions based on semantic equality
- Defers to concrete implementations for specific grouping logic (cube vs rollup vs explicit sets)
- Uses `distinctGroupByExprs` to eliminate semantically equivalent expressions (e.g., `a * b` and `b * a`)
- Converts grouping sets to flattened indexes for efficient processing

## Partitioning Behavior
- **Requires shuffle**: All grouping sets operations require data shuffling to group by different column combinations
- **Does not preserve partitioning**: The multiple grouping combinations typically break existing partition schemes
- **Multiple aggregation phases**: May require multiple shuffle stages for complex grouping set combinations

## Edge Cases
- **Null handling**: Nullable is always true; null values participate in grouping operations
- **Unresolved children**: Throws assertion error if `groupByExprs` is called before children are resolved  
- **Empty grouping sets**: Supported and represents aggregation over entire dataset
- **Duplicate expressions**: Semantic equality is used to eliminate duplicates (e.g., `a + b` equals `b + a`)
- **Evaluation attempts**: Throws `SparkUnsupportedOperationException` since this is a placeholder

## Code Generation
Extends `CodegenFallback`, meaning this expression does not support Tungsten code generation and falls back to interpreted mode during the placeholder phase. Concrete implementations may have different codegen behavior.

## Examples
```sql
-- CUBE example - generates 2^n combinations
SELECT dept, job, SUM(salary) 
FROM employees 
GROUP BY CUBE(dept, job);
-- Generates: (dept,job), (dept), (job), ()

-- ROLLUP example - generates hierarchical combinations  
SELECT year, quarter, month, SUM(sales)
FROM sales_data
GROUP BY ROLLUP(year, quarter, month);
-- Generates: (year,quarter,month), (year,quarter), (year), ()

-- GROUPING SETS example - explicit combinations
SELECT region, product, SUM(revenue)
FROM sales 
GROUP BY GROUPING SETS((region), (product), (region, product));
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.groupBy(cube($"dept", $"job"))
  .agg(sum($"salary"))

df.groupBy(rollup($"year", $"quarter", $"month"))  
  .agg(sum($"sales"))

// Note: Direct BaseGroupingSets instantiation not exposed in public API
```

## See Also
- `Cube` - Concrete implementation for CUBE operations
- `Rollup` - Concrete implementation for ROLLUP operations  
- `GroupingSets` - Concrete implementation for explicit GROUPING SETS
- `Grouping` - Function to test if a column is aggregated in current grouping
- `GroupingID` - Function that returns the grouping level as a bitmask