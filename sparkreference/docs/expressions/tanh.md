# Tanh

## Overview
The `Tanh` expression computes the hyperbolic tangent of a numeric value. This is a unary mathematical expression that applies the `math.tanh` function to its input, returning a double-precision floating-point result.

## Syntax
```sql
TANH(expr)
```

```scala
// DataFrame API
col("column_name").tanh
// or
tanh(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Numeric | The input expression for which to calculate the hyperbolic tangent |

## Return Type
Double - Returns a double-precision floating-point number representing the hyperbolic tangent of the input.

## Supported Data Types

- Byte
- Short  
- Integer
- Long
- Float
- Double
- Decimal

All numeric input types are implicitly cast to Double for computation.

## Algorithm

- Inherits from `UnaryMathExpression` which provides the evaluation framework
- Delegates the actual computation to Scala's `math.tanh` function
- Input values are cast to Double before applying the hyperbolic tangent function
- The result is returned as a Double value
- Follows standard IEEE 754 floating-point arithmetic rules

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it's a unary transformation that doesn't require data movement
- Does not require shuffle operations
- Can be computed independently for each row

## Edge Cases

- Null handling: Returns null if the input expression evaluates to null
- Empty input: Not applicable for scalar expressions
- Overflow behavior: Returns values asymptotically approaching ±1.0 for very large positive/negative inputs
- Special values: `tanh(0)` returns `0.0`, `tanh(∞)` returns `1.0`, `tanh(-∞)` returns `-1.0`
- NaN inputs: Returns NaN following IEEE 754 standards

## Code Generation
This expression supports Tungsten code generation through the `UnaryMathExpression` base class, which generates efficient Java code that directly calls the underlying math function without boxing/unboxing overhead.

## Examples
```sql
-- Basic usage
SELECT TANH(0);
-- Result: 0.0

SELECT TANH(1);
-- Result: 0.7615941559557649

SELECT TANH(-1);
-- Result: -0.7615941559557649

-- With column data
SELECT name, TANH(value) as tanh_value FROM measurements;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(tanh(col("input_column")))

// With column expression
df.withColumn("tanh_result", col("numeric_col").tanh)

// Chaining with other math functions
df.select(tanh(sinh(col("x"))))
```

## See Also

- `Sinh` - Hyperbolic sine function
- `Cosh` - Hyperbolic cosine function  
- `Tan` - Trigonometric tangent function
- Other `UnaryMathExpression` implementations for mathematical operations