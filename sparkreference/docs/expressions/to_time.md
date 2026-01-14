# ToTime

## Overview
The `ToTime` expression converts a string representation of time into a `TimeType` value. It supports both default parsing and custom format-based parsing using optional format strings, and serves as a runtime replaceable expression that delegates actual parsing to a specialized `ToTimeParser` class.

## Syntax
```sql
to_time(str)
to_time(str, format)
```

```scala
// DataFrame API usage
ToTime(stringExpr)
ToTime(stringExpr, formatExpr)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `str` | String | The input string containing the time value to be parsed |
| `format` | String (Optional) | Optional format pattern specifying how to parse the input string |

## Return Type
`TimeType` - A Spark SQL time data type representing time values.

## Supported Data Types

- **Input**: `StringTypeWithCollation` (supports trim collation for both string argument and optional format argument)
- **Output**: `TimeType`

## Algorithm

- Creates an `Invoke` expression that calls a `ToTimeParser` instance to perform the actual parsing
- If no format is provided, uses default parsing behavior through the parser
- If format is foldable (constant), evaluates it at optimization time and creates a specialized parser with the format
- If format is non-foldable, falls back to runtime parsing with dynamic format evaluation
- Handles null format expressions by returning a null literal with appropriate data type

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require shuffle operations
- Maintains existing partition boundaries since it operates row-by-row
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null input string**: Returns null result
- **Null format**: When format expression evaluates to null, returns null literal
- **Invalid format**: Handled by underlying `ToTimeParser` implementation
- **Unparseable time strings**: Behavior depends on `ToTimeParser` implementation
- **Non-foldable format**: Falls back to runtime format evaluation for dynamic format expressions

## Code Generation
This expression uses runtime replacement pattern rather than direct code generation:

- Implements `RuntimeReplaceable` trait, meaning it's replaced by an `Invoke` expression during query planning
- The replacement `Invoke` expression can potentially benefit from code generation depending on the underlying method call
- Actual parsing is delegated to `ToTimeParser.parse()` method calls

## Examples
```sql
-- Parse time with default format
SELECT to_time('12:10:05');

-- Parse time with custom format
SELECT to_time('10:05 AM', 'HH:mm a');

-- Handle null inputs
SELECT to_time(NULL);
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Default parsing
df.select(expr("to_time(time_string)"))

// With format
df.select(expr("to_time(time_string, 'HH:mm:ss')"))

// Direct expression usage
val timeExpr = ToTime(col("time_column").expr)
val timeWithFormatExpr = ToTime(col("time_column").expr, lit("HH:mm").expr)
```

## See Also

- Time-related expressions and functions
- `TimeType` data type documentation
- Date/time parsing expressions
- `RuntimeReplaceable` expression pattern