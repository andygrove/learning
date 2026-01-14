# ILike

## Overview

ILike is a case-insensitive pattern matching expression that performs SQL LIKE operations without regard to case. It is implemented as a runtime-replaceable expression that internally converts both the input string and pattern to lowercase before applying the standard LIKE operation.

## Syntax

```sql
column ILIKE pattern [ESCAPE escape_char]
```

```scala
// DataFrame API usage
df.filter(col("column_name").like(pattern.toLowerCase))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The input string expression to match against |
| right | Expression | The pattern expression containing wildcards (% and _) |
| escapeChar | Char | Optional escape character for literal wildcard matching (defaults to '\\') |

## Return Type

Returns `BooleanType` - true if the pattern matches the input string (case-insensitive), false otherwise.

## Supported Data Types

- **Input types**: StringTypeBinaryLcase and StringTypeWithCollation
- **Pattern types**: String expressions with SQL LIKE wildcards
- **Escape character**: Single character or character expression

## Algorithm

- Converts the left expression (input string) to lowercase using the Lower function
- Converts the right expression (pattern) to lowercase using the Lower function
- Delegates to the standard Like expression with the lowercase inputs
- Applies SQL LIKE pattern matching rules with % (any sequence) and _ (single character) wildcards
- Honors the escape character for literal wildcard matching

## Partitioning Behavior

- **Preserves partitioning**: No, this is a filtering predicate that can change data distribution
- **Requires shuffle**: No, operates on individual rows without requiring data movement
- **Push-down eligible**: Yes, can be pushed down to data sources that support case-insensitive LIKE operations

## Edge Cases

- **Null handling**: Returns null if either input string or pattern is null
- **Empty input**: Empty string matches only empty patterns or patterns that can match empty (e.g., "%")
- **Empty pattern**: Matches only empty strings
- **Escape character**: When escape character precedes % or _, treats them as literal characters
- **Unicode considerations**: Lowercase conversion follows Unicode case mapping rules

## Code Generation

This expression supports code generation through its RuntimeReplaceable interface. The replacement expression (Like with Lower transformations) is code-generated, providing efficient execution through Tungsten code generation rather than interpreted evaluation.

## Examples

```sql
-- Basic case-insensitive matching
SELECT * FROM users WHERE name ILIKE 'john%';

-- Using escape character for literal wildcards
SELECT * FROM products WHERE code ILIKE 'ABC\_%' ESCAPE '\';

-- Pattern with multiple wildcards
SELECT * FROM emails WHERE address ILIKE '%@gmail.com';
```

```scala
// DataFrame API equivalent
import org.apache.spark.sql.functions._

// Case-insensitive pattern matching
df.filter(lower(col("name")).like("john%"))

// Using DataFrame filter with ilike-equivalent logic
df.filter(lower(col("code")).like("abc\\_%"))
```

## See Also

- **Like**: Case-sensitive pattern matching expression
- **RLike**: Regular expression matching with standard regex syntax
- **Lower**: String case conversion function used internally
- **StringRegexExpression**: Base functionality for string pattern matching