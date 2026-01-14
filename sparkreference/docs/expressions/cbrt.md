# Cbrt

## Overview
The `Cbrt` expression computes the cube root of a numeric value. It extends `UnaryMathExpression` and delegates to Scala's `math.cbrt` function to calculate the cube root of the input expression.

## Syntax
```sql
CBRT(expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.cbrt
cbrt(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric expression to compute the cube root of |

## Return Type
Returns a `DoubleType` value representing the cube root of the input.

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

- Inherits evaluation logic from `UnaryMathExpression`
- Converts input value to `Double` type
- Delegates computation to Scala's `math.cbrt()` function
- Returns the computed cube root as a `Double`
- Handles null propagation through the parent class

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not affect data partitioning
- No shuffle operations required
- Can be evaluated locally on each partition
- Maintains existing partition boundaries

## Edge Cases

- **Null handling**: Returns null if input is null
- **Negative numbers**: Correctly handles negative inputs (cube root of negative numbers is negative)
- **Zero**: Returns 0.0 for input value 0
- **Infinity**: Returns positive infinity for positive infinity input, negative infinity for negative infinity input
- **NaN**: Returns NaN for NaN input

## Code Generation
This expression supports Tungsten code generation through inheritance from `UnaryMathExpression`, which implements the `CodegenFallback` trait for optimized runtime performance.

## Examples
```sql
-- Basic usage
SELECT CBRT(27.0);
-- Result: 3.0

-- With negative numbers
SELECT CBRT(-8.0);
-- Result: -2.0

-- With column data
SELECT CBRT(volume) FROM measurements;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.cbrt

df.select(cbrt(col("volume")))

// With column alias
df.select(cbrt(col("volume")).alias("cube_root_volume"))
```

## See Also

- `Sqrt` - Square root expression
- `Pow` - Power/exponentiation expression  
- `UnaryMathExpression` - Base class for unary mathematical operations