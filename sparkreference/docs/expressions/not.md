# Not

## Overview
The `Not` expression implements logical negation in Spark SQL, inverting boolean values from TRUE to FALSE and vice versa. It follows three-valued logic semantics where NULL inputs produce NULL outputs, making it null-tolerant in its evaluation.

## Syntax
```sql
NOT column_name
NOT (expression)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.not
df.filter(not(col("boolean_column")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The boolean expression to negate |

## Return Type
BooleanType - Returns a boolean value or NULL.

## Supported Data Types
- BooleanType only (implicit casting is applied to convert other types to boolean when possible)

## Algorithm

- Evaluates the child expression first

- If the child evaluates to NULL, returns NULL (null-tolerant behavior)

- If the child evaluates to TRUE, returns FALSE

- If the child evaluates to FALSE, returns TRUE

- Applies algebraic optimizations during canonicalization by converting negated comparison operators to their opposites

## Partitioning Behavior
- Preserves partitioning as it operates on individual rows without requiring data redistribution

- Does not require shuffle operations

- Can be pushed down as a filter predicate to reduce data movement

## Edge Cases

- **Null handling**: NOT NULL evaluates to NULL, following SQL three-valued logic

- **Comparison optimization**: Negated comparisons are automatically converted (e.g., NOT (a > b) becomes a <= b)

- **Boolean casting**: Non-boolean inputs are implicitly cast to boolean type before evaluation

- **Nested negation**: Multiple NOT operations can be applied and will be evaluated sequentially

## Code Generation
Supports Tungsten code generation for optimal performance. The generated code directly applies the `!` operator on the boolean value, producing efficient bytecode without falling back to interpreted mode.

## Examples
```sql
-- Basic negation
SELECT NOT true;
-- FALSE

-- With NULL
SELECT NOT NULL;
-- NULL

-- Column negation
SELECT * FROM table WHERE NOT active;

-- Complex expression
SELECT NOT (age > 18 AND status = 'active') FROM users;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Simple negation
df.select(not(col("is_active")))

// In filter conditions
df.filter(not(col("is_deleted")))

// Complex expressions
df.filter(not(col("age") > 18 && col("status") === "active"))
```

## See Also
- Comparison operators (GreaterThan, LessThan, GreaterThanOrEqual, LessThanOrEqual)
- Logical operators (And, Or)
- IsNull, IsNotNull expressions