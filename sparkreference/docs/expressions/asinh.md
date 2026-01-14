# Asinh

## Overview
The `Asinh` expression computes the inverse hyperbolic sine (arc hyperbolic sine) of a numeric value. It returns the hyperbolic angle whose hyperbolic sine is the input value, handling special cases like negative infinity appropriately.

## Syntax
```sql
ASINH(expr)
```

```scala
// DataFrame API
col("column_name").asinh()
// or using expr
expr("asinh(column_name)")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric expression for which to calculate the inverse hyperbolic sine |

## Return Type
Double - returns a double-precision floating-point number representing the inverse hyperbolic sine.

## Supported Data Types
Numeric data types that can be converted to Double:

- TINYINT
- SMALLINT  
- INTEGER
- BIGINT
- FLOAT
- DOUBLE
- DECIMAL

## Algorithm

- Uses the mathematical formula: `asinh(x) = log(x + sqrt(x² + 1))`
- Implements special case handling for negative infinity input
- Leverages `StrictMath.log()` for precise logarithmic calculations
- Combines standard math operations (`sqrt`, addition) for the core computation
- Maintains IEEE 754 compliance for floating-point edge cases

## Partitioning Behavior
This expression preserves partitioning:

- Does not require data shuffle as it's a unary transformation
- Can be applied per-partition independently
- Maintains the same number of rows and partitioning scheme

## Edge Cases

- **Null handling**: Returns null if input is null (inherited from UnaryMathExpression)
- **Negative infinity**: Explicitly handled to return `Double.NegativeInfinity`  
- **Positive infinity**: Returns `Double.PositiveInfinity` through natural mathematical evaluation
- **NaN input**: Returns `NaN` following IEEE 754 standards
- **Zero input**: Returns `0.0` as `asinh(0) = 0`
- **Very large values**: May approach positive/negative infinity asymptotically

## Code Generation
This expression supports Tungsten code generation (Whole Stage Code Generation):

- Implements `doGenCode()` method for compiled code path
- Generates optimized Java bytecode avoiding function call overhead
- Falls back to interpreted mode only when code generation is disabled
- Uses direct Java math operations in generated code for maximum performance

## Examples
```sql
-- Basic usage
SELECT ASINH(1.0);
-- Returns: 0.8813735870195430

-- Special case: zero
SELECT ASINH(0);
-- Returns: 0.0

-- Negative values
SELECT ASINH(-2.0);
-- Returns: -1.4436354751788103

-- With column data
SELECT name, ASINH(value) as asinh_value FROM measurements;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Apply to column
df.select(col("value"), asinh(col("value")).alias("asinh_value"))

// Using expr function
df.selectExpr("value", "asinh(value) as asinh_value")

// In transformations
df.withColumn("asinh_transformed", asinh(col("numeric_column")))
```

## See Also

- `SINH` - Hyperbolic sine (inverse operation)
- `ACOSH` - Inverse hyperbolic cosine  
- `ATANH` - Inverse hyperbolic tangent
- `LOG` - Natural logarithm (used internally)
- `SQRT` - Square root (used internally)