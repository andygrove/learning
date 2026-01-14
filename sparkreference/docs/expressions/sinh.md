# Sinh

## Overview
The `Sinh` expression computes the hyperbolic sine of a numeric value. It is a unary mathematical expression that applies the `math.sinh` function to its input argument.

## Syntax
```sql
SINH(expr)
```

```scala
sinh(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Numeric | The numeric expression for which to calculate the hyperbolic sine |

## Return Type
Double - Returns a double-precision floating-point value representing the hyperbolic sine of the input.

## Supported Data Types

- Byte
- Short  
- Integer
- Long
- Float
- Double
- Decimal

All numeric input types are converted to double for the calculation.

## Algorithm

- Accepts a single numeric expression as input
- Converts the input value to a double-precision floating-point number
- Applies the Java `math.sinh` function to compute the hyperbolic sine
- Returns the result as a double value
- Inherits standard unary expression evaluation patterns from `UnaryMathExpression`

## Partitioning Behavior
This expression preserves partitioning as it is a deterministic unary operation:

- Does not require data shuffling
- Maintains existing partitioning scheme
- Can be applied per-partition independently

## Edge Cases

- **Null handling**: Returns null if the input expression evaluates to null
- **Positive infinity**: Returns positive infinity for very large positive inputs
- **Negative infinity**: Returns negative infinity for very large negative inputs  
- **NaN inputs**: Returns NaN (Not a Number) for NaN inputs
- **Zero input**: Returns 0.0 for input value 0

## Code Generation
This expression supports Tungsten code generation as it extends `UnaryMathExpression`, which provides optimized code generation for mathematical operations rather than falling back to interpreted mode.

## Examples
```sql
-- Basic usage
SELECT SINH(0);
-- Result: 0.0

SELECT SINH(1);  
-- Result: 1.1752011936438014

SELECT SINH(-1);
-- Result: -1.1752011936438014

SELECT SINH(NULL);
-- Result: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.sinh

df.select(sinh(col("value"))).show()

// With column alias
df.select(sinh(col("input_column")).alias("sinh_result"))
```

## See Also

- `Cosh` - Hyperbolic cosine function
- `Tanh` - Hyperbolic tangent function  
- `Sin` - Trigonometric sine function
- `UnaryMathExpression` - Base class for unary mathematical expressions