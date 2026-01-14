# StringTrimLeft

## Overview

The `StringTrimLeft` expression removes leading whitespace characters from the left side of a string. It extends the `String2TrimExpression` base class and supports both single-argument (trimming whitespace) and two-argument (trimming custom characters) variants. This expression has been available since Spark 1.5.0 and is part of the string functions group.

## Syntax

```sql
LTRIM(string_expr)
LTRIM(string_expr, trim_chars)
```

```scala
// DataFrame API usage
ltrim(col("column_name"))
ltrim(col("column_name"), lit("chars_to_trim"))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| srcStr | Expression | The source string expression to trim characters from |
| trimStr | Option[Expression] | Optional expression specifying characters to trim (defaults to whitespace) |

## Return Type

Returns `UTF8String` - the input string with leading characters removed.

## Supported Data Types

- String types with non-CSAI (Case Sensitive Accent Insensitive) collation support
- Both source and trim string arguments must support trim collation operations
- Input types are validated as `StringTypeNonCSAICollation(supportsTrimCollation = true)`

## Algorithm

- Evaluates the source string expression to get the input string
- If no trim string is provided, removes leading whitespace characters using default trimming behavior
- If a trim string is provided, removes leading occurrences of any characters found in the trim string
- Uses `CollationSupport.StringTrimLeft.exec()` for the actual trimming operation, respecting collation rules
- Direction is specified as "LEADING" to indicate left-side trimming only

## Partitioning Behavior

This expression preserves partitioning characteristics:

- Does not require data shuffle as it operates on individual string values
- Maintains existing partitioning scheme since it's a row-level transformation
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- Null input: Returns null if the source string is null
- Empty string input: Returns empty string unchanged
- Null trim string: Falls back to whitespace trimming behavior
- Empty trim string: May return the original string unchanged
- Collation handling: Respects the collation rules specified by `collationId` when using custom trim characters

## Code Generation

This expression supports Catalyst code generation through the `CollationSupport.StringTrimLeft.exec()` method calls. The code generation path is optimized for performance and avoids object creation in the hot path when possible.

## Examples

```sql
-- Basic whitespace trimming
SELECT LTRIM('    SparkSQL   ');
-- Result: 'SparkSQL   '

-- Custom character trimming  
SELECT LTRIM('###SparkSQL###', '#');
-- Result: 'SparkSQL###'

-- Trimming multiple characters
SELECT LTRIM('.,!Hello World!,.', '.!,');
-- Result: 'Hello World!,.'
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Trim leading whitespace
df.select(ltrim(col("text_column")))

// Trim custom characters
df.select(ltrim(col("text_column"), lit("#.")))
```

## See Also

- `StringTrimRight` - removes trailing characters from the right side
- `StringTrim` - removes characters from both sides of a string  
- `String2TrimExpression` - base class for trimming operations
- `CollationSupport` - provides collation-aware string operations