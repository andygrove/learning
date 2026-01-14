# Cosh

## Overview
The `Cosh` expression computes the hyperbolic cosine of a numeric value. It is a unary mathematical expression that takes a single numeric input and returns the hyperbolic cosine using the standard mathematical formula cosh(x) = (e^x + e^(-x))/2.

## Syntax
```sql
COSH(expr)
```

```scala
cosh(column)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child/expr | Expression/Column | The numeric expression for which to compute the hyperbolic cosine |

## Return Type
Returns a `DoubleType` value representing the hyperbolic cosine of the input.

## Supported Data Types

- All numeric data types (ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType)
- DecimalType values are converted to double precision for computation

## Algorithm

- Inherits from `UnaryMathExpression` which handles type conversion and null propagation
- Delegates the actual computation to Scala's `math.cosh` function
- Input values are converted to Double type before computation
- The result is returned as a DoubleType value
- Null inputs produce null outputs following standard SQL null semantics

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle as it operates on individual rows
- Maintains existing data partitioning since it's a row-level transformation
- Can be executed in parallel across partitions without coordination

## Edge Cases

- Null input returns null (standard null propagation)
- Very large positive or negative values may result in overflow, returning `Double.PositiveInfinity`
- Zero input returns 1.0 (cosh(0) = 1)
- The function always returns positive values (cosh(x) ≥ 1 for all real x)
- NaN input returns NaN

## Code Generation
This expression supports Tungsten code generation through its parent class `UnaryMathExpression`, which generates optimized bytecode for mathematical operations rather than falling back to interpreted mode.

## Examples
```sql
-- Basic usage
SELECT COSH(0);
-- Returns: 1.0

SELECT COSH(1);
-- Returns: 1.5430806348152437

SELECT COSH(-1);
-- Returns: 1.5430806348152437

-- With table data
SELECT value, COSH(value) as cosh_value 
FROM VALUES (0), (1), (2), (-1) AS t(value);
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.cosh

df.select(cosh($"column_name"))
df.withColumn("cosh_result", cosh($"input_column"))

// Example with literal values
spark.range(5).select(cosh($"id")).show()
```

## See Also

- `Sinh` - Hyperbolic sine function
- `Tanh` - Hyperbolic tangent function  
- `Cos` - Trigonometric cosine function
- Other `UnaryMathExpression` implementations for mathematical functions