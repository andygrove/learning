# If

## Overview
The If expression is a conditional expression that evaluates a boolean predicate and returns one of two values based on the result. It implements the standard ternary conditional logic where a true predicate returns the first value, and a false predicate returns the second value.

## Syntax
```sql
IF(condition, true_value, false_value)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| predicate | Boolean | The condition to evaluate |
| trueValue | Any | The value to return if the predicate is true |
| falseValue | Any | The value to return if the predicate is false |

## Return Type
Returns the unified data type of the `trueValue` and `falseValue` expressions after type merging. The return type is nullable if either the true or false value expressions are nullable.

## Supported Data Types

- Predicate must be of BooleanType
- True and false value expressions must have compatible types that can be merged through type coercion
- All primitive and complex data types are supported for the value expressions

## Algorithm

- The predicate expression is always evaluated first
- If the predicate evaluates to `true`, the trueValue expression is evaluated and returned
- If the predicate evaluates to `false` or `null`, the falseValue expression is evaluated and returned
- Only one of the value expressions is evaluated per row (lazy evaluation)
- Type coercion is applied to ensure both value expressions have the same data type

## Partitioning Behavior
The If expression preserves partitioning characteristics:

- Does not require shuffle operations
- Maintains existing partitioning schemes
- Does not affect data distribution across partitions

## Edge Cases

- If the predicate is `null`, the expression returns the false value
- The result is `null` only if the selected branch (true or false value) evaluates to `null`
- Type validation ensures both value expressions can be coerced to a common type
- The predicate must be exactly BooleanType - no implicit conversion from other types

## Code Generation
This expression supports full Tungsten code generation through the `doGenCode` method. It generates efficient Java code that:

- Evaluates the predicate condition first
- Uses conditional branching to evaluate only the selected value expression
- Properly handles null values and type conversions

## Examples
```sql
-- Basic conditional logic
SELECT IF(age >= 18, 'Adult', 'Minor') AS category FROM users;

-- Null handling
SELECT IF(score IS NOT NULL, score, 0) AS final_score FROM tests;

-- Nested conditions
SELECT IF(status = 'ACTIVE', IF(premium, 'Premium User', 'Regular User'), 'Inactive') FROM accounts;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(when(col("age") >= 18, "Adult").otherwise("Minor").as("category"))

// Using expr for IF function
df.select(expr("IF(score IS NOT NULL, score, 0)").as("final_score"))
```

## See Also

- CaseWhen - For multiple conditional branches
- Coalesce - For null value handling
- When/Otherwise - DataFrame API equivalent for conditional logic