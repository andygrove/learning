# Logarithm

## Overview
The Logarithm expression computes the logarithm of a value with a specified base. It supports both custom base logarithms and natural logarithm (using Euler's number as the base). The expression returns null if either the base or the value is less than or equal to zero.

## Syntax
```sql
LOG(base, value)
LN(value)  -- natural logarithm shorthand
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(log(base_col, value_col))
df.select(log(value_col))  // natural logarithm
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| base | Expression (Double) | The base of the logarithm. Must be greater than 0. For natural log, uses Euler's number |
| value | Expression (Double) | The value to compute the logarithm for. Must be greater than 0 |

## Return Type
Double - returns the logarithm result as a double-precision floating point number, or null for invalid inputs.

## Supported Data Types

- Numeric types that can be cast to Double
- Both arguments must evaluate to numeric values
- Input values are internally converted to Double for computation

## Algorithm

- Validates that both base and value are greater than 0.0
- For natural logarithm: uses `StrictMath.log(value)` directly when base is Euler's number
- For custom base: computes `StrictMath.log(value) / StrictMath.log(base)` using change of base formula  
- Returns null immediately if either argument is <= 0.0
- Unlike Hive, supports logarithm bases in the range (0.0, 1.0]

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it's a deterministic row-level transformation
- Does not require shuffle operations
- Can be pushed down in query optimization

## Edge Cases

- Returns null if base <= 0.0 or value <= 0.0
- Handles null inputs through inherited null-safe evaluation from BinaryMathExpression
- Uses StrictMath for consistent cross-platform behavior
- Supports bases in (0.0, 1.0] range, differing from some other SQL implementations
- Special optimization for natural logarithm case (single argument constructor)

## Code Generation
This expression supports Tungsten code generation with specialized optimizations:

- Generated code includes null-safety checks inline
- Optimized code path for natural logarithm (Euler base) case
- Falls back to `StrictMath.log()` calls in generated code for performance
- Avoids method call overhead through direct Java math library usage

## Examples
```sql
-- Basic logarithm with base 10
SELECT LOG(10, 100);  -- Returns 2.0

-- Natural logarithm
SELECT LN(2.718281828);  -- Returns ~1.0

-- Logarithm with base 2
SELECT LOG(2, 8);  -- Returns 3.0

-- Invalid inputs return null
SELECT LOG(-1, 10);  -- Returns null
SELECT LOG(10, -5);  -- Returns null
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Custom base logarithm
df.select(log(lit(10), col("value")))

// Natural logarithm  
df.select(log(col("value")))

// With column-based base
df.select(log(col("base"), col("value")))
```

## See Also

- `Exp` - exponential function (inverse of natural logarithm)
- `Log10` - base-10 logarithm specialized expression
- `Log2` - base-2 logarithm specialized expression  
- `Pow` - power function
- `EulerNumber` - Euler's number constant expression