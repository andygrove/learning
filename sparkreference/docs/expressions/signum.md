# Signum

## Overview
The `Signum` expression computes the mathematical sign function (signum) of a numeric value or interval. It returns -1.0 for negative values, 0.0 for zero, and 1.0 for positive values, effectively normalizing any numeric input to indicate its sign.

## Syntax
```sql
SIGNUM(expr)
-- or
SIGN(expr)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Double, YearMonthInterval, DayTimeInterval | The numeric expression or interval to evaluate the sign of |

## Return Type
`Double` - Always returns a double-precision floating point value (-1.0, 0.0, or 1.0).

## Supported Data Types

- `DoubleType` - Standard double-precision floating point numbers
- `YearMonthIntervalType` - Year-month intervals (e.g., INTERVAL '2-3' YEAR TO MONTH)
- `DayTimeIntervalType` - Day-time intervals (e.g., INTERVAL '1 2:3:4' DAY TO SECOND)

## Algorithm

- Extracts the numeric double value from the input using `doubleValue()`
- Applies the Java `Math.signum()` function to determine the mathematical sign
- Returns -1.0 if the input is negative
- Returns 0.0 if the input is zero or negative zero
- Returns 1.0 if the input is positive

## Partitioning Behavior
This expression preserves partitioning:

- Does not require data shuffle across partitions
- Can be evaluated independently on each partition
- Maintains existing partition boundaries since it's a row-level transformation

## Edge Cases

- **Null handling**: Returns `null` if the input expression is `null` (null-safe evaluation)
- **NaN values**: Returns `NaN` when input is `Double.NaN` (follows Java Math.signum behavior)
- **Infinity**: Returns 1.0 for positive infinity, -1.0 for negative infinity
- **Zero handling**: Both +0.0 and -0.0 return 0.0
- **Interval conversion**: Intervals are converted to their double representation before sign calculation

## Code Generation
This expression extends `UnaryMathExpression` which supports Tungsten code generation for optimized execution. The generated code will inline the signum calculation rather than using interpreted evaluation.

## Examples
```sql
-- Basic numeric examples
SELECT SIGNUM(42.5);        -- Returns 1.0
SELECT SIGNUM(-17.3);       -- Returns -1.0
SELECT SIGNUM(0);           -- Returns 0.0

-- Interval examples
SELECT SIGNUM(INTERVAL '5' YEAR);     -- Returns 1.0
SELECT SIGNUM(INTERVAL -'100' YEAR);  -- Returns -1.0
SELECT SIGNUM(INTERVAL '0' DAY);      -- Returns 0.0
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(signum(col("amount")))
df.withColumn("sign", signum($"value"))

// Using the sign alias
df.select(sign(col("temperature")))
```

## See Also

- `Abs` - Absolute value function
- `Floor` - Floor mathematical function  
- `Ceil` - Ceiling mathematical function
- Other mathematical expressions in the `math_funcs` group