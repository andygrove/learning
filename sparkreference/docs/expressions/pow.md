# Pow

## Overview
The `Pow` expression computes the value of the first argument raised to the power of the second argument. It performs exponentiation using Java's `StrictMath.pow` function to ensure consistent results across platforms.

## Syntax
```sql
POWER(base, exponent)
-- or
POW(base, exponent)
```

```scala
pow(base, exponent)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| base | Numeric | The base value to be raised to a power |
| exponent | Numeric | The exponent to which the base is raised |

## Return Type
Double - returns a double-precision floating-point value representing the result of base^exponent.

## Supported Data Types

- Numeric types (byte, short, int, long, float, double, decimal)
- Inputs are converted to double for computation

## Algorithm

- Converts both input arguments to double-precision floating-point values
- Delegates computation to Java's `StrictMath.pow(double a, double b)` method
- `StrictMath.pow` ensures IEEE 754 compliance and consistent results across platforms
- Returns the computed result as a double value
- Inherits null handling from parent `BinaryMathExpression` class

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffling between partitions
- Can be computed independently on each partition
- Does not affect data distribution or partitioning scheme

## Edge Cases

- Returns null if either input argument is null
- Returns 1.0 when exponent is 0 (including 0^0 = 1.0)
- Returns positive infinity for overflow conditions
- Returns 0.0 for underflow conditions
- Follows IEEE 754 standards for special cases (NaN, infinity handling)
- Negative base with fractional exponent may return NaN

## Code Generation
This expression supports Tungsten code generation:

- Implements `doGenCode` method for optimized code generation
- Generates direct calls to `java.lang.StrictMath.pow` in generated code
- Avoids interpreted execution overhead in code-generated queries

## Examples
```sql
-- Basic exponentiation
SELECT POWER(2, 3);
-- Returns: 8.0

-- Square root using fractional exponent
SELECT POWER(16, 0.5);
-- Returns: 4.0

-- Negative exponent
SELECT POWER(2, -3);
-- Returns: 0.125
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.pow

df.select(pow(col("base_column"), col("exponent_column")))

// With literal values
df.select(pow(col("value"), lit(2)))
```

## See Also

- `Sqrt` - Square root function
- `Exp` - Exponential function (e^x)
- Other mathematical expressions in the `math_funcs` group