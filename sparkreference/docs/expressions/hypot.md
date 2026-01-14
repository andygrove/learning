# Hypot

## Overview
The `Hypot` expression calculates the Euclidean distance (hypotenuse) between two points in a 2D coordinate system. It computes the square root of the sum of squares of two numeric values using the formula √(x² + y²), implemented through Java's `math.hypot` function for numerical stability.

## Syntax
```sql
HYPOT(left_expr, right_expr)
```

```scala
hypot(col("left_column"), col("right_column"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The first numeric expression (x coordinate) |
| right | Expression | The second numeric expression (y coordinate) |

## Return Type
Returns a `DoubleType` representing the hypotenuse value as a floating-point number.

## Supported Data Types
Supports all numeric data types including:

- ByteType
- ShortType  
- IntegerType
- LongType
- FloatType
- DoubleType
- DecimalType

## Algorithm
The expression evaluation follows these steps:

- Both left and right expressions are evaluated to produce numeric values
- Values are automatically cast to double precision if needed
- The Java `Math.hypot(x, y)` method is called internally
- This method computes √(x² + y²) while avoiding intermediate overflow/underflow
- Returns the result as a DoubleType value

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffling between partitions
- Maintains existing partitioning scheme since it operates row-by-row
- Can be safely pushed down in query optimization

## Edge Cases

- Returns `null` if either input expression evaluates to `null`
- Handles infinite values according to IEEE 754 standards
- `HYPOT(INFINITY, any_finite_value)` returns `INFINITY`
- `HYPOT(NaN, any_value)` returns `NaN`
- Uses numerically stable algorithm to prevent intermediate overflow/underflow
- Very large inputs that would cause x² + y² to overflow are handled gracefully

## Code Generation
This expression extends `BinaryMathExpression` which supports Tungsten code generation for optimized execution in the Catalyst engine.

## Examples
```sql
-- Calculate hypotenuse of a right triangle with sides 3 and 4
SELECT HYPOT(3, 4);
-- Result: 5.0

-- Using with table columns
SELECT HYPOT(x_coord, y_coord) as distance 
FROM coordinates;

-- Handling edge cases
SELECT HYPOT(null, 5);
-- Result: null
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(hypot(col("x"), col("y")).alias("hypotenuse"))

// Calculate distance from origin
df.withColumn("distance_from_origin", hypot(col("x_pos"), col("y_pos")))
```

## See Also

- `SQRT` - Square root function
- `POW` - Power function  
- `SQRT` combined with arithmetic operations for manual hypotenuse calculation