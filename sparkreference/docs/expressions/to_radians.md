# ToRadians

## Overview
The ToRadians expression converts angle values from degrees to radians. It is a unary mathematical expression that applies the standard mathematical conversion formula using Scala's `math.toRadians` function.

## Syntax
```sql
RADIANS(angle_in_degrees)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.radians
df.select(radians(col("degrees_column")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The angle value in degrees to be converted to radians |

## Return Type
Double - returns the angle converted to radians as a double-precision floating-point number.

## Supported Data Types

- Numeric types (Int, Long, Float, Double)
- Any expression that can be cast to a numeric type

## Algorithm

- Takes the input angle value in degrees as a Double
- Applies the mathematical conversion formula: radians = degrees × (π / 180)
- Uses Scala's built-in `math.toRadians` function for the conversion
- Returns the result as a Double value
- Inherits null handling and type coercion from UnaryMathExpression

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it operates on individual rows independently
- Does not require shuffle operations
- Can be applied within existing partitions without data movement

## Edge Cases

- Null input values return null (inherited from UnaryMathExpression)
- Handles infinite values according to IEEE 754 standards
- Very large degree values may result in loss of precision in floating-point arithmetic
- Negative degree values are converted correctly to negative radian values
- Zero degrees converts to zero radians

## Code Generation
This expression supports Tungsten code generation through its parent class UnaryMathExpression, which generates efficient bytecode for mathematical operations rather than falling back to interpreted mode.

## Examples
```sql
-- Convert 180 degrees to radians
SELECT RADIANS(180);
-- Result: 3.141592653589793

-- Convert multiple angle values
SELECT RADIANS(0), RADIANS(90), RADIANS(180), RADIANS(360);
-- Results: 0.0, 1.5707963267948966, 3.141592653589793, 6.283185307179586

-- Use with column data
SELECT angle_degrees, RADIANS(angle_degrees) as angle_radians 
FROM angles_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.radians

// Convert a column of degree values
df.select(radians(col("degrees_column")).alias("radians_column"))

// Chain with other mathematical operations
df.select(sin(radians(col("angle_degrees"))).alias("sine_value"))
```

## See Also

- ToDegrees - converts radians back to degrees
- Sin, Cos, Tan - trigonometric functions that typically work with radian inputs
- UnaryMathExpression - parent class for mathematical unary operations