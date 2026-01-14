# NullIf

## Overview
The `NullIf` expression compares two expressions and returns NULL if they are equal, otherwise returns the first expression. This is a conditional function that provides a way to replace specific values with NULL based on equality comparison.

## Syntax
```sql
NULLIF(expr1, expr2)
```

```scala
// DataFrame API
nullIf(col("column1"), col("column2"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The primary expression to evaluate and potentially return |
| right | Expression | The comparison expression used to determine equality |

## Return Type
Returns the same data type as the left (first) expression, or NULL if the expressions are equal.

## Supported Data Types
All data types are supported as long as both expressions have comparable types that can be evaluated for equality using the `EqualTo` expression.

## Algorithm

- Evaluates both the left and right expressions for equality using `EqualTo` comparison

- If the expressions are equal, returns a NULL literal with the same data type as the left expression

- If the expressions are not equal, returns the value of the left expression

- Uses conditional expression rewriting based on the `ALWAYS_INLINE_COMMON_EXPR` configuration setting

- When inlining is disabled, uses `With` expression to avoid re-evaluating the left expression

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require shuffle operations

- Maintains existing data partitioning since it only transforms values within partitions

- The partitioning key remains unchanged unless the partitioning column itself is being transformed

## Edge Cases

- When left expression is NULL and right expression is NULL, returns NULL (since NULL equals NULL in this context)

- When left expression is NULL and right expression is not NULL, returns NULL

- When left expression is not NULL and right expression is NULL, returns the left expression value

- The expression handles type coercion implicitly through the underlying `EqualTo` comparison

- Uses `Literal.create(null, left.dataType)` to ensure proper NULL typing

## Code Generation
This is a `RuntimeReplaceable` expression, which means it is replaced with simpler expressions (`If`, `EqualTo`, and `Literal`) during query planning. The replacement expressions support Tungsten code generation, so `NullIf` effectively benefits from code generation through its replacements.

## Examples
```sql
-- Basic usage
SELECT NULLIF(2, 2);
-- Returns: NULL

SELECT NULLIF(1, 2);
-- Returns: 1

-- With column data
SELECT NULLIF(salary, 0) FROM employees;
-- Returns NULL for employees with 0 salary, otherwise returns actual salary
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(nullIf(col("value"), lit(0)))

// Replace specific values with NULL
df.withColumn("cleaned_score", nullIf(col("score"), lit(-1)))
```

## See Also

- `If` - Conditional expression used internally by NullIf
- `Coalesce` - Returns first non-null expression from a list
- `IsNull` / `IsNotNull` - Null checking expressions
- `EqualTo` - Equality comparison expression used internally