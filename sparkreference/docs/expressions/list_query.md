# ListQuery

## Overview

`ListQuery` is a Catalyst expression that represents a subquery used in list-based operations, most commonly for `IN` and `EXISTS` clauses. It encapsulates a logical plan that produces a list of values to be compared against outer query expressions, enabling correlated and non-correlated subquery execution within Spark SQL.

## Syntax

```sql
-- IN subquery
SELECT * FROM table1 WHERE column IN (SELECT column FROM table2)

-- EXISTS subquery  
SELECT * FROM table1 WHERE EXISTS (SELECT 1 FROM table2 WHERE table1.id = table2.id)
```

```scala
// Created internally by Catalyst during query planning
// Not directly accessible via DataFrame API
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `plan` | `LogicalPlan` | The logical plan representing the subquery |
| `outerAttrs` | `Seq[Expression]` | References to outer query attributes used in correlation |
| `exprId` | `ExprId` | Unique identifier for this expression instance |
| `numCols` | `Int` | Number of columns in the original plan (-1 if unset) |
| `joinCond` | `Seq[Expression]` | Join conditions for correlated subqueries |
| `hint` | `Option[HintInfo]` | Optional query hints for optimization |

## Return Type

The return type depends on the number of columns in the subquery:

- Single column: Returns the data type of the first output column
- Multiple columns: Returns a `StructType` containing all column types

## Supported Data Types

Supports all Spark SQL data types as the subquery can contain any valid expressions. The specific data types depend on the columns selected in the subquery plan.

## Algorithm

- Executes the encapsulated logical plan to produce a dataset
- For single-column subqueries, returns the column values directly
- For multi-column subqueries, constructs struct values from all columns
- Handles correlation by binding outer attributes to the subquery execution context
- Applies join conditions when processing correlated subqueries

## Partitioning Behavior

- Does not preserve partitioning as it represents a subquery operation
- May require shuffle operations depending on the subquery complexity
- Correlated subqueries typically require broadcast or shuffle joins
- The actual partitioning behavior depends on the underlying logical plan execution

## Edge Cases

- **Null handling**: Nullability is undefined for standalone `ListQuery` execution and throws an assertion error in Spark 3.5+ unless legacy mode is enabled
- **Empty subquery**: Returns empty result set, which affects `IN` clause evaluation (returns false for all comparisons)
- **Unresolved state**: Expression remains unresolved until `numCols` is set to a valid value (not -1)
- **Multi-column correlation**: Properly handles complex correlation scenarios with multiple outer attributes

## Code Generation

This expression is marked as `Unevaluable`, meaning it cannot be directly evaluated and does not support code generation. It must be transformed into executable operations (like joins or broadcasts) during query planning phases.

## Examples

```sql
-- Simple IN subquery
SELECT name FROM employees 
WHERE department_id IN (SELECT id FROM departments WHERE budget > 100000);

-- Correlated EXISTS subquery
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- Multi-column subquery
SELECT * FROM products 
WHERE (category, supplier) IN (SELECT category, supplier FROM featured_products);
```

```scala
// Internal usage during Catalyst optimization
// ListQuery instances are created by the analyzer when processing subquery expressions
// Not directly instantiated in user code
```

## See Also

- `SubqueryExpression` - Base class for all subquery expressions
- `ScalarSubquery` - For scalar subquery expressions
- `Exists` - For EXISTS clause implementations
- `In` - For IN clause expressions that may contain ListQuery instances