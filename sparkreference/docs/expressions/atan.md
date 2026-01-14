# Atan

## Overview
The `Atan` expression computes the arctangent (inverse tangent) of a numeric value in radians. It extends the `UnaryMathExpression` class and delegates to Scala's `math.atan` function for the actual computation.

## Syntax
```sql
ATAN(expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.atan
atan(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Numeric | The numeric expression for which to compute the arctangent |

## Return Type
Double - Returns the arctangent of the input value as a double-precision floating-point number.

## Supported Data Types

- Byte
- Short  
- Integer
- Long
- Float
- Double
- Decimal

## Algorithm

- Accepts a single numeric expression as input (child)
- Converts the input value to a double if necessary
- Delegates the arctangent calculation to Scala's `math.atan` function
- Returns the result as a double value in radians
- The result is in the range (-π/2, π/2)

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffling as it operates on individual rows
- Maintains existing partitioning scheme since it's a deterministic row-level transformation
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null if the input expression evaluates to null
- **Positive infinity**: Returns π/2 (approximately 1.5708) for positive infinity input
- **Negative infinity**: Returns -π/2 (approximately -1.5708) for negative infinity input  
- **NaN input**: Returns NaN (Not a Number)
- **Zero input**: Returns 0.0 exactly

## Code Generation
This expression supports Tungsten code generation through its parent class `UnaryMathExpression`, which generates optimized Java bytecode for efficient execution rather than falling back to interpreted mode.

## Examples
```sql
-- Basic arctangent calculation
SELECT ATAN(1.0);
-- Returns: 0.7853981633974483 (π/4)

-- Arctangent of zero
SELECT ATAN(0);
-- Returns: 0.0

-- Using with table data
SELECT name, value, ATAN(value) as atan_value 
FROM measurements 
WHERE value IS NOT NULL;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.atan

val df = spark.table("measurements")
val result = df.select(
  col("name"),
  col("value"), 
  atan(col("value")).alias("atan_value")
)

// With literal value
val literalResult = df.select(atan(lit(1.0)))
```

## See Also

- `Acos` - Arccosine function
- `Asin` - Arcsine function  
- `Atan2` - Two-argument arctangent function
- `Tan` - Tangent function (inverse of arctangent)