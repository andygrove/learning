# EqualNull

## Overview
EqualNull is a runtime-replaceable predicate expression that provides null-safe equality comparison between two expressions. It returns true when both operands are null or when both operands are equal, making it useful for comparisons where null values should be treated as equal to other null values.

## Syntax
```sql
equal_null(expr1, expr2)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The left operand for comparison |
| right | Expression | The right operand for comparison |

## Return Type
Boolean - returns true, false, or potentially null depending on the comparison result.

## Supported Data Types
All data types are supported since this expression delegates to EqualNullSafe, which can compare any two expressions of compatible types:

- Numeric types (byte, short, int, long, float, double, decimal)
- String types
- Boolean
- Date and timestamp types
- Binary data
- Complex types (arrays, maps, structs)
- Null values

## Algorithm

- The expression is implemented as a RuntimeReplaceable that delegates to EqualNullSafe
- During query planning, EqualNull is replaced with EqualNullSafe(left, right)
- The actual comparison logic is handled by the EqualNullSafe expression
- Returns true if both operands are null
- Returns true if both operands are non-null and equal
- Returns false otherwise

## Partitioning Behavior
This expression does not directly affect partitioning behavior:

- Does not preserve partitioning when used in transformations
- Does not require shuffle operations by itself
- When used in joins or filters, may influence partitioning strategy of parent operations

## Edge Cases

- Null handling: Returns true when both operands are null (unlike standard equality)
- Mixed null values: Returns false when one operand is null and the other is not
- Type compatibility: Follows Spark's type coercion rules for comparison
- Complex types: Performs deep equality comparison for nested structures

## Code Generation
This expression supports code generation through its replacement expression EqualNullSafe, which can generate efficient Tungsten code for the null-safe equality comparison.

## Examples
```sql
-- Basic usage
SELECT equal_null(1, 1); -- true
SELECT equal_null(1, 2); -- false

-- Null handling
SELECT equal_null(NULL, NULL); -- true
SELECT equal_null(1, NULL); -- false
SELECT equal_null(NULL, 1); -- false

-- With columns
SELECT equal_null(col1, col2) FROM table_name;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("equal_null(col1, col2)"))
df.filter(expr("equal_null(status, 'active')"))
```

## See Also

- EqualNullSafe - The underlying implementation expression
- EqualTo - Standard equality operator that returns null for null operands
- IsNull - Checks if an expression is null
- Coalesce - Handles null value replacement