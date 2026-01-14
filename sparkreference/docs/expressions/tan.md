# Tan

## Overview
The `Tan` expression computes the trigonometric tangent of a numeric value. It is a unary mathematical expression that takes a single numeric input representing an angle in radians and returns its tangent value.

## Syntax
```sql
TAN(expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.tan
df.select(tan($"angle_column"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | A numeric expression representing an angle in radians |

## Return Type
Returns a `DoubleType` value representing the tangent of the input angle.

## Supported Data Types

- ByteType
- ShortType  
- IntegerType
- LongType
- FloatType
- DoubleType
- DecimalType (converted to Double internally)

## Algorithm

- Inherits from `UnaryMathExpression` which provides the evaluation framework
- Uses Java's `math.tan` function for the actual computation
- Input values are converted to Double type before computation
- Returns the tangent value as a Double result
- Leverages Catalyst's expression evaluation infrastructure for optimization

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require shuffle operations
- Maintains existing data partitioning since it's a row-level transformation
- Can be pushed down in query optimization when appropriate

## Edge Cases

- **Null handling**: Returns null if the input expression evaluates to null
- **Infinity cases**: Returns positive or negative infinity for angles where tangent is undefined (e.g., π/2, 3π/2)
- **NaN handling**: Returns NaN (Not a Number) if input is NaN
- **Overflow behavior**: Follows IEEE 754 floating-point standards for extreme values
- **Zero input**: `TAN(0)` returns `0.0` as expected

## Code Generation
This expression supports Catalyst code generation (Tungsten):

- Inherits code generation capabilities from `UnaryMathExpression`
- Generates efficient Java bytecode for the `math.tan` operation
- Falls back to interpreted mode only in exceptional cases where code generation fails

## Examples
```sql
-- Basic usage
SELECT TAN(0) AS tan_zero;
-- Result: 0.0

-- With column data
SELECT angle, TAN(angle) AS tangent_value
FROM trigonometry_table;

-- Using π/4 (45 degrees)
SELECT TAN(PI()/4) AS tan_45_degrees;
-- Result: 1.0
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic tangent calculation
df.select(tan(col("angle_radians")))

// With alias
df.select(tan(col("angle_radians")).alias("tangent_value"))

// Combined with other math functions  
df.select(
  col("angle"),
  tan(col("angle")).alias("tangent"),
  cos(col("angle")).alias("cosine")
)
```

## See Also

- `Sin` - Computes sine of an angle
- `Cos` - Computes cosine of an angle  
- `Asin`, `Acos`, `Atan` - Inverse trigonometric functions
- `Degrees`, `Radians` - Angle unit conversion functions