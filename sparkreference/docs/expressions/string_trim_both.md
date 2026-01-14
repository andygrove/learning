# StringTrimBoth

## Overview
StringTrimBoth is a runtime replaceable expression that removes specified characters from both the beginning and end of a string. It serves as a wrapper around the StringTrim expression and provides the SQL function `btrim` for bilateral string trimming operations.

## Syntax
```sql
btrim(string_expr [, trim_chars])
```

```scala
// DataFrame API usage through SQL expression
col("string_column").expr("btrim(string_column, ' ')")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| srcStr | Expression | The source string expression to be trimmed |
| trimStr | Option[Expression] | Optional expression specifying characters to trim. If not provided, whitespace characters are trimmed |

## Return Type
Returns a String type containing the trimmed result.

## Supported Data Types

- String types for the source string argument

- String types for the optional trim characters argument

## Algorithm

- Inherits the trimming logic from the underlying StringTrim expression through runtime replacement

- When trimStr is provided, removes all occurrences of those characters from both ends of the source string

- When trimStr is omitted, defaults to trimming whitespace characters from both ends

- Operates as a RuntimeReplaceable expression, delegating actual execution to StringTrim

- Supports both single-argument (whitespace trimming) and two-argument (custom character trimming) variants

## Partitioning Behavior

- Preserves partitioning as it operates on individual string values without requiring data redistribution

- Does not require shuffle operations since trimming is applied row-by-row

## Edge Cases

- Returns null when the source string is null

- Returns null when the trim characters argument is null

- Returns empty string when the source string contains only the characters specified for trimming

- When trim string is empty, returns the original source string unchanged

## Code Generation
As a RuntimeReplaceable expression, StringTrimBoth delegates code generation to its replacement expression (StringTrim), which supports Tungsten code generation for optimal performance.

## Examples
```sql
-- Trim whitespace from both ends
SELECT btrim('  hello world  ');
-- Result: 'hello world'

-- Trim specific characters from both ends  
SELECT btrim('xxxhello worldxxx', 'x');
-- Result: 'hello world'

-- Example from source code documentation
SELECT btrim(encode('SSparkSQLS', 'utf-8'), encode('SL', 'utf-8'));
-- Result: 'parkSQ'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Trim whitespace
df.select(expr("btrim(column_name)"))

// Trim specific characters
df.select(expr("btrim(column_name, 'abc')"))
```

## See Also

- StringTrim - The underlying expression that performs the actual trimming logic

- StringTrimLeft (ltrim) - For trimming characters from the left side only

- StringTrimRight (rtrim) - For trimming characters from the right side only