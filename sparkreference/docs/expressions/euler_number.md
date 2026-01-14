# EulerNumber

## Overview
The EulerNumber expression represents Euler's number (e), the base of natural logarithms. This is a constant leaf expression that returns the mathematical constant e ≈ 2.718281828459045 without requiring any input parameters.

## Syntax
```sql
E()
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("E()"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | - | This expression takes no arguments |

## Return Type
`DoubleType` - Returns a double-precision floating-point representation of Euler's number.

## Supported Data Types
This expression does not accept input data types as it is a constant leaf expression that takes no parameters.

## Algorithm

- Extends `LeafMathExpression` with the constant value `math.E`

- Returns the pre-computed Java `Math.E` constant (2.718281828459045)

- No computation is performed at runtime as the value is constant

- Optimized during constant folding phase by Catalyst optimizer

- Uses the string representation "E" for code generation and SQL display

## Partitioning Behavior
This expression has no impact on partitioning behavior:

- Preserves existing partitioning schemes since it produces the same constant value

- Does not require data shuffling or repartitioning

- Can be evaluated independently on each partition

## Edge Cases

- Never returns null as it represents a mathematical constant

- No overflow or underflow concerns since it returns a fixed double value

- Always returns the same value regardless of input data or context

- No special handling required for empty datasets

## Code Generation
This expression does not utilize code generation as noted in the source comments. It is designed to be evaluated during the constant folding optimization phase rather than at runtime, making code generation unnecessary for this constant value.

## Examples
```sql
-- Basic usage
SELECT E();
-- Result: 2.718281828459045

-- Using in calculations
SELECT E() * 2;
-- Result: 5.436563656918090

-- Using in mathematical expressions
SELECT LOG(E());
-- Result: 1.0
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Select Euler's number
df.select(expr("E()")).show()

// Use in calculations
df.select(expr("E() * 2").alias("double_e")).show()

// Combine with other math functions
df.select(expr("LOG(E())").alias("natural_log_e")).show()
```

## See Also

- `Pi()` - Returns the mathematical constant π
- `Exp(expr)` - Returns e raised to the power of expr
- `Log(expr)` - Returns the natural logarithm using base e

---

# Pi

## Overview
The Pi expression represents the mathematical constant π (pi), the ratio of a circle's circumference to its diameter. This is a constant leaf expression that returns the value of π ≈ 3.141592653589793 without requiring any input parameters.

## Syntax
```sql
PI()
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("PI()"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | - | This expression takes no arguments |

## Return Type
`DoubleType` - Returns a double-precision floating-point representation of the mathematical constant π.

## Supported Data Types
This expression does not accept input data types as it is a constant leaf expression that takes no parameters.

## Algorithm

- Extends `LeafMathExpression` with the constant value `math.Pi`

- Returns the pre-computed Java `Math.PI` constant (3.141592653589793)

- No computation is performed at runtime as the value is constant

- Optimized during constant folding phase by Catalyst optimizer

- Uses the string representation "PI" for code generation and SQL display

## Partitioning Behavior
This expression has no impact on partitioning behavior:

- Preserves existing partitioning schemes since it produces the same constant value

- Does not require data shuffling or repartitioning

- Can be evaluated independently on each partition

## Edge Cases

- Never returns null as it represents a mathematical constant

- No overflow or underflow concerns since it returns a fixed double value

- Always returns the same value regardless of input data or context

- No special handling required for empty datasets

## Code Generation
This expression does not utilize code generation as explicitly noted in the source comments. The expression is designed to be evaluated only by the optimizer during constant folding, making runtime code generation unnecessary for this constant value.

## Examples
```sql
-- Basic usage
SELECT PI();
-- Result: 3.141592653589793

-- Using in geometric calculations
SELECT PI() * 2;
-- Result: 6.283185307179586

-- Calculate area of circle with radius 5
SELECT PI() * 5 * 5;
-- Result: 78.53981633974483
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Select Pi
df.select(expr("PI()")).show()

// Use in calculations
df.select(expr("PI() * 2").alias("two_pi")).show()

// Geometric calculations
df.select(expr("PI() * POWER(radius, 2)").alias("circle_area")).show()
```

## See Also

- `EulerNumber()` - Returns the mathematical constant e
- Trigonometric functions like `Sin(expr)`, `Cos(expr)`, `Tan(expr)`
- `Degrees(expr)` and `Radians(expr)` for angle conversions

---

# Acos

## Overview
The Acos expression computes the inverse cosine (arc cosine) of the input expression. It returns the angle in radians whose cosine equals the input value, equivalent to `java.lang.Math.acos()`.

## Syntax
```sql
ACOS(expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(acos(col("column_name")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Numeric | The input expression whose inverse cosine is to be calculated. Must be between -1 and 1 inclusive. |

## Return Type
`DoubleType` - Returns the arc cosine of the input as a double value in radians, ranging from 0 to π.

## Supported Data Types

- All numeric types (ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType)

- DecimalType with automatic promotion to DoubleType

- Input values are cast to Double before computation

## Algorithm

- Extends `UnaryMathExpression` with `math.acos` function

- Delegates computation to Java's `Math.acos()` method

- Converts input to double precision before applying the arc cosine function

- Returns result in radians within the range [0, π]

- Uses "ACOS" as the string representation for SQL and code generation

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffling as it operates row-by-row

- Maintains existing partition boundaries

- Can be evaluated independently within each partition

## Edge Cases

- Returns `NaN` for input values outside the valid domain [-1, 1]

- Returns `null` when input is `null`

- `ACOS(1.0)` returns `0.0` (angle whose cosine is 1)

- `ACOS(-1.0)` returns `π` (angle whose cosine is -1)

- `ACOS(0.0)` returns `π/2` (90 degrees in radians)

## Code Generation
This expression supports Tungsten code generation through the `UnaryMathExpression` base class, providing optimized runtime performance for the arc cosine computation.

## Examples
```sql
-- Basic usage
SELECT ACOS(1);
-- Result: 0.0

SELECT ACOS(0);
-- Result: 1.5707963267948966 (π/2)

SELECT ACOS(-1);
-- Result: 3.141592653589793 (π)

-- Invalid domain example
SELECT ACOS(2);
-- Result: NaN

-- Using with column data
SELECT name, ACOS(cosine_value) as angle_radians
FROM trigonometry_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic inverse cosine
df.select(acos(lit(1.0))).show()

// Apply to column
df.select(acos(col("cosine_values")).alias("angles")).show()

// Convert result to degrees
df.select(
  degrees(acos(col("cosine_values"))).alias("angles_degrees")
).show()

// Handle edge cases
df.select(
  when(col("value").between(-1.0, 1.0), acos(col("value")))
    .otherwise(lit(Double.NaN))
    .alias("safe_acos")
).show()
```

## See Also

- `Asin(expr)` - Inverse sine function
- `Atan(expr)` - Inverse tangent function
- `Cos(expr)` - Cosine function (inverse operation)
- `Degrees(expr)` - Convert radians to degrees
- `Pi()` - Mathematical constant π for angle calculations