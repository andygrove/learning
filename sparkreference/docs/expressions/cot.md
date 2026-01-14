# Cot

## Overview
The `Cot` expression computes the cotangent of a numeric value. It calculates the reciprocal of the tangent function, mathematically equivalent to `1/tan(x)` or `cos(x)/sin(x)`.

## Syntax
```sql
COT(expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("COT(column_name)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Numeric | The input value in radians for which to compute the cotangent |

## Return Type
`DoubleType` - Returns a double-precision floating-point number.

## Supported Data Types

- Numeric types (IntegerType, LongType, FloatType, DoubleType, DecimalType)
- Input values are automatically cast to Double for computation

## Algorithm

- Takes the input numeric value as radians
- Computes the tangent using `math.tan(x)`
- Calculates the reciprocal: `1 / math.tan(x)`
- Returns the result as a Double value
- Supports Catalyst code generation for optimized execution

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it operates on individual row values
- Does not require shuffle operations
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null if input is null
- **Zero tangent**: Returns positive or negative infinity when `tan(x) = 0` (e.g., at multiples of π)
- **Overflow behavior**: May return `Double.PositiveInfinity` or `Double.NegativeInfinity` for certain inputs
- **NaN handling**: Returns `NaN` for invalid mathematical operations

## Code Generation
This expression supports Catalyst code generation (Tungsten). The `doGenCode` method generates optimized Java bytecode using `java.lang.Math.tan()` for better performance compared to interpreted execution.

## Examples
```sql
-- Basic cotangent calculation
SELECT COT(1);
-- Result: 0.6420926159343306

-- Using with PI for known values
SELECT COT(PI()/4);
-- Result: 1.0 (cotangent of 45 degrees)

-- Cotangent of PI/2 approaches infinity
SELECT COT(PI()/2);
-- Result: 6.123233995736766E-17 (very close to 0, tan(π/2) approaches infinity)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = Seq(1.0, Math.PI/4, Math.PI/2).toDF("angle")
df.select(col("angle"), expr("COT(angle)").as("cotangent")).show()

// Using with mathematical expressions
df.select(expr("COT(PI()/6)").as("cot_30_degrees")).show()
```

## See Also

- `Tan` - Tangent function (reciprocal of cotangent)
- `Sin` - Sine function
- `Cos` - Cosine function
- Other trigonometric expressions in the `math_funcs` group