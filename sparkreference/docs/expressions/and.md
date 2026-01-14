# And

## Overview
The `And` expression implements the logical AND operation between two boolean expressions. It follows SQL three-valued logic, returning `true` only when both operands are `true`, `false` when at least one operand is `false`, and `null` when the result is indeterminate due to null values.

## Syntax
```sql
expression1 AND expression2
```

```scala
// DataFrame API
col("column1") && col("column2")
// or
col("column1").and(col("column2"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | Left boolean expression operand |
| right | Expression | Right boolean expression operand |

## Return Type
`BooleanType` - Returns a boolean value or null

## Supported Data Types

- Input expressions must evaluate to `BooleanType`
- Both operands must be boolean expressions or convertible to boolean

## Algorithm

- Evaluates the left operand first for short-circuit optimization
- If left operand is `false`, immediately returns `false` without evaluating right operand
- If left operand is not `false`, evaluates the right operand
- If right operand is `false`, returns `false`
- If both operands are non-null and not `false`, returns `true`
- If either operand is null and neither is `false`, returns `null`

## Partitioning Behavior
- This expression preserves partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be pushed down to data sources as a filter predicate

## Edge Cases

- **Null handling**: Follows three-valued logic where `false AND null = false`, `true AND null = null`, `null AND false = false`, `null AND null = null`
- **Short-circuit evaluation**: If the left operand is `false`, the right operand is not evaluated
- **Type safety**: Both operands must be boolean expressions; type coercion is not performed

## Code Generation
This expression supports Tungsten code generation for optimized performance. It generates different code paths depending on whether the operands are nullable:

- For non-nullable operands: Generates simpler code without null checks
- For nullable operands: Generates comprehensive null-handling logic following three-valued logic rules

## Examples
```sql
-- Basic AND operation
SELECT true AND true;   -- Returns: true
SELECT true AND false;  -- Returns: false
SELECT false AND null;  -- Returns: false
SELECT true AND null;   -- Returns: null

-- Using in WHERE clause
SELECT * FROM table WHERE active AND verified;

-- Complex conditions
SELECT * FROM users WHERE age > 18 AND status = 'active';
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic AND operation
df.filter(col("active") && col("verified"))

// Multiple conditions
df.filter(col("age") > 18 && col("status") === "active")

// With null handling
df.select(col("flag1") && col("flag2") as "both_true")
```

## See Also

- `Or` - Logical OR operation
- `Not` - Logical NOT operation
- `BooleanExpression` - Base class for boolean expressions
- SQL three-valued logic documentation