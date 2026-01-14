# RLike

## Overview
RLike is a regular expression matching predicate function that determines whether a string matches a given regular expression pattern. It performs pattern matching using Java's Pattern class and returns true if the pattern is found anywhere within the input string.

## Syntax
```sql
RLIKE(string_expr, pattern_expr)
```

```scala
// DataFrame API
col("string_column").rlike("pattern")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The input string expression to be matched against the pattern |
| right | Expression | The regular expression pattern as a string expression |

## Return Type
Boolean - returns true if the pattern matches, false otherwise, or null if either input is null.

## Supported Data Types

- Input string: String/UTF8String types
- Pattern: String/UTF8String types
- Output: BooleanType

## Algorithm

- Compiles the right-hand expression into a Java Pattern object with collation-specific regex flags
- Uses Pattern.matcher() to create a Matcher for the input string
- Calls find(0) to search for the pattern starting from position 0 in the string
- Returns true if any occurrence of the pattern is found anywhere in the string
- Handles null values by returning null if either operand is null

## Partitioning Behavior
How this expression affects partitioning:

- Preserves existing partitioning as it operates row-by-row without requiring data movement
- Does not require shuffle operations
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- Null handling: Returns null if either the input string or pattern is null
- Empty string behavior: Empty string ("") will match patterns that can match zero characters
- Invalid regex patterns: Will throw PatternSyntaxException during compilation
- Case sensitivity: Follows collation-specific regex flags for case matching rules
- Unicode handling: Supports Unicode characters through UTF8String processing

## Code Generation
This expression supports full Tungsten code generation with optimizations:

- When the pattern is foldable (constant), it pre-compiles the Pattern object as a mutable state
- For non-constant patterns, generates code to compile the pattern at runtime
- Uses nullSafeCodeGen for dynamic pattern scenarios to handle null safety efficiently

## Examples
```sql
-- Match strings containing digits
SELECT name FROM users WHERE RLIKE(name, '[0-9]+');

-- Match email patterns
SELECT email FROM contacts WHERE RLIKE(email, '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$');

-- Case-sensitive pattern matching
SELECT product FROM inventory WHERE RLIKE(product, 'iPhone.*Pro');
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Match strings with specific pattern
df.filter(col("description").rlike("\\d{3}-\\d{3}-\\d{4}"))

// Find records with alphanumeric codes
df.where($"code".rlike("[A-Z]{2}[0-9]{4}"))
```

## See Also

- Like - for simple pattern matching with wildcards
- RegExpReplace - for pattern-based string replacement
- RegExpExtract - for extracting substrings using regular expressions
- StringRegexExpression - the parent class for regex-based string operations