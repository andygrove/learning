# Sec

## Overview
The `Sec` expression computes the secant of a numeric value. The secant function is defined as the reciprocal of the cosine function (1/cos(x)), where the input is expected to be in radians.

## Syntax
```sql
SEC(expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("sec(column_name)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | A numeric expression representing the angle in radians |

## Return Type
Returns a `DoubleType` value representing the secant of the input.

## Supported Data Types

- Numeric types (converted to Double internally)
- Any expression that can be cast to a numeric value

## Algorithm

- Takes the input numeric value as an angle in radians
- Computes the cosine of the input using `math.cos(x)`
- Returns the reciprocal (1/cosine) to get the secant value
- Uses standard Java Math library functions for the underlying calculation
- Supports Catalyst code generation for optimized execution

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle
- Operates on individual rows independently
- Maintains existing data partitioning scheme

## Edge Cases

- Returns `null` when input is `null`
- Returns `Double.POSITIVE_INFINITY` or `Double.NEGATIVE_INFINITY` when cosine of input equals zero (at π/2 + nπ)
- Input values that cause cosine to be very close to zero may result in very large values
- NaN input produces NaN output

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which generates optimized Java code using `java.lang.Math.cos()` for better performance in tight loops.

## Examples
```sql
-- Basic usage
SELECT SEC(0);
-- Result: 1.0

-- Using with column data
SELECT SEC(angle_column) FROM trigonometry_table;

-- Using with mathematical constants
SELECT SEC(PI()/3);
-- Result: 2.0 (secant of 60 degrees)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.range(1).select(lit(0).as("angle"))
df.select(expr("sec(angle)")).show()

// Using with existing columns
val trigDF = spark.table("angles_table")
trigDF.select(col("*"), expr("sec(radians)").as("secant_value"))
```

## See Also

- `cos()` - Cosine function (reciprocal of secant)
- `csc()` - Cosecant function (reciprocal of sine)
- `sin()`, `tan()` - Other trigonometric functions
- `acos()` - Inverse cosine function