# ScalarSubquery

## Overview
ScalarSubquery represents a correlated scalar subquery expression in Spark SQL that returns a single value from a subquery. It extends SubqueryExpression and is used to handle subqueries that are expected to return at most one row and one column, with support for correlation predicates that reference outer query attributes.

## Syntax
```sql
-- Used implicitly in scalar subquery contexts
SELECT col1, (SELECT MAX(col2) FROM table2 WHERE table2.id = table1.id) 
FROM table1
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| plan | LogicalPlan | The logical plan representing the subquery |
| outerAttrs | Seq[Expression] | Sequence of expressions referencing outer query attributes for correlation |
| exprId | ExprId | Unique expression identifier for this subquery instance |
| joinCond | Seq[Expression] | Join conditions for correlating the subquery with outer query |
| hint | Option[HintInfo] | Optional hint information for query optimization |
| mayHaveCountBug | Option[Boolean] | Flag indicating potential count aggregation issues |
| needSingleJoin | Option[Boolean] | Flag indicating if LeftSingle join is needed when single row guarantee cannot be made |

## Return Type
Returns the data type of the first (and only) column in the subquery's schema. The expression is always nullable regardless of the underlying column's nullability.

## Supported Data Types
Supports any data type that can be returned by the subquery's single output column, including:

- Numeric types (IntegerType, LongType, DoubleType, DecimalType, etc.)
- String types (StringType, VarcharType, CharType)
- Date and timestamp types (DateType, TimestampType)
- Binary types (BinaryType)
- Complex types (ArrayType, MapType, StructType)

## Algorithm

- Validates that the subquery plan returns exactly one column, throwing QueryCompilationErrors if multiple columns are present
- Executes the subquery plan with correlation to outer attributes through outerAttrs and joinCond
- Returns the single scalar value from the subquery result
- Uses LeftSingle join when needSingleJoin is true to handle cases where single row guarantee cannot be made
- Applies canonicalization by normalizing the plan, outer attributes, join conditions, and resetting expression ID to 0

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve partitioning as it represents a subquery operation
- May require shuffle operations depending on the correlation predicates and join conditions
- The needSingleJoin flag can trigger specialized join operations that affect data distribution

## Edge Cases

- Null handling: Always returns nullable results even if the underlying column is non-nullable
- Empty subquery results: Returns null when the correlated subquery produces no rows
- Multiple rows: When needSingleJoin is not set and multiple rows are returned, behavior depends on the execution context and may result in runtime errors
- Zero columns: Throws QueryCompilationErrors.subqueryReturnMoreThanOneColumn when the subquery schema has no fields
- Correlation: Handles complex correlation scenarios through outerAttrs and joinCond parameters

## Code Generation
This expression extends Unevaluable, indicating it cannot be directly evaluated through code generation. Instead, it must be rewritten into physical join operations during query planning phases like RewriteCorrelatedScalarSubquery.

## Examples
```sql
-- Correlated scalar subquery
SELECT employee_name, 
       (SELECT AVG(salary) FROM employees e2 WHERE e2.dept_id = e1.dept_id) as avg_dept_salary
FROM employees e1;

-- Scalar subquery in WHERE clause
SELECT * FROM products 
WHERE price > (SELECT AVG(price) FROM products WHERE category = 'electronics');
```

```scala
// ScalarSubquery is typically created internally during query analysis
// Not directly instantiated in DataFrame API, but used in SQL parsing
val df = spark.sql("""
  SELECT col1, (SELECT MAX(col2) FROM table2 WHERE table2.id = table1.id) as max_col2
  FROM table1
""")
```

## See Also

- SubqueryExpression - Base class for all subquery expressions
- ExistsSubquery - For EXISTS subquery expressions  
- ListQuery - For IN subquery expressions
- RewriteCorrelatedScalarSubquery - Optimizer rule that rewrites scalar subqueries
- PullupCorrelatedPredicates - Rule that sets the needSingleJoin flag