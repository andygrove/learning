# Nvl2

## Overview
The `Nvl2` expression provides a conditional replacement based on whether the first expression is null or not. If the first expression is not null, it returns the second expression; otherwise, it returns the third expression. This is a runtime-replaceable expression that gets transformed into an `If(IsNotNull(expr1), expr2, expr3)` construct during query planning.

## Syntax
```sql
NVL2(expr1, expr2, expr3)
```

```scala
// DataFrame API
col("column").isNotNull.when(col("expr2")).otherwise(col("expr3"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr1 | Expression | The expression to test for null |
| expr2 | Expression | The value to return if expr1 is not null |
| expr3 | Expression | The value to return if expr1 is null |

## Return Type
The return type is determined by the common type resolution between `expr2` and `expr3`. The expression system will attempt to find a compatible type that both expressions can be cast to.

## Supported Data Types
All data types are supported for `expr1` since null checking is universal. The `expr2` and `expr3` expressions must be of compatible types that can be resolved to a common type through Spark's type coercion rules.

## Algorithm

- Evaluate `expr1` to determine if it produces a null value
- If `expr1` is not null, evaluate and return `expr2`
- If `expr1` is null, evaluate and return `expr3`
- The actual implementation transforms this into `If(IsNotNull(expr1), expr2, expr3)` at runtime
- Short-circuit evaluation ensures only the necessary expressions are computed

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require shuffle operations
- Maintains existing data partitioning
- Can be safely pushed down in query optimization
- Preserves partition pruning capabilities when used in filters

## Edge Cases

- If `expr1` evaluation throws an exception, the entire expression fails
- If `expr2` and `expr3` have incompatible types, compilation will fail during analysis
- Nested null checks are supported (expr2 or expr3 can also be Nvl2 expressions)
- The expression supports lazy evaluation - only the chosen branch is computed

## Code Generation
As a `RuntimeReplaceable` expression, `Nvl2` supports Tungsten code generation through its replacement expression `If(IsNotNull(expr1), expr2, expr3)`. The generated code will include optimized null checking and branching logic.

## Examples
```sql
-- Replace null salary with 0, or use bonus if salary exists
SELECT NVL2(salary, bonus, 0) as final_amount FROM employees;

-- String replacement based on null check
SELECT NVL2(middle_name, CONCAT(first_name, ' ', middle_name, ' ', last_name), 
            CONCAT(first_name, ' ', last_name)) as full_name FROM users;
```

```scala
// DataFrame API equivalent
import org.apache.spark.sql.functions._

df.select(
  when(col("salary").isNotNull, col("bonus"))
    .otherwise(lit(0))
    .alias("final_amount")
)

// Using conditional logic
df.select(
  when(col("middle_name").isNotNull, 
    concat(col("first_name"), lit(" "), col("middle_name"), lit(" "), col("last_name")))
    .otherwise(concat(col("first_name"), lit(" "), col("last_name")))
    .alias("full_name")
)
```

## See Also

- `Nvl` - Two-argument null replacement
- `If` - General conditional expression  
- `Coalesce` - Multi-argument null replacement
- `IsNotNull` - Null checking predicate
- `CaseWhen` - Multi-branch conditional logic