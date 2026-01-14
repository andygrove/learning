# Or

## Overview
The Or expression implements the logical OR operation between two boolean expressions. It follows three-valued logic (3VL) rules, where the result can be true, false, or null depending on the input values and their nullability.

## Syntax
```sql
expression1 OR expression2
-- Alternative symbol syntax
expression1 || expression2
```

```scala
// DataFrame API
col("column1") || col("column2")
// or using the or method
col("column1").or(col("column2"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | Left operand boolean expression |
| right | Expression | Right operand boolean expression |

## Return Type
BooleanType (can be true, false, or null)

## Supported Data Types

- BooleanType for both left and right operands

## Algorithm

- If the left operand evaluates to true, return true immediately (short-circuit evaluation)

- If the left operand is not true, evaluate the right operand

- If the right operand evaluates to true, return true

- If both operands are non-null and neither is true, return false

- If either operand is null and neither evaluates to true, return null

## Partitioning Behavior

- This expression preserves partitioning as it operates on individual rows

- Does not require shuffle operations

- Can be pushed down to data sources for predicate pushdown optimization

## Edge Cases

- **Null handling**: Follows SQL three-valued logic where `true OR null = true`, `false OR null = null`, and `null OR null = null`

- **Short-circuit evaluation**: If the left operand is true, the right operand is not evaluated

- **Type safety**: Both operands must be boolean expressions; type mismatches are caught at analysis time

## Code Generation
This expression supports Tungsten code generation with optimized paths for both nullable and non-nullable operands. The generated code includes short-circuit evaluation and efficient null handling without falling back to interpreted mode.

## Examples
```sql
-- Basic OR operation
SELECT true OR false;  -- Result: true

-- OR with NULL values
SELECT false OR NULL;  -- Result: NULL
SELECT true OR NULL;   -- Result: true

-- Using in WHERE clauses
SELECT * FROM table WHERE status = 'active' OR priority = 'high';

-- Complex expressions
SELECT * FROM table WHERE (age > 65 OR income < 30000) OR status = 'special';
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Basic OR operation
df.filter(col("status") === "active" || col("priority") === "high")

// Using or method
df.filter(col("status").equalTo("active").or(col("priority").equalTo("high")))

// Complex boolean logic
df.filter((col("age") > 65 || col("income") < 30000) || col("status") === "special")
```

## See Also

- And - Logical AND operation
- Not - Logical NOT operation  
- BooleanExpression - Base trait for boolean expressions
- Predicate - Interface for filter predicates