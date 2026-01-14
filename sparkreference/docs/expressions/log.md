# Log

## Overview
The Log expression computes the natural logarithm (base e) of a numeric value using `StrictMath.log`. It extends `UnaryLogExpression` and provides the mathematical logarithm function with alias support for "ln".

## Syntax
```sql
LOG(expr)
LN(expr)  -- alias
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(log(col("column_name")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric expression to compute the natural logarithm of |

## Return Type
Double - Returns a double precision floating point number representing the natural logarithm.

## Supported Data Types

- Numeric types (Int, Long, Float, Double, Decimal)

- Values are internally converted to double for computation

## Algorithm

- Evaluates the child expression to get the input value

- Converts the input to double precision

- Applies `StrictMath.log()` which computes the natural logarithm (base e)

- Returns the result as a double value

- Handles special mathematical cases according to `StrictMath.log` behavior

## Partitioning Behavior

- Preserves partitioning as it's a deterministic unary expression

- Does not require shuffle operations

- Can be pushed down to individual partitions independently

## Edge Cases

- Returns `NaN` for negative input values

- Returns `Double.NEGATIVE_INFINITY` for input value 0.0

- Returns `NaN` for `NaN` input

- Returns `Double.POSITIVE_INFINITY` for `Double.POSITIVE_INFINITY` input

- Null input values result in null output

## Code Generation
This expression supports Catalyst code generation (Tungsten) through its parent `UnaryLogExpression` class, generating efficient Java bytecode for evaluation.

## Examples
```sql
-- Basic natural logarithm
SELECT LOG(2.718281828);
-- Result: ~1.0

SELECT LN(1);
-- Result: 0.0

-- Edge cases
SELECT LOG(-1);
-- Result: NaN

SELECT LOG(0);
-- Result: -Infinity
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.range(1, 10).toDF("value")
df.select(log(col("value"))).show()

// Using alias
df.select(expr("ln(value)")).show()
```

## See Also

- Log10 - Base 10 logarithm
- Log2 - Base 2 logarithm  
- Exp - Exponential function (inverse of natural log)
- Pow - Power function