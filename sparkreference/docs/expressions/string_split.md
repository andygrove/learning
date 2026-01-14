# StringSplit

## Overview
The StringSplit expression splits a string into an array of substrings using a regular expression pattern as the delimiter. It provides control over the maximum number of splits through an optional limit parameter, and supports collation-aware string processing.

## Syntax
```sql
SPLIT(str, regex [, limit])
```

```scala
// DataFrame API
col("column").split(regex, limit)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | String | The input string to be split |
| regex | String | The regular expression pattern used as delimiter |
| limit | Integer (optional) | Maximum number of splits to perform. Defaults to -1 (no limit) |

## Return Type
Returns `ArrayType(StringType, containsNull = false)` - an array of strings that cannot contain null elements.

## Supported Data Types

- **Input string**: StringType with binary lowercase collation support and collation-aware string types
- **Regex pattern**: StringType with collation support  
- **Limit**: IntegerType only

## Algorithm

- Extracts collation information from the input string data type for collation-aware regex processing
- Creates a collation-aware regex pattern using `CollationSupport.collationAwareRegex()`
- Applies either legacy truncation split behavior or standard split based on `LEGACY_TRUNCATE_FOR_EMPTY_REGEX_SPLIT` configuration
- Performs the actual split operation using UTF8String's split methods with the compiled pattern and limit
- Wraps the resulting string array in a `GenericArrayData` structure

## Partitioning Behavior
How this expression affects partitioning (if applicable):

- Preserves partitioning as it operates on individual rows without requiring data movement
- Does not require shuffle operations since it's a row-level transformation

## Edge Cases

- **Null handling**: The expression is null intolerant (`nullIntolerant = true`), meaning if any input is null, the result is null
- **Empty regex**: Behavior depends on the `LEGACY_TRUNCATE_FOR_EMPTY_REGEX_SPLIT` configuration setting
- **Negative limit**: Default limit of -1 means no limit on splits
- **Zero limit**: Follows Java Pattern.split() semantics
- **Collation sensitivity**: Regex matching respects the collation settings of the input string type

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, generating optimized Java code that avoids object creation overhead and uses direct UTF8String split operations.

## Examples
```sql
-- Basic string splitting
SELECT SPLIT('apple,banana,cherry', ',');
-- Result: ["apple", "banana", "cherry"]

-- Splitting with limit
SELECT SPLIT('oneAtwoBthreeC', '[ABC]', 2);
-- Result: ["one", "twoBthreeC"]

-- Splitting with regex pattern
SELECT SPLIT('word1 word2 word3', '\\s+');
-- Result: ["word1", "word2", "word3"]
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(split(col("text_column"), ","))
df.select(split(col("text_column"), "\\s+", 3))
```

## See Also

- `RegExpReplace` - for replacing matches with replacement strings
- `RegExpExtract` - for extracting specific groups from regex matches
- `SubstringIndex` - for simpler delimiter-based string splitting without regex support