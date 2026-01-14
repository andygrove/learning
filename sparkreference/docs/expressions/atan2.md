# Atan2

## Overview
The `ATAN2` expression computes the arctangent of the quotient of two numeric values, returning the angle (in radians) whose tangent is the quotient of the specified y and x coordinates. This function handles the signs of both arguments to determine the quadrant of the result, providing a result in the range [-π, π].

## Syntax
```sql
ATAN2(y, x)
```

```scala
atan2(y_column, x_column)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| y | Double | The y-coordinate value (first argument) |
| x | Double | The x-coordinate value (second argument) |

## Return Type
Returns a `Double` representing the angle in radians.

## Supported Data Types
Supports numeric data types that can be converted to `Double`:

- Double
- Float  
- Integer
- Long
- Short
- Byte
- Decimal (converted to Double)

## Algorithm
The expression is evaluated using the following process:

- Both input arguments are cast to `Double` type
- A special normalization is applied by adding `0.0` to each argument to handle the difference between `-0.0` and `0.0` in codegen
- The standard `java.lang.Math.atan2()` function is called with the normalized arguments
- The result is returned as a `Double` in the range [-π, π]

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle
- Maintains existing partitioning scheme
- Can be evaluated independently on each partition

## Edge Cases

- **Null handling**: If either argument is null, the result is null
- **Zero handling**: Special normalization (`+ 0.0`) ensures consistent behavior between `-0.0` and `0.0` across interpreted and codegen execution
- **Infinite values**: Follows standard IEEE 754 behavior for infinite inputs
- **Both arguments zero**: Returns `0.0` when both arguments are zero

## Code Generation
This expression supports Tungsten code generation for optimized performance. The generated code uses `java.lang.Math.atan2()` with the same normalization applied to handle zero values consistently.

## Examples
```sql
-- Basic arctangent calculation
SELECT ATAN2(1, 1);
-- Result: 0.7853981633974483 (π/4)

-- Handling different quadrants  
SELECT ATAN2(1, -1);
-- Result: 2.356194490192345 (3π/4)

-- Zero case example from source
SELECT ATAN2(0, 0);
-- Result: 0.0
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.atan2

df.select(atan2($"y_col", $"x_col"))

// With literal values
df.select(atan2(lit(1.0), lit(1.0)))
```

## See Also

- `ATAN` - Single-argument arctangent function
- `SIN`, `COS`, `TAN` - Other trigonometric functions
- `PI` - Mathematical constant π
- `DEGREES`, `RADIANS` - Angle unit conversion functions