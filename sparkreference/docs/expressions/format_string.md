# FormatString

## Overview
FormatString is a Spark Catalyst expression that formats a string using Java's `java.util.Formatter` with a format pattern and variable arguments. It provides sprintf-style string formatting functionality within Spark SQL expressions, allowing dynamic string construction with type-safe parameter substitution.

## Syntax
```sql
format_string(format, arg1, arg2, ...)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
format_string(col("format_pattern"), col("arg1"), col("arg2"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| format | String (with collation support) | The format pattern string following Java Formatter syntax |
| args | Any (variadic) | Variable number of arguments to be formatted according to the pattern |

## Return Type
Returns the same data type as the first argument (format pattern), typically `StringType` or a string type with specific collation.

## Supported Data Types

- **Format pattern**: String types with collation support (including trim collation)
- **Arguments**: Any data type (`AnyDataType`) - will be converted to appropriate Java objects for formatting

## Algorithm

- Evaluates the format pattern expression and checks for null values
- Creates a new `java.util.Formatter` instance with US locale for consistent formatting
- Evaluates all argument expressions and converts them to Java `AnyRef` objects
- Applies Java string formatting using the pattern and argument list
- Returns the formatted result as a `UTF8String`

## Partitioning Behavior
- **Preserves partitioning**: Yes, this is a row-level transformation that doesn't require data movement
- **Requires shuffle**: No, operates independently on each row

## Edge Cases

- **Null format pattern**: Returns null if the format string is null
- **Null arguments**: Null arguments are passed as null objects to the Java formatter
- **Empty arguments**: Requires at least one argument (the format pattern), throws compilation error if empty
- **Zero-index formatting**: Validates against `%0$` format specifiers to ensure Java version compatibility (controlled by `ALLOW_ZERO_INDEX_IN_FORMAT_STRING` configuration)
- **Invalid format patterns**: Will throw runtime exceptions from Java's Formatter if pattern is malformed

## Code Generation
Supports Tungsten code generation with optimized code paths. The generated code:

- Uses `splitExpressionsWithCurrentInputs` for handling large argument lists
- Boxes Java primitives to handle null values properly  
- Creates efficient object arrays for argument passing
- Generates inline null-checking logic

## Examples
```sql
-- Basic string formatting
SELECT format_string('Hello %s, you have %d messages', 'World', 100);
-- Result: "Hello World, you have 100 messages"

-- With positional arguments
SELECT format_string('Hello %2$s, you have %1$d messages', 100, 'World');
-- Result: "Hello World, you have 100 messages"

-- Numeric formatting
SELECT format_string('%.2f%%', 85.6789);
-- Result: "85.68%"
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(format_string(lit("User: %s, Score: %d"), col("username"), col("score")))

// With column-based format patterns
df.select(format_string(col("message_template"), col("arg1"), col("arg2")))
```

## See Also

- `concat()` - Simple string concatenation
- `concat_ws()` - String concatenation with separator
- `printf()` - Alternative name for format_string in some contexts
- String interpolation expressions