# InSubquery

## Overview

The `InSubquery` expression evaluates to `true` if the specified values are found in the result set of a subquery. This is a predicate expression that implements the SQL `IN` operator with subquery functionality, allowing for membership testing against dynamically computed result sets.

## Syntax

```sql
expression IN (SELECT ...)
(expr1, expr2, ...) IN (SELECT col1, col2, ... FROM table WHERE condition)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `values` | `Seq[Expression]` | The expressions to test for membership in the subquery results |
| `query` | `ListQuery` | The subquery that returns a list of values to check against |

## Return Type

Returns `BooleanType` - `true` if the values exist in the subquery result set, `false` otherwise, or `null` if nullability conditions are met.

## Supported Data Types

Supports any data types that can be compared for equality and have ordering semantics. The expression requires:

- Values and subquery columns must have matching data types
- All data types must support ordering operations
- Number of values must match the number of columns returned by the subquery

## Algorithm

- Creates a structured representation of multiple values using `CreateNamedStruct` for multi-column comparisons or uses the single value directly

- Validates that the number of input values matches the number of columns returned by the subquery

- Performs structural data type comparison between values and subquery output, ignoring nullability

- Checks that all data types support ordering operations required for membership testing

- Defers actual evaluation to the query execution engine as this is an `Unevaluable` expression

## Partitioning Behavior

This expression affects partitioning as follows:

- Does not preserve partitioning due to subquery dependency
- May require shuffle operations depending on the subquery implementation
- Subquery evaluation strategy determines the actual partitioning impact

## Edge Cases

- **Null handling**: Nullability depends on the `LEGACY_IN_SUBQUERY_NULLABILITY` configuration setting. When disabled (default), considers nullability of both values and subquery outputs. When enabled, only considers left-hand side nullability for legacy compatibility

- **Length mismatch**: Throws `DataTypeMismatch` error when the number of values doesn't match the number of subquery columns

- **Type mismatch**: Validates structural data type equality and reports specific mismatched columns in error messages

- **Empty subquery**: Returns `false` when subquery returns no results (standard SQL behavior)

## Code Generation

This expression is marked as `Unevaluable`, meaning it does not support direct code generation. The expression is transformed during query planning phases into executable operators that handle the subquery evaluation and membership testing.

## Examples

```sql
-- Single value IN subquery
SELECT * FROM orders WHERE customer_id IN (SELECT id FROM premium_customers);

-- Multiple values IN subquery  
SELECT * FROM products WHERE (category_id, supplier_id) IN (
  SELECT cat_id, sup_id FROM active_combinations
);
```

```scala
// DataFrame API usage (typically generated internally)
import org.apache.spark.sql.catalyst.expressions._
import org.apache.spark.sql.catalyst.plans.logical._

// This expression is typically created during SQL parsing
// and not directly instantiated in DataFrame API
val inSubquery = InSubquery(
  values = Seq(col("customer_id").expr),
  query = ListQuery(subqueryPlan)
)
```

## See Also

- `In` - For IN expressions with literal value lists
- `Exists` - For existential subquery predicates  
- `ScalarSubquery` - For subqueries returning single values
- `ListQuery` - The subquery container used by this expression