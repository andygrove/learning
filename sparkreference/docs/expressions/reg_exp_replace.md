# RegExpReplace

## Overview
The `RegExpReplace` expression performs regular expression-based string replacement operations. It searches for occurrences of a regular expression pattern in a subject string and replaces them with a replacement string, starting from a specified position.

## Syntax
```sql
REGEXP_REPLACE(subject, regexp, rep[, pos])
```

```scala
// DataFrame API
col("subject").regexp_replace(regexp, replacement)
// or with position
regexp_replace(col("subject"), regexp, replacement, position)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| subject | StringType | The input string to search within |
| regexp | StringType | The regular expression pattern to search for |
| rep | StringType | The replacement string |
| pos | IntegerType | Starting position for the search (1-based, defaults to 1) |

## Return Type
Returns the same `StringType` as the subject input, preserving collation settings.

## Supported Data Types

- Subject: String types with binary lowercase collation support
- Pattern: String types with collation support  
- Replacement: String types with binary lowercase collation support
- Position: Integer type only

## Algorithm

- Validates that the position parameter is foldable (constant) and greater than 0
- Caches compiled regex patterns for performance when the pattern hasn't changed
- Converts 1-based position to 0-based for internal Java regex operations
- Uses Java's `Matcher.region()` to limit search scope to the specified starting position
- Applies `appendReplacement()` and `appendTail()` for efficient string building
- Returns original subject string if position is beyond string length

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows without requiring data movement:

- Does not require shuffle operations
- Maintains existing partitioning scheme
- Can be pushed down to individual partitions

## Edge Cases

- Returns null if any input parameter is null (null intolerant behavior)
- Returns original subject string unchanged if position exceeds string length
- Position parameter must be a constant expression (foldable) and positive
- Invalid regex patterns throw compilation errors at evaluation time
- Invalid replacement strings (e.g., invalid group references) throw runtime errors
- Empty subject strings are handled gracefully, returning empty results

## Code Generation
This expression supports Tungsten code generation for optimized performance. It generates specialized bytecode that:

- Caches compiled regex patterns and replacement strings
- Uses efficient string building with `StringBuilder`
- Includes proper exception handling for invalid regex operations
- Avoids object allocation in the hot path when possible

## Examples
```sql
-- Basic replacement
SELECT REGEXP_REPLACE('Hello World', 'World', 'Spark');
-- Result: 'Hello Spark'

-- With position parameter
SELECT REGEXP_REPLACE('abc abc abc', 'abc', 'xyz', 5);
-- Result: 'abc xyz xyz'

-- Using capture groups
SELECT REGEXP_REPLACE('2023-12-25', '(\\d{4})-(\\d{2})-(\\d{2})', '$3/$2/$1');
-- Result: '25/12/2023'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(regexp_replace(col("text"), "old", "new"))

// With position
df.select(regexp_replace(col("text"), "pattern", "replacement", 3))
```

## See Also

- `RegExpExtract` - Extract substrings using regular expressions
- `RegExpCount` - Count regex pattern matches
- `Like` - Simple pattern matching with wildcards
- `RLike` - Regular expression matching (boolean result)