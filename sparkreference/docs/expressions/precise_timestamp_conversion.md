# PreciseTimestampConversion

## Overview
PreciseTimestampConversion is an internal Spark Catalyst expression used for converting TimestampType to Long and back without losing precision during time windowing operations. It preserves microsecond-level precision by maintaining the internal representation format used by Spark's timestamp handling.

## Syntax
This is an internal expression not directly exposed in SQL or DataFrame API. It is automatically generated during time windowing operations.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression to be converted |
| fromType | DataType | The source data type for conversion |
| toType | DataType | The target data type for conversion |

## Return Type
Returns the data type specified by the `toType` parameter, typically either TimestampType or LongType depending on conversion direction.

## Supported Data Types
Supports conversion between TimestampType and LongType while preserving microsecond precision for time windowing operations.

## Algorithm

- Evaluates the child expression to get the input value
- Performs a direct value pass-through without modification (`nullSafeEval` returns input unchanged)
- Relies on Spark's internal type system to handle the actual conversion semantics
- Uses code generation to optimize the conversion process
- Maintains null safety by propagating null values from child expressions

## Partitioning Behavior
This expression preserves partitioning since it performs deterministic, row-local transformations:

- Preserves existing partitioning schemes
- Does not require data shuffle
- Maintains data locality during conversion

## Edge Cases

- **Null handling**: Expression is null-intolerant (`nullIntolerant = true`), meaning null inputs produce null outputs
- **Type safety**: Input types are validated against the specified `fromType` through `ExpectsInputTypes` trait
- **Precision preservation**: Maintains full microsecond precision during timestamp conversions
- **Code generation fallback**: Always uses code generation path with direct value assignment

## Code Generation
This expression fully supports Tungsten code generation. It generates optimized Java code that directly assigns the input value to the output without function call overhead, making it highly efficient for time windowing operations.

## Examples
```sql
-- This expression is not directly accessible in SQL
-- It is automatically used internally during time window operations
SELECT window(timestamp_col, '1 hour') FROM events;
```

```scala
// Not directly accessible in DataFrame API
// Used internally during time windowing operations
df.groupBy(window($"timestamp", "1 hour")).count()
```

## See Also

- TimeWindow expressions for windowing operations
- UnaryExpression base class for single-input expressions
- ExpectsInputTypes trait for type validation
- TimestampType and LongType data types