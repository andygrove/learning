# Asin

## Overview
The `Asin` expression computes the arc sine (inverse sine) of a numeric value. It returns the angle in radians whose sine is the input value, with the result range being [-π/2, π/2].

## Syntax
```sql
ASIN(expr)
```

```scala
// DataFrame API
col("column_name").asin
// or
asin(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric expression to compute the arc sine of |

## Return Type
Returns `DoubleType` - a double precision floating-point number representing the angle in radians.

## Supported Data Types
Supports all numeric data types as input:

- ByteType
- ShortType  
- IntegerType
- LongType
- FloatType
- DoubleType
- DecimalType

## Algorithm
The expression evaluation follows these steps:

- Inherits from `UnaryMathExpression` which handles null propagation and type conversion
- Converts input value to double precision
- Delegates computation to `java.lang.Math.asin()` function
- Returns NaN for input values outside the valid domain [-1, 1]
- Preserves null values (null input produces null output)

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffle as it operates on individual rows
- Maintains existing partitioning scheme
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null when input is null
- **Domain validation**: Returns NaN for input values < -1 or > 1  
- **Boundary values**: ASIN(-1) = -π/2, ASIN(1) = π/2, ASIN(0) = 0
- **Special values**: Returns NaN for NaN input, handles positive/negative infinity as NaN
- **Precision**: Subject to floating-point precision limitations of underlying Math.asin implementation

## Code Generation
This expression supports Tungsten code generation through the `UnaryMathExpression` base class, which generates efficient Java code that directly calls `Math.asin()` without object creation overhead.

## Examples
```sql
-- Basic usage
SELECT ASIN(0.5);
-- Result: 0.5235987755982989 (π/6 radians)

-- Edge case - invalid domain
SELECT ASIN(2);
-- Result: NaN

-- With column data
SELECT name, ASIN(sine_value) as angle_radians 
FROM trigonometry_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(asin(col("sine_column")))

// Using column method
df.select(col("sine_column").asin)

// Converting result to degrees
df.select((asin(col("sine_column")) * 180 / math.Pi).alias("angle_degrees"))
```

## See Also

- `Sin` - Computes sine of an angle
- `Acos` - Computes arc cosine  
- `Atan` - Computes arc tangent
- `Sinh` - Computes hyperbolic sine
- Other trigonometric functions in the `math_funcs` group