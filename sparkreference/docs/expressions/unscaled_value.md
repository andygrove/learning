# UnscaledValue

## Overview
The UnscaledValue expression extracts the unscaled Long value from a Decimal data type. This is an internal expression created only by the Catalyst optimizer to efficiently access the underlying long representation of decimal values without performing scaling operations.

## Syntax
This is an internal expression not directly exposed in SQL or DataFrame API. It is generated automatically by the Catalyst optimizer during query planning and optimization phases.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression that must evaluate to a Decimal type |

## Return Type
LongType - returns the unscaled long value of the input decimal.

## Supported Data Types

- DecimalType (all precision and scale combinations)

## Algorithm

- Takes a Decimal input value and extracts its internal unscaled Long representation
- No type checking is performed since this is an optimizer-generated expression
- Directly calls the `toUnscaledLong()` method on the Decimal object
- Preserves null values through null-safe evaluation
- Uses efficient code generation for runtime execution

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require shuffle operations
- Maintains the same partitioning as the input expression
- Can be safely pushed down in query optimization

## Edge Cases

- **Null handling**: Returns null if the input decimal is null (null-intolerant behavior)
- **Overflow behavior**: Assumes the decimal's unscaled value fits within a Long range
- **No validation**: Does not perform type checking since it's optimizer-generated
- **Internal use only**: Not accessible through user-facing APIs

## Code Generation
This expression fully supports Tungsten code generation through the `doGenCode` method, which generates efficient Java code that directly calls `toUnscaledLong()` on the decimal value.

## Examples
```sql
-- Not directly available in SQL
-- Generated internally by optimizer for decimal operations
```

```scala
// Not directly available in DataFrame API
// Automatically created during query optimization
// Example of when it might be generated internally:
import org.apache.spark.sql.types._
val df = spark.range(1).select(lit(BigDecimal("123.45")).cast(DecimalType(5,2)))
// UnscaledValue expression may be generated internally during optimization
```

## See Also

- MakeDecimal - constructs Decimal values from unscaled long and precision/scale
- CheckOverflow - validates decimal precision and scale bounds
- Decimal type documentation - for understanding decimal representation