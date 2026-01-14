# UpCast

## Overview
UpCast is a Catalyst expression that performs safe upcast operations between compatible data types without risk of data loss or truncation. It represents type conversions that widen the data type, such as int to long or date to timestamp, ensuring data integrity during the transformation.

## Syntax
UpCast is primarily used internally by the Catalyst optimizer and is not directly exposed in SQL syntax. It is automatically inserted during query planning when safe type promotions are needed.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The source expression to be upcast |
| target | AbstractDataType | The target data type for the upcast operation |
| walkedTypePath | Seq[String] | Optional path tracking for nested type resolution (default: Nil) |

## Return Type
Returns the target data type specified in the `target` parameter. For DecimalType objects, returns `DecimalType.SYSTEM_DEFAULT` with system-defined precision and scale.

## Supported Data Types
UpCast supports safe conversions between compatible data types including:

- Numeric widening (byte → short → int → long → float → double)
- Decimal precision/scale expansion
- Date to timestamp conversions
- String length expansions
- Compatible complex type expansions

## Algorithm
UpCast operates through the following internal mechanism:

- Validates that the source and target types are compatible for safe upcast
- Preserves the original expression as a child node in the expression tree
- Defers actual evaluation to the Cast expression during code generation
- Tracks type resolution path for complex nested types
- Maintains foldability properties based on child expression and timezone requirements

## Partitioning Behavior
UpCast has the following partitioning characteristics:

- Preserves data partitioning as it does not change data distribution
- Does not require shuffle operations
- Maintains partition keys when applied to partitioning columns

## Edge Cases

- Null values: Preserves null values without modification
- Timezone dependency: Foldability is affected when timezone conversion is required
- Decimal handling: Uses system default precision/scale for generic DecimalType targets
- Unevaluable: Cannot be directly evaluated and must be resolved to Cast expressions

## Code Generation
UpCast is marked as `Unevaluable` and does not support direct code generation. It serves as a placeholder expression that gets resolved to actual Cast expressions during query optimization phases, which then participate in code generation.

## Examples
```sql
-- UpCast is not directly accessible in SQL
-- It's automatically inserted during optimization
SELECT column_int + column_bigint FROM table
-- Internally creates UpCast(column_int, LongType)
```

```scala
// UpCast is primarily used internally by Catalyst
// Example of internal usage during expression resolution
val upcastExpr = UpCast(
  child = col("int_column").expr,
  target = LongType,
  walkedTypePath = Seq.empty
)
```

## See Also

- Cast - The evaluable expression that UpCast resolves to
- ImplicitCastInputTypes - Trait for expressions requiring implicit casting
- TypeCoercion - Rule set that inserts UpCast expressions during analysis