# Cos

## Overview
The `Cos` expression computes the cosine of a numeric value in radians. It is a unary mathematical expression that wraps the standard `math.cos` function and returns a double-precision floating-point result.

## Syntax
```sql
COS(expr)
```

```scala
cos(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | A numeric expression representing an angle in radians |

## Return Type
`DoubleType` - Returns a double-precision floating-point number representing the cosine value.

## Supported Data Types

- All numeric data types (IntegerType, LongType, FloatType, DoubleType, DecimalType)
- Input values are implicitly converted to double before computation

## Algorithm

- Inherits from `UnaryMathExpression` which handles the core evaluation logic
- Applies `math.cos` function to the child expression's evaluated result
- Input value is treated as an angle measured in radians
- Leverages Scala's standard math library for the actual cosine computation
- Returns null if the input expression evaluates to null

## Partitioning Behavior
This expression preserves partitioning:

- Does not require data shuffling across partitions
- Can be computed independently on each partition
- Maintains existing data distribution patterns

## Edge Cases

- **Null handling**: Returns null if the input expression is null
- **Infinite values**: `COS(∞)` returns `NaN` (Not a Number)
- **NaN input**: `COS(NaN)` returns `NaN`
- **Very large values**: May lose precision due to floating-point limitations
- **Range**: Always returns values between -1.0 and 1.0 for finite inputs

## Code Generation
This expression supports Tungsten code generation through its parent class `UnaryMathExpression`, which generates efficient Java code that directly calls `Math.cos()` method instead of using interpreted evaluation.

## Examples
```sql
-- Basic usage
SELECT COS(0);
-- Result: 1.0

-- Using with PI
SELECT COS(3.14159265359);
-- Result: -1.0

-- Using with column data
SELECT angle_radians, COS(angle_radians) as cosine_value 
FROM measurements;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.cos

df.select(cos($"angle_column"))

// With column transformation
df.withColumn("cosine_result", cos($"radians_column"))
```

## See Also

- `Sin` - Computes sine of an angle in radians
- `Tan` - Computes tangent of an angle in radians
- `Acos` - Computes arc cosine (inverse cosine)
- `Radians` - Converts degrees to radians
- `Degrees` - Converts radians to degrees