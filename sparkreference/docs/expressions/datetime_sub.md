# DatetimeSub

## Overview
DatetimeSub is a runtime-replaceable expression that subtracts an interval from a timestamp or date value. It serves primarily as a SQL presentation layer for datetime subtraction operations, providing a clean string representation while delegating actual computation to its replacement expression.

## Syntax
```sql
datetime_column - INTERVAL value unit
timestamp_column - INTERVAL '1' DAY
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| start | Expression | The timestamp or date value from which to subtract |
| interval | Expression | The interval value to subtract from the start datetime |
| replacement | Expression | The underlying expression that performs the actual computation |

## Return Type
The return type depends on the replacement expression, but typically returns:

- `TimestampType` when subtracting from timestamp values
- `DateType` when subtracting from date values

## Supported Data Types

- **start**: `TimestampType`, `DateType`
- **interval**: `CalendarIntervalType`, interval literals
- Input types are validated by the replacement expression during analysis

## Algorithm

- Acts as a wrapper around the actual computation logic in the replacement expression
- During SQL generation, formats the operation as a simple subtraction using `makeSQLString`
- Runtime evaluation is delegated entirely to the replacement expression
- Inherits analysis rules from its replacement expression through `InheritAnalysisRules`
- The `parameters` method exposes only the meaningful operands (start and interval) for analysis

## Partitioning Behavior
Partitioning behavior depends on the underlying replacement expression:

- Generally preserves partitioning when operating on non-partitioning columns
- Does not typically require shuffle operations
- Partition pruning may be affected if operating on partition columns

## Edge Cases

- **Null handling**: Behavior depends on the replacement expression, typically follows SQL null semantics
- **Invalid intervals**: Runtime errors may occur for malformed interval expressions
- **Overflow scenarios**: Large interval subtractions may cause timestamp overflow
- **Type mismatches**: Analysis phase will validate compatible types between start and interval

## Code Generation
Code generation support depends entirely on the replacement expression:

- The DatetimeSub wrapper itself does not participate in code generation
- Actual codegen behavior is determined by the replacement expression's capabilities
- Most datetime arithmetic operations support Tungsten code generation

## Examples
```sql
-- Subtract 1 day from current timestamp
SELECT current_timestamp() - INTERVAL '1' DAY;

-- Subtract multiple units
SELECT date_col - INTERVAL '1 year 2 months 3 days' FROM table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("timestamp_col") - expr("INTERVAL '1' HOUR"))
df.withColumn("yesterday", col("date_col") - expr("INTERVAL '1' DAY"))
```

## See Also

- `DatetimeAdd` - Addition counterpart for datetime arithmetic
- `TimeAdd` - Time-specific addition operations
- `DateAdd` - Date-specific addition operations
- `RuntimeReplaceable` - Base trait for expressions with compile-time replacements