# Log10

## Overview
The Log10 expression computes the base-10 logarithm of a numeric value. It extends UnaryLogExpression and uses Java's StrictMath.log10 function to perform the calculation.

## Syntax
```sql
LOG10(expr)
```

```scala
import org.apache.spark.sql.functions.log10
log10(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric expression to compute the base-10 logarithm of |

## Return Type
Double - returns a double precision floating point number representing the base-10 logarithm.

## Supported Data Types

- Numeric types (Int, Long, Float, Double, Decimal)
- Any expression that can be cast to a numeric type

## Algorithm

- Evaluates the child expression to get the input value
- Converts the input to a double if necessary
- Applies Java's StrictMath.log10 function to compute the base-10 logarithm
- Returns the result as a double value
- Handles null propagation through the UnaryLogExpression parent class

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not affect data distribution or partitioning scheme
- Does not require shuffle operations
- Can be applied per-partition independently

## Edge Cases

- Returns null if the input expression evaluates to null
- Returns NaN (Not a Number) for negative input values
- Returns negative infinity for input value 0
- Returns 0.0 for input value 1.0
- Returns positive infinity for input value positive infinity

## Code Generation
This expression supports Catalyst code generation (Tungsten) through its parent UnaryLogExpression class, enabling efficient compiled code execution rather than interpreted evaluation.

## Examples
```sql
-- Basic usage
SELECT LOG10(100);
-- Returns: 2.0

-- Using with column data
SELECT LOG10(amount) FROM sales;

-- Example from source documentation
SELECT LOG10(10);
-- Returns: 1.0
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.log10

df.select(log10(col("value")))

// With column transformation
df.withColumn("log10_value", log10(col("original_value")))
```

## See Also

- Log (natural logarithm)
- Log2 (base-2 logarithm)
- Exp (exponential function)
- Pow (power function)