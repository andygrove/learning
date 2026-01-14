# RegExpSubStr

## Overview
RegExpSubStr extracts the first substring from an input string that matches a specified regular expression pattern. This expression is implemented as a runtime replaceable expression that internally uses RegExpExtract to find matches and NullIf to handle empty results, returning NULL when no match is found.

## Syntax
```sql
regexp_substr(string, pattern)
```

```scala
regexp_substr(col("string_column"), lit("pattern"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| string | String/Binary (case-insensitive) | The input string to search within |
| pattern | String (with collation support) | The regular expression pattern to match |

## Return Type
String - Returns the first matching substring, or NULL if no match is found.

## Supported Data Types

- **Input string**: StringTypeBinaryLcase (string and binary types with case-insensitive behavior)
- **Pattern**: StringTypeWithCollation (string types with collation support)
- **Output**: Same string type as the input string

## Algorithm

- Internally delegates to RegExpExtract with index 0 to extract the entire first match
- Wraps the result with NullIf to convert empty string results to NULL
- Uses implicit type casting to ensure input compatibility
- Pattern matching follows standard regular expression semantics
- Returns the complete matched substring (not capture groups)

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning since it operates on individual rows independently
- Does not require shuffle operations
- Can be pushed down in query optimization

## Edge Cases

- **Null inputs**: Returns NULL if either the input string or pattern is NULL
- **Empty string input**: Returns NULL if the input string is empty and pattern doesn't match empty strings
- **Empty pattern**: Behavior follows standard regex semantics for empty patterns
- **Invalid regex**: May throw runtime exceptions for malformed regular expression patterns
- **No match found**: Returns NULL when the pattern doesn't match any part of the input string

## Code Generation
This expression uses runtime replacement and does not directly support Tungsten code generation. The underlying RegExpExtract and NullIf expressions may support code generation depending on their implementation.

## Examples
```sql
-- Extract email domains
SELECT regexp_substr('contact@example.com', '[^@]+@([^.]+)') AS result;
-- Returns: 'contact@example.com'

-- Extract first word
SELECT regexp_substr('Hello World', '[A-Za-z]+') AS first_word;
-- Returns: 'Hello'

-- No match case
SELECT regexp_substr('12345', '[A-Za-z]+') AS no_match;
-- Returns: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(regexp_substr(col("email"), lit("[^@]+@([^.]+)"))).show()

// Extract phone number pattern
df.select(regexp_substr(col("text"), lit("\\d{3}-\\d{3}-\\d{4}"))).show()
```

## See Also

- RegExpExtract - For extracting specific capture groups from regex matches
- RegExpReplace - For replacing matched patterns with new strings
- RLike - For boolean regex matching operations
- NullIf - Used internally for NULL handling