# RoundCeil

## Overview
The `RoundCeil` expression performs ceiling-based rounding on a numeric value to a specified number of decimal places. It rounds the input value away from zero to the nearest value at the given scale using `BigDecimal.RoundingMode.CEILING`.

## Syntax
```sql
ROUND_CEILING(value, scale)
```

```scala
// DataFrame API usage would typically go through SQL functions
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric value to be rounded |
| scale | Expression | The number of decimal places to round to (must be integer type) |

## Return Type
Returns a decimal type that preserves the precision and scale characteristics of the input decimal value after applying ceiling rounding.

## Supported Data Types

- **Input value (child)**: DecimalType only
- **Scale parameter**: IntegerType only

## Algorithm

- Evaluates the child expression to get the decimal value to be rounded
- Evaluates the scale expression to determine the number of decimal places
- Applies `BigDecimal.RoundingMode.CEILING` to round the value away from zero
- Returns the rounded decimal result
- Inherits core rounding logic from the `RoundBase` parent class

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffle as it operates on individual row values
- Maintains existing partitioning scheme since it's a deterministic row-level transformation
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: If either the child value or scale parameter is null, the expression returns null
- **Scale bounds**: The scale parameter must be a valid integer; behavior with extreme scale values depends on underlying BigDecimal implementation
- **Precision limits**: Result precision is constrained by Spark's DecimalType precision limits
- **Ceiling rounding**: Always rounds away from zero (e.g., 2.1 becomes 3.0, -2.1 becomes -2.0)

## Code Generation
This expression extends `RoundBase` which likely supports Catalyst code generation for optimized execution, though the specific code generation behavior depends on the parent class implementation.

## Examples
```sql
-- Round 3.14159 to 2 decimal places using ceiling
SELECT ROUND_CEILING(3.14159, 2); -- Returns 3.15

-- Round to whole number
SELECT ROUND_CEILING(2.1, 0); -- Returns 3

-- Negative number ceiling rounding  
SELECT ROUND_CEILING(-2.7, 0); -- Returns -2
```

```scala
// DataFrame API usage would typically use SQL expression
import org.apache.spark.sql.catalyst.expressions.RoundCeil
import org.apache.spark.sql.catalyst.expressions.Literal

// Direct expression usage in Catalyst
val roundExpr = RoundCeil(
  child = Literal(3.14159),
  scale = Literal(2)
)
```

## See Also

- `RoundBase` - Parent class containing core rounding functionality
- Other rounding expressions that extend `RoundBase` with different rounding modes
- Standard SQL `ROUND()` and `CEIL()` functions for related rounding operations