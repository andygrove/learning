# Rint

## Overview
The `Rint` expression rounds a numeric value to the nearest integer using "round half to even" strategy (banker's rounding). It delegates to Java's `math.rint` function and is aliased as "ROUND" in SQL context.

## Syntax
```sql
RINT(expr)
ROUND(expr)  -- alias
```

```scala
// DataFrame API
col("column_name").rint()
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric expression to be rounded to nearest integer |

## Return Type
Returns a `Double` value representing the rounded result.

## Supported Data Types

- Numeric types (Int, Long, Float, Double, Decimal)
- Any expression that evaluates to a numeric value

## Algorithm

- Delegates evaluation to Java's `math.rint()` function
- Uses "round half to even" (banker's rounding) strategy  
- Values exactly halfway between two integers round to the nearest even integer
- Inherits behavior from `UnaryMathExpression` base class
- Performs standard null propagation and type coercion

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it's a deterministic unary transformation
- Does not require shuffle operations
- Can be applied per-partition independently

## Edge Cases

- Null input returns null (standard null propagation)
- NaN input returns NaN
- Positive/negative infinity returns the same infinity value
- Values like 2.5 round to 2, while 3.5 rounds to 4 (banker's rounding)
- Very large values may lose precision due to Double limitations

## Code Generation
Supports Tungsten code generation through inheritance from `UnaryMathExpression`, generating efficient bytecode that directly calls `math.rint`.

## Examples
```sql
-- Example SQL usage
SELECT RINT(2.3) as result;     -- Returns 2.0
SELECT RINT(2.5) as result;     -- Returns 2.0 (banker's rounding)
SELECT RINT(3.5) as result;     -- Returns 4.0 (banker's rounding)
SELECT ROUND(-2.7) as result;   -- Returns -3.0
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._
df.select(rint(col("price"))).show()
df.withColumn("rounded_value", rint($"decimal_column"))
```

## See Also

- `Round` - Standard rounding with configurable decimal places
- `Floor` - Always rounds down to nearest integer  
- `Ceil` - Always rounds up to nearest integer
- Other `UnaryMathExpression` implementations