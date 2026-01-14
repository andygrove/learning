# Log1p

## Overview
Log1p computes the natural logarithm of (1 + x) for a given numeric expression. This function is mathematically equivalent to `ln(1 + x)` but provides better numerical precision for values of x close to zero. It is implemented as a unary logarithmic expression that uses `StrictMath.log1p` for computation.

## Syntax
```sql
LOG1P(expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.log1p
log1p(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Numeric | The numeric expression to compute log1p for |

## Return Type
Returns a `DoubleType` value representing the natural logarithm of (1 + input).

## Supported Data Types

- All numeric types (IntegerType, LongType, FloatType, DoubleType, DecimalType)
- Numeric values are automatically cast to Double for computation

## Algorithm

- Inherits from `UnaryLogExpression` which handles the core logarithmic expression logic
- Uses `StrictMath.log1p` as the underlying mathematical function for precise computation
- Defines a vertical asymptote at y = -1.0, meaning the function approaches negative infinity as x approaches -1
- Implements null-safe evaluation through the parent expression framework
- Returns null for invalid inputs (such as values ≤ -1)

## Partitioning Behavior
This expression preserves partitioning:

- Does not require data shuffling across partitions
- Can be computed independently on each partition
- Maintains the same partitioning scheme as the input data

## Edge Cases

- Returns null when input is null
- Returns `Double.NaN` for inputs where x ≤ -1 (since log of non-positive numbers is undefined)
- Returns `Double.NEGATIVE_INFINITY` when x approaches -1 from the right
- Returns 0.0 when input is 0 (since ln(1 + 0) = ln(1) = 0)
- Handles very small positive and negative values with high precision due to `StrictMath.log1p` implementation

## Code Generation
This expression supports Spark's Tungsten code generation framework, inheriting code generation capabilities from the `UnaryLogExpression` base class for optimized runtime performance.

## Examples
```sql
-- Basic usage
SELECT LOG1P(0);
-- Returns: 0.0

SELECT LOG1P(1);  
-- Returns: 0.6931471805599453 (ln(2))

SELECT LOG1P(-0.5);
-- Returns: -0.6931471805599453 (ln(0.5))

SELECT LOG1P(null);
-- Returns: null
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.log1p

df.select(log1p(col("value")))

// With column alias
df.select(log1p(col("input_col")).alias("log1p_result"))
```

## See Also

- `Log` - Natural logarithm function
- `Log10` - Base-10 logarithm function  
- `Log2` - Base-2 logarithm function
- `Exp` - Exponential function (inverse of natural log)
- `Expm1` - Computes exp(x) - 1 (inverse operation of log1p)