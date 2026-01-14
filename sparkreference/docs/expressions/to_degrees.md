# ToDegrees

## Overview
The `ToDegrees` expression converts an angle value from radians to degrees. This is a unary mathematical expression that applies the standard radian-to-degree conversion formula by multiplying the input by 180/π.

## Syntax
```sql
DEGREES(angle_in_radians)
```

```scala
degrees(col("angle_column"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The angle value in radians to convert to degrees |

## Return Type
Double - returns a floating-point number representing the angle in degrees.

## Supported Data Types

- Numeric types (Int, Long, Float, Double, Decimal)

- The expression internally uses `math.toDegrees` which operates on Double values

- Non-numeric inputs will cause a cast or runtime error

## Algorithm

- Takes the input angle value in radians as a Double

- Applies the Java `math.toDegrees` function internally

- Uses the conversion formula: degrees = radians × (180/π)

- Returns the result as a Double value

- Inherits evaluation logic from `UnaryMathExpression` base class

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it's a unary expression that doesn't require data movement

- Does not require shuffle operations

- Can be applied per-partition independently

## Edge Cases

- Null input returns null (standard Spark null propagation)

- Handles positive and negative radian values correctly  

- Very large input values may result in overflow to infinity

- Very small input values near zero are handled precisely

- NaN input produces NaN output

## Code Generation
This expression supports Tungsten code generation through the `UnaryMathExpression` base class, which generates efficient native code for the mathematical operation rather than falling back to interpreted mode.

## Examples
```sql
-- Convert π radians to degrees
SELECT DEGREES(3.141592653589793);
-- Result: 180.0

-- Convert π/2 radians to degrees  
SELECT DEGREES(1.5707963267948966);
-- Result: 90.0

-- Handle negative values
SELECT DEGREES(-3.141592653589793);
-- Result: -180.0
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.degrees

df.select(degrees(col("radian_column")))

// Convert literal value
df.select(degrees(lit(math.Pi)))
```

## See Also

- `ToRadians` - converts degrees to radians (inverse operation)

- Other trigonometric functions: `Sin`, `Cos`, `Tan`

- `UnaryMathExpression` - base class for unary mathematical operations