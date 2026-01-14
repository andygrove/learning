# ZeroIfNull

## Overview
The `ZeroIfNull` expression returns zero if the input expression evaluates to null, otherwise returns the original input value. This is a runtime-replaceable expression that internally uses the `Nvl` (NullValue) function with a literal zero as the replacement value.

## Syntax
```sql
ZEROIFNULL(expr)
```

```scala
// DataFrame API usage would be through SQL function
df.selectExpr("ZEROIFNULL(column_name)")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| input | Expression | The expression to evaluate for null values |

## Return Type
Returns the same data type as the input expression, or an integer zero (which may be cast to match the input type).

## Supported Data Types
Supports all data types that can be compared with null and are compatible with integer zero:

- Numeric types (byte, short, int, long, float, double, decimal)
- String types (with implicit conversion)
- Date/timestamp types (with implicit conversion)

## Algorithm

- Evaluate the input expression
- Check if the result is null
- If null, return literal zero value
- If not null, return the original input value
- The replacement logic is delegated to the `Nvl` expression internally

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle
- Maintains existing partition boundaries
- Can be applied per-partition independently
- Preserves data distribution patterns

## Edge Cases

- **Null input**: Returns 0 when input is null
- **Non-null input**: Returns the original value unchanged
- **Type compatibility**: Zero literal must be compatible with input data type
- **Nested nulls**: Only evaluates top-level null, not nulls within complex types
- **Expression evaluation**: Input expression is only evaluated once

## Code Generation
This expression supports Tungsten code generation through its `RuntimeReplaceable` trait, which delegates code generation to the underlying `Nvl` expression implementation.

## Examples
```sql
-- Basic usage
SELECT ZEROIFNULL(2);
-- Result: 2

-- With null value
SELECT ZEROIFNULL(NULL);
-- Result: 0

-- With column data
SELECT ZEROIFNULL(salary) FROM employees;
-- Returns 0 for null salaries, original values otherwise
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("ZEROIFNULL(amount)"))

// Alternative using coalesce
df.select(coalesce(col("amount"), lit(0)))
```

## See Also

- `Nvl` - The underlying null value replacement expression
- `Coalesce` - Returns first non-null value from multiple expressions
- `IsNull` - Tests for null values
- `IfNull` - Generic null replacement function