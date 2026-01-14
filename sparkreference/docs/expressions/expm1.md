# Expm1

## Overview
The `Expm1` expression computes e^x - 1 for a given numeric input, where e is Euler's number (approximately 2.718281828). This function provides better numerical precision than computing `exp(x) - 1` directly, especially for values of x close to zero.

## Syntax
```sql
EXPM1(expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expm1(col("value")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Numeric | The exponent value for which to compute e^x - 1 |

## Return Type
Returns a `DoubleType` value representing the result of e^x - 1.

## Supported Data Types
Supports all numeric data types as input:

- ByteType
- ShortType  
- IntegerType
- LongType
- FloatType
- DoubleType
- DecimalType

Input values are cast to double precision for computation.

## Algorithm
The expression evaluation follows these steps:

- Input validation and null checking
- Cast the input value to double precision
- Delegate computation to `java.lang.StrictMath.expm1()` method
- Return the computed result as DoubleType
- Uses StrictMath for consistent cross-platform results

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle
- Can be computed independently on each partition
- Maintains existing data distribution
- Safe for columnar operations within partitions

## Edge Cases

- **Null handling**: Returns null if the input expression evaluates to null
- **Positive infinity**: `EXPM1(+∞)` returns positive infinity
- **Negative infinity**: `EXPM1(-∞)` returns -1.0
- **Very large positive values**: May result in positive infinity due to overflow
- **Zero input**: `EXPM1(0)` returns exactly 0.0
- **NaN input**: Returns NaN (Not a Number)

## Code Generation
This expression supports Tungsten code generation for optimized performance. The generated code directly calls `java.lang.StrictMath.expm1()` method, avoiding object creation overhead and enabling efficient vectorized execution.

## Examples
```sql
-- Basic usage
SELECT EXPM1(1.0);
-- Result: 1.7182818284590451

-- With zero (high precision case)
SELECT EXPM1(0);
-- Result: 0.0

-- With small values where precision matters
SELECT EXPM1(1e-10);
-- Result: 1.00000000005E-10

-- With column data
SELECT name, EXPM1(log_value) FROM measurements;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic computation
df.select(expm1(col("input_value")))

// Combined with other math functions
df.select(
  col("id"),
  expm1(col("rate")).alias("exponential_growth")
)

// Handling potential nulls
df.select(
  when(col("value").isNotNull, expm1(col("value")))
    .otherwise(lit(0.0))
    .alias("safe_expm1")
)
```

## See Also

- `exp()` - Exponential function e^x
- `log1p()` - Natural logarithm of (1 + x) with high precision
- `ln()` - Natural logarithm function
- `pow()` - Power function