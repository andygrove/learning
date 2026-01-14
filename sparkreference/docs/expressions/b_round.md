# BRound

## Overview

BRound is a Spark Catalyst expression that implements banker's rounding (also known as round half to even) for numeric values. It rounds a numeric value to a specified number of decimal places using the HALF_EVEN rounding mode, which rounds to the nearest even number when the value is exactly halfway between two numbers.

## Syntax

```sql
ROUND(value, scale)
```

```scala
// DataFrame API usage
df.select(round(col("value"), lit(2)))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric value to be rounded |
| scale | Expression | The number of decimal places to round to (defaults to 0) |
| ansiEnabled | Boolean | Whether ANSI SQL compliance mode is enabled (internal parameter) |

## Return Type

Returns the same numeric type as the input expression (e.g., Double, Decimal, Float).

## Supported Data Types

- Double
- Float
- Decimal
- Integer types (Byte, Short, Int, Long)

## Algorithm

- Evaluates the child expression to get the numeric value to round
- Evaluates the scale expression to determine the number of decimal places
- Applies BigDecimal.RoundingMode.HALF_EVEN rounding mode
- When a number is exactly halfway between two values, rounds to the nearest even number
- Returns the rounded value in the same data type as the input

## Partitioning Behavior

- Preserves partitioning as it's a deterministic per-row transformation
- Does not require shuffle operations
- Can be pushed down to individual partitions safely

## Edge Cases

- Returns null if either the child expression or scale expression evaluates to null
- When ANSI mode is enabled, may throw exceptions for overflow conditions
- Negative scale values round to the left of the decimal point (e.g., scale -1 rounds to nearest 10)
- Very large scale values may result in precision limitations based on the underlying data type

## Code Generation

This expression extends RoundBase which typically supports Tungsten code generation for efficient evaluation in the generated Java code rather than falling back to interpreted mode.

## Examples

```sql
-- Round to 2 decimal places using banker's rounding
SELECT ROUND(2.125, 2) -- Returns 2.12 (rounds to even)
SELECT ROUND(2.135, 2) -- Returns 2.14 (rounds to even)

-- Round to nearest integer
SELECT ROUND(3.7) -- Returns 4

-- Round to nearest 10 using negative scale
SELECT ROUND(123, -1) -- Returns 120
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Round price to 2 decimal places
df.select(round(col("price"), 2))

// Round with default scale (0)
df.select(round(col("amount")))

// Round to nearest hundred
df.select(round(col("salary"), -2))
```

## See Also

- Round (standard rounding)
- Ceil (ceiling function)
- Floor (floor function) 
- RoundBase (parent class for rounding expressions)