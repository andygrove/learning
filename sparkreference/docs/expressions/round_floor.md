# RoundFloor

## Overview
The `RoundFloor` expression performs rounding of a decimal number to a specified scale using the FLOOR rounding mode. It always rounds down towards negative infinity, truncating any digits beyond the specified decimal places.

## Syntax
```sql
ROUND_FLOOR(value, scale)
```

```scala
// DataFrame API usage would typically be through built-in functions
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | DecimalType | The decimal value to be rounded |
| scale | IntegerType | The number of decimal places to round to |

## Return Type
Returns a decimal value with the same precision characteristics as the input, rounded according to the FLOOR rounding mode.

## Supported Data Types

- **Input**: DecimalType for the value, IntegerType for the scale parameter
- **Output**: DecimalType

## Algorithm

- Takes the input decimal value and scale parameter
- Applies BigDecimal.RoundingMode.FLOOR rounding mode
- Rounds the value to the specified number of decimal places
- Always rounds towards negative infinity (down)
- Inherits core rounding logic from the RoundBase parent class

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it's a deterministic row-level transformation
- Does not require shuffle operations
- Can be safely pushed down in query optimization

## Edge Cases

- **Null handling**: If either child or scale is null, the result is null
- **Negative scale**: Rounds to positions left of the decimal point when scale is negative
- **Zero scale**: Rounds to the nearest integer using FLOOR mode
- **Precision limits**: Respects decimal precision and scale constraints of the Spark DecimalType system

## Code Generation
This expression extends RoundBase which typically supports Tungsten code generation for optimal performance in the Catalyst query engine, avoiding interpreted evaluation overhead.

## Examples
```sql
-- Round 3.7 down to nearest integer
SELECT ROUND_FLOOR(3.7, 0); -- Returns 3

-- Round 3.14159 down to 2 decimal places  
SELECT ROUND_FLOOR(3.14159, 2); -- Returns 3.14

-- Round negative number down
SELECT ROUND_FLOOR(-2.3, 0); -- Returns -3
```

```scala
// Example would use Catalyst expression directly
val roundFloor = RoundFloor(
  child = Literal(Decimal(3.14159)), 
  scale = Literal(2)
)
```

## See Also

- RoundBase - Parent class providing core rounding functionality
- RoundCeil - Ceiling rounding mode equivalent
- Round - Standard rounding expression