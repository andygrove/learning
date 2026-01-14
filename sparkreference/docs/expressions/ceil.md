# Ceil

## Overview
The `Ceil` expression returns the smallest integer greater than or equal to the input value. It extends `UnaryMathExpression` and uses `math.ceil` for floating-point calculations while providing optimized handling for decimal and integer types.

## Syntax
```sql
CEIL(expr)
```

```scala
// DataFrame API
df.select(ceil($"column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric expression to apply the ceiling function to |

## Return Type
The return type depends on the input data type:

- **DecimalType with scale 0**: Returns the same DecimalType
- **DecimalType with scale > 0**: Returns DecimalType with precision adjusted to `precision - scale + 1` and scale 0
- **All other types**: Returns LongType

## Supported Data Types
The expression accepts the following input data types:

- DoubleType
- DecimalType (any precision and scale)
- LongType

## Algorithm
The evaluation algorithm varies by input data type:

- **LongType**: Returns the input value unchanged (already an integer)
- **DoubleType**: Applies `math.ceil()` and converts result to Long
- **DecimalType**: Uses the Decimal's built-in `ceil()` method
- **DecimalType with scale 0**: Returns input unchanged (already integer precision)

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffle
- Maintains existing partitioning scheme
- Can be applied per-partition independently

## Edge Cases

- **Null handling**: Returns null if input is null (inherited from UnaryMathExpression)
- **LongType input**: No transformation needed, returns input value directly  
- **DecimalType with scale 0**: Optimized to return input unchanged
- **Precision bounds**: DecimalType results are bounded using `DecimalType.bounded()`
- **Overflow**: Large double values converted to Long may cause overflow

## Code Generation
This expression supports Tungsten code generation with type-specific optimizations:

- **DecimalType with scale 0**: Generates `c` (identity)
- **DecimalType with scale > 0**: Generates `c.ceil()`
- **LongType**: Generates `c` (identity)
- **DoubleType**: Generates `(long)(java.lang.Math.CEIL(c))`

## Examples
```sql
-- Basic ceiling operations
SELECT CEIL(3.14) AS result;     -- Returns 4
SELECT CEIL(-2.8) AS result;     -- Returns -2
SELECT CEIL(5) AS result;        -- Returns 5

-- With decimal types
SELECT CEIL(CAST(3.567 AS DECIMAL(10,3))) AS result;  -- Returns 4
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.ceil

df.select(ceil($"price"))
df.withColumn("ceiling_value", ceil($"measurement"))

// With decimal columns  
df.select(ceil($"decimal_column".cast(DecimalType(10, 2))))
```

## See Also
- Floor - Returns largest integer less than or equal to input
- Round - Rounds to nearest integer
- Cbrt - Cube root function (also in mathExpressions.scala)