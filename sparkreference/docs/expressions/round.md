# Round

## Overview
The Round expression rounds a numeric value to a specified number of decimal places using the HALF_UP rounding mode. It extends RoundBase and provides rounding functionality with configurable scale and ANSI SQL compliance support.

## Syntax
```sql
ROUND(expr [, scale])
```

```scala
round(col("column_name"), scale)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric expression to be rounded |
| scale | Expression | The number of decimal places to round to (defaults to 0) |
| ansiEnabled | Boolean | Whether ANSI SQL compliance is enabled (defaults to SQLConf setting) |

## Return Type
Returns the same numeric data type as the input expression (preserves input type).

## Supported Data Types

- Decimal types
- Float and Double
- Byte, Short, Integer, Long
- Any numeric type that can be converted to BigDecimal

## Algorithm

- Converts the input value to BigDecimal for precision handling
- Applies HALF_UP rounding mode (rounds 0.5 up to the next integer)
- Scales the result to the specified number of decimal places
- Returns the rounded value in the original data type
- Handles ANSI mode for strict error handling on overflow/underflow

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it's a deterministic row-level transformation
- Does not require shuffle operations
- Can be applied within partition boundaries

## Edge Cases

- Null input returns null (null-safe operation)
- Negative scale values round to the left of decimal point (e.g., scale=-1 rounds to tens)
- Zero scale rounds to nearest integer
- ANSI mode affects overflow/underflow error handling behavior
- Very large scale values may cause precision issues

## Code Generation
This expression supports Catalyst code generation (Tungsten) through its RoundBase parent class, enabling optimized bytecode generation for improved performance in tight loops.

## Examples
```sql
-- Round to nearest integer
SELECT ROUND(3.7) -- Returns 4

-- Round to 2 decimal places  
SELECT ROUND(3.14159, 2) -- Returns 3.14

-- Round to tens place
SELECT ROUND(123.45, -1) -- Returns 120
```

```scala
// Round to nearest integer
df.select(round(col("price")))

// Round to 2 decimal places
df.select(round(col("price"), lit(2)))

// Using in withColumn
df.withColumn("rounded_price", round(col("price"), lit(2)))
```

## See Also

- RoundBase - Parent class providing core rounding functionality
- Ceil - Rounds up to nearest integer
- Floor - Rounds down to nearest integer
- Truncate - Truncates without rounding