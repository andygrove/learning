# LateralSubquery

## Overview
A LateralSubquery represents a subquery that can return multiple rows and columns and has access to columns from the outer query. This expression is designed to be rewritten as a join with the outer query during the query optimization phase rather than being directly evaluated.

## Syntax
```sql
-- Used internally during query planning for LATERAL subqueries
SELECT * FROM table1, LATERAL (SELECT * FROM table2 WHERE table2.id = table1.id)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| plan | LogicalPlan | The logical plan representing the subquery |
| outerAttrs | Seq[Expression] | Expressions from the outer query that the subquery references |
| exprId | ExprId | Unique identifier for this expression, used in explain output |
| joinCond | Seq[Expression] | Join conditions between the subquery and outer query |
| hint | Option[HintInfo] | Optional hint information for query optimization |

## Return Type
Returns a StructType composed of all output columns from the subquery's logical plan. The expression is always nullable.

## Supported Data Types
Supports any data types that can be output by the underlying logical plan, as the return type is dynamically determined from the plan's output schema.

## Algorithm

- Inherits from SubqueryExpression and is marked as Unevaluable, meaning it cannot be directly executed
- During query optimization, the Catalyst optimizer rewrites this expression as a join operation
- The outerAttrs parameter allows the subquery to reference columns from the outer query scope
- Join conditions are stored separately to facilitate the rewriting process
- Canonicalization normalizes the plan and expressions while resetting the exprId to 0 for comparison purposes

## Partitioning Behavior
Since LateralSubquery is rewritten as a join during optimization:

- Does not directly affect partitioning as it's not executed in its original form
- The resulting join operation may require shuffling depending on the join conditions and current partitioning
- Partitioning behavior depends on the specific join strategy chosen after rewriting

## Edge Cases

- Cannot be directly evaluated due to Unevaluable trait - will throw an exception if evaluation is attempted
- Always returns nullable=true regardless of the actual nullability of subquery results
- Empty outerAttrs sequence indicates the subquery doesn't reference outer columns
- Missing hint information defaults to None and doesn't affect functionality

## Code Generation
This expression does not support code generation since it extends Unevaluable. The expression must be rewritten into a join operation during the optimization phase before code generation can occur.

## Examples
```scala
// Internal usage during query planning - not directly accessible to users
val subqueryPlan = // ... logical plan for subquery
val outerRefs = Seq(// ... expressions referencing outer query)
val lateralSubquery = LateralSubquery(
  plan = subqueryPlan,
  outerAttrs = outerRefs,
  exprId = NamedExpression.newExprId
)
```

```sql
-- SQL that would internally create LateralSubquery during planning
SELECT t1.id, sub.value 
FROM table1 t1, 
LATERAL (SELECT value FROM table2 t2 WHERE t2.parent_id = t1.id) sub
```

## See Also
- SubqueryExpression - Base class for all subquery expressions
- ScalarSubquery - For subqueries returning single values
- ListQuery - For subqueries used in IN expressions
- ExistsSubquery - For EXISTS clause subqueries