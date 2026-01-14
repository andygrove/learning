# Acos

## Overview
The `Acos` expression computes the arc cosine (inverse cosine) of a numeric value. This function returns the angle in radians whose cosine is the input value, with the result range being [0, π].

## Syntax
```sql
ACOS(expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.acos
df.select(acos(col("column_name")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric expression to compute the arc cosine of |

## Return Type
Double - returns a double precision floating-point number representing the angle in radians.

## Supported Data Types

- Byte
- Short  
- Integer
- Long
- Float
- Double
- Decimal

All input types are converted to Double before computation.

## Algorithm

- Converts the input expression to a Double value
- Delegates to `java.lang.Math.acos()` for the actual computation
- Returns NaN for inputs outside the valid domain [-1, 1]
- Returns null if the input is null
- Follows IEEE 754 floating-point arithmetic standards

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it's a deterministic unary expression
- Does not require shuffle operations
- Can be pushed down to individual partitions independently

## Edge Cases

- **Null handling**: Returns null when input is null
- **Domain validation**: Returns NaN for inputs outside [-1, 1] range
- **Boundary values**: acos(-1) = π, acos(0) = π/2, acos(1) = 0
- **Invalid inputs**: acos(2) returns NaN as shown in the usage example
- **Infinity handling**: Returns NaN for positive or negative infinity inputs

## Code Generation
This expression extends `UnaryMathExpression` which supports Tungsten code generation for optimal performance in the Catalyst optimizer.

## Examples
```sql
-- Basic usage
SELECT ACOS(0.5);
-- Result: 1.0471975511965979

-- Edge case with invalid input
SELECT ACOS(2);
-- Result: NaN

-- With column data
SELECT ACOS(cosine_value) FROM trigonometry_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.acos

// Basic usage
df.select(acos(lit(0.5)))

// With column
df.select(acos(col("cosine_values")))

// Chained with other expressions
df.select(acos(col("x")).alias("angle_radians"))
```

## See Also

- `Asin` - Arc sine function
- `Atan` - Arc tangent function
- `Cos` - Cosine function (inverse of Acos)
- `Sin` - Sine function
- `Tan` - Tangent function