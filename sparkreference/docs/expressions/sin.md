# Sin

## Overview
The `Sin` expression computes the trigonometric sine of a numeric value in radians. It extends the `UnaryMathExpression` class and delegates the actual computation to Java's `math.sin` function.

## Syntax
```sql
SIN(expr)
```

```scala
sin(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Numeric | The input value in radians for which to compute the sine |

## Return Type
Double - Returns a double-precision floating-point value representing the sine of the input.

## Supported Data Types

- Byte
- Short  
- Integer
- Long
- Float
- Double
- Decimal

All numeric input types are implicitly converted to Double for the sine calculation.

## Algorithm

- Takes a single numeric expression as input (child expression)

- Evaluates the child expression to get the numeric value

- Converts the input value to Double if not already

- Delegates to Java's `math.sin()` function to compute the trigonometric sine

- Returns the result as a Double value

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows without requiring data movement:

- Preserves existing partitioning schemes

- Does not require shuffle operations

- Can be executed independently on each partition

## Edge Cases

- **Null handling**: Returns null if the input expression evaluates to null

- **NaN input**: Returns NaN (Not a Number) when input is NaN

- **Infinite input**: Returns NaN for positive or negative infinity inputs

- **Very large values**: May lose precision due to floating-point limitations

- **Domain**: Accepts any finite numeric value (sine function has no domain restrictions)

## Code Generation
This expression supports Whole-Stage Code Generation (Tungsten) through its parent `UnaryMathExpression` class, allowing it to generate efficient Java code rather than falling back to interpreted evaluation.

## Examples
```sql
-- Basic sine calculation
SELECT SIN(0);
-- Result: 0.0

-- Sine of π/2 (90 degrees)  
SELECT SIN(1.5707963267948966);
-- Result: 1.0

-- Sine with column reference
SELECT SIN(angle_radians) FROM measurements;

-- Sine of null
SELECT SIN(null);
-- Result: null
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.sin

df.select(sin(col("radians_column")))

// With literal value
df.select(sin(lit(Math.PI / 2)))

// Combined with other functions
df.select(sin(radians(col("degrees_column"))))
```

## See Also

- `Cos` - Computes cosine of a value
- `Tan` - Computes tangent of a value  
- `Asin` - Computes arcsine (inverse sine)
- `Radians` - Converts degrees to radians
- `Degrees` - Converts radians to degrees