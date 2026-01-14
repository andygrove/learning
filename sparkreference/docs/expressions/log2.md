# Log2

## Overview
The Log2 expression computes the base-2 logarithm of a numeric input value. It extends the UnaryLogExpression class and uses the mathematical formula log₂(x) = log(x) / log(2) where log represents the natural logarithm. This expression has been available since Spark 1.4.0 and belongs to the math_funcs group.

## Syntax
```sql
LOG2(expr)
```

```scala
log2(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric expression for which to calculate the base-2 logarithm |

## Return Type
Double - Returns a double precision floating-point number representing the base-2 logarithm.

## Supported Data Types

- Numeric types (Int, Long, Float, Double)
- Any expression that can be cast to a numeric type

## Algorithm

- Validates that the input value is greater than the asymptotic boundary (typically 0)
- Computes the natural logarithm of the input using `StrictMath.log(x)`
- Divides by the natural logarithm of 2 using `StrictMath.log(2)`
- Returns null if the input is less than or equal to the asymptotic value
- Uses strict mathematical operations to ensure consistent results across platforms

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it's a deterministic unary operation
- Does not require shuffle operations
- Can be applied per-partition independently

## Edge Cases

- Returns null for null input values (null-safe operation)
- Returns null for values less than or equal to 0 (logarithm undefined for non-positive numbers)
- Handles positive infinity input by returning positive infinity
- Very small positive values near zero may result in large negative numbers

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method. It generates optimized Java code that performs null checking and boundary validation inline, avoiding function call overhead during execution.

## Examples
```sql
-- Basic usage
SELECT LOG2(8);
-- Result: 3.0

-- With column reference
SELECT LOG2(value) FROM table_name;

-- Example from source code
SELECT LOG2(2);
-- Result: 1.0
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.log2

df.select(log2(col("numeric_column")))

// With literal value
df.select(log2(lit(16)))  // Returns 4.0
```

## See Also

- Log (natural logarithm)
- Log10 (base-10 logarithm)
- Exp (exponential function)
- Pow (power function)