# StringTranslate

## Overview
The `StringTranslate` expression performs character-by-character translation on a string by replacing characters found in a matching string with corresponding characters from a replacement string. It builds a translation dictionary from the matching and replacement strings, then applies this mapping to transform the source string.

## Syntax
```sql
TRANSLATE(source_string, matching_characters, replacement_characters)
```

```scala
// DataFrame API
translate(source_col, matching_string, replacement_string)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| srcExpr | StringType | The source string to be translated |
| matchingExpr | StringType | String containing characters to be replaced |
| replaceExpr | StringType | String containing replacement characters |

## Return Type
Returns `StringType` with the same data type as the source expression, preserving collation settings.

## Supported Data Types

- All three arguments must be StringType with non-CSAI collation
- Supports trim collation
- Preserves the collation ID from the source expression

## Algorithm

- Builds a character translation dictionary by mapping characters from `matchingExpr` to corresponding positions in `replaceExpr`
- Caches the translation dictionary when matching and replacement strings remain unchanged
- Iterates through each character in the source string and applies the translation mapping
- Uses collation-aware string processing through `CollationSupport.StringTranslate.exec`
- Delegates dictionary construction to `StringTranslate.buildDict` utility method

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows without requiring data movement:

- Does not require shuffle operations
- Maintains existing data distribution
- Can be executed independently on each partition

## Edge Cases

- **Null handling**: Returns null if any input argument is null (null intolerant behavior)
- **Mismatched lengths**: When replacement string is shorter than matching string, excess matching characters are handled by the `buildDict` implementation
- **Empty strings**: Empty matching or replacement strings result in no character translation
- **Duplicate characters**: If matching string contains duplicate characters, behavior depends on the dictionary building logic
- **Collation sensitivity**: Translation respects the collation settings of the input strings

## Code Generation
Supports Tungsten code generation for optimized performance:

- Generates mutable state variables for caching translation dictionary
- Optimizes dictionary rebuild checks for foldable (literal) expressions
- Uses `nullSafeCodeGen` for efficient null handling in generated code
- Falls back to interpreted mode only when code generation fails

## Examples
```sql
-- Replace vowels with numbers
SELECT TRANSLATE('Apache Spark', 'aeiou', '12345');
-- Result: 'Ap1ch2 Sp1rk'

-- Remove characters by providing shorter replacement string
SELECT TRANSLATE('hello world', 'aeiou', '12');
-- Result: 'h2ll wrld'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.translate

df.select(translate(col("name"), "aeiou", "12345"))

// Using column expressions
df.withColumn("translated", translate($"text", lit("abc"), lit("123")))
```

## See Also

- `StringReplace` - For substring-based replacement operations
- `RegExpReplace` - For pattern-based string replacement using regular expressions
- `Overlay` - For replacing substrings at specific positions