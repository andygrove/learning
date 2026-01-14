# Exp

## Overview
The `Exp` expression computes the exponential function (e^x) of a numeric value. It returns Euler's number (e) raised to the power of the input value, using Java's StrictMath.exp function for precise mathematical calculations.

## Syntax
```sql
EXP(expr)
```

```scala
exp(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric expression to compute the exponential of |

## Return Type
Double - Returns a double-precision floating-point value representing e^x.

## Supported Data Types

- Numeric types (Integer, Long, Float, Double, Decimal)
- Input values are automatically cast to Double for computation

## Algorithm

- Inherits from `UnaryMathExpression` which handles type coercion and null checking
- Uses `java.lang.StrictMath.exp()` for the actual exponential calculation
- StrictMath ensures reproducible results across different platforms and JVM implementations
- Input is automatically converted to double precision before calculation
- Returns IEEE 754 compliant double-precision result

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning - this is a row-level transformation
- Does not require shuffle operations
- Can be applied within partition boundaries independently

## Edge Cases

- **Null handling**: Returns null if input is null
- **Positive infinity**: EXP(709.8) and above returns positive infinity
- **Underflow**: Very negative values (below -745) return 0.0
- **NaN handling**: EXP(NaN) returns NaN
- **Special values**: EXP(0) returns exactly 1.0, EXP(1) returns approximately 2.718281828459045

## Code Generation
This expression supports Tungsten code generation. The `doGenCode` method generates optimized Java code that directly calls `java.lang.StrictMath.exp()`, avoiding object creation and method dispatch overhead during execution.

## Examples
```sql
-- Basic exponential calculation
SELECT EXP(0);
-- Result: 1.0

-- Exponential of 1 (Euler's number)
SELECT EXP(1);
-- Result: 2.718281828459045

-- Using with column data
SELECT name, value, EXP(value) as exp_value 
FROM measurements;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.exp

df.select(exp(col("temperature"))).show()

// With column alias
df.select(exp(col("log_value")).alias("original_value")).show()
```

## See Also

- `Log` - Natural logarithm (inverse of Exp)
- `Log10` - Base-10 logarithm  
- `Pow` - General exponentiation with custom base
- `Sqrt` - Square root function