# RegExpCount

## Overview
The `RegExpCount` expression counts the number of matches of a regular expression pattern in a string. It is implemented as a runtime-replaceable expression that internally uses `RegExpExtractAll` combined with `Size` to count the extracted matches.

## Syntax
```sql
regexp_count(str, pattern)
```

```scala
regexp_count(col("str"), lit("pattern"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | String | The input string to search for pattern matches |
| pattern | String | The regular expression pattern to match against |

## Return Type
Returns an `Integer` representing the count of pattern matches found in the input string.

## Supported Data Types

- **Input string (str)**: String types with binary lowercase collation support
- **Pattern**: String types with collation support
- **Output**: Integer type

## Algorithm

- Internally delegates to `RegExpExtractAll(left, right, Literal(0))` to extract all matches of the pattern
- Uses `Size()` function with `legacySizeOfNull = false` to count the number of extracted matches
- The `Literal(0)` parameter indicates extraction of the entire matched pattern (group 0)
- Implements implicit casting to ensure proper input type conversion
- Acts as a `RuntimeReplaceable` expression, meaning it gets replaced during query planning

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle as it operates on individual rows
- Can be executed in parallel across partitions
- Maintains the same partitioning scheme as the input DataFrame

## Edge Cases

- **Null input string**: Returns null when the input string is null
- **Null pattern**: Returns null when the pattern is null  
- **Empty string**: Returns 0 for empty input strings
- **Invalid regex pattern**: May throw runtime exception for malformed regular expressions
- **No matches found**: Returns 0 when no matches are found

## Code Generation
This expression supports Spark's Tungsten code generation through its replacement mechanism. Since it's a `RuntimeReplaceable` expression, the actual code generation is handled by the underlying `RegExpExtractAll` and `Size` expressions.

## Examples
```sql
-- Count occurrences of digits in a string
SELECT regexp_count('abc123def456', '[0-9]+');
-- Returns: 2

-- Count word boundaries
SELECT regexp_count('hello world test', '\\b\\w+\\b');
-- Returns: 3

-- No matches case
SELECT regexp_count('abc', '[0-9]');
-- Returns: 0
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(regexp_count(col("text"), lit("[0-9]+")))

// Count email patterns
df.select(regexp_count(col("content"), lit("\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b")))
```

## See Also

- `RegExpExtractAll` - Extracts all matches of a pattern
- `RegExpExtract` - Extracts specific groups from pattern matches
- `RegExpReplace` - Replaces pattern matches with specified strings
- `Size` - Returns the size of arrays, maps, or strings