# Csc

## Overview
The `Csc` expression calculates the cosecant of a numeric value. It returns the reciprocal of the sine function, mathematically equivalent to 1/sin(x), where x is the input value in radians.

## Syntax
```sql
CSC(expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("CSC(column_name)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric expression to calculate the cosecant of (value in radians) |

## Return Type
`DoubleType` - Returns a double-precision floating-point number.

## Supported Data Types

- Numeric types (INT, LONG, FLOAT, DOUBLE, DECIMAL)
- Any expression that can be implicitly cast to DOUBLE

## Algorithm

- Takes the input expression and evaluates it as a double value
- Calculates the sine of the input value using `math.sin(x)`
- Returns the reciprocal (1 / sin(x)) as the cosecant result
- Leverages Java's `Math.sin()` function for the underlying sine calculation
- Uses Spark's `UnaryMathExpression` framework for consistent null handling and type coercion

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it operates on individual rows without requiring data movement
- Does not require shuffle operations
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null if the input expression evaluates to null
- **Zero and multiples of π**: Returns positive or negative infinity when sin(x) equals zero (x = 0, π, 2π, etc.)
- **NaN input**: Returns NaN (Not a Number) if input is NaN
- **Infinite input**: Returns NaN if input is positive or negative infinity
- **Domain considerations**: While mathematically defined for all real numbers except multiples of π, floating-point precision may cause unexpected results near these values

## Code Generation
This expression supports Tungsten code generation for optimized performance. The `doGenCode` method generates Java code that directly calls `java.lang.Math.sin()` and computes the reciprocal, avoiding the overhead of interpreted execution.

## Examples
```sql
-- Calculate cosecant of 1 radian
SELECT CSC(1);
-- Result: 1.1883951057781212

-- Calculate cosecant of π/2 (which equals 1)
SELECT CSC(PI()/2);
-- Result: 1.0

-- Handle null input
SELECT CSC(NULL);
-- Result: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Calculate cosecant of a column
df.select(expr("CSC(angle_column)"))

// Using with literal values
df.select(expr("CSC(1.0)").alias("csc_result"))

// Chaining with other math functions
df.select(expr("CSC(RADIANS(degrees_column))").alias("csc_from_degrees"))
```

## See Also

- `Sin` - Sine function (reciprocal of cosecant)
- `Cos` - Cosine function  
- `Sec` - Secant function (reciprocal of cosine)
- `Tan` - Tangent function
- `Cot` - Cotangent function