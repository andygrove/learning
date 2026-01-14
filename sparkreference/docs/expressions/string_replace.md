# StringReplace

## Overview
The StringReplace expression replaces all occurrences of a search string within a source string with a replacement string. It supports collation-aware string matching and replacement operations, making it suitable for internationalized text processing.

## Syntax
```sql
REPLACE(src, search, replace)
```

```scala
// DataFrame API
col("column").replace(searchStr, replaceStr)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| srcExpr | StringType | The source string expression to search within |
| searchExpr | StringType | The substring to search for in the source string |
| replaceExpr | StringType | The replacement string (optional, defaults to empty string) |

## Return Type
Returns a StringType with the same collation as the source expression.

## Supported Data Types

- StringType with various collations
- Non-case-sensitive-accent-insensitive (Non-CSAI) collations with trim support
- All three arguments must be string types

## Algorithm

- Extracts the collation ID from the source expression's data type
- Uses CollationSupport.StringReplace.exec() for null-safe evaluation
- Performs collation-aware string search and replacement operations
- Handles UTF8String objects internally for efficient string processing
- Supports code generation through CollationSupport.StringReplace.genCode()

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require shuffle operations
- Can be executed locally on each partition
- Output partitioning matches input partitioning scheme

## Edge Cases

- **Null handling**: Expression is null-intolerant, returns null if any argument is null
- **Empty search string**: Behavior depends on underlying CollationSupport implementation
- **Empty source string**: Returns empty string when source is empty
- **No matches found**: Returns original source string unchanged
- **Collation sensitivity**: Matching behavior varies based on the string's collation settings

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which delegates to `CollationSupport.StringReplace.genCode()` for optimal performance in compiled expressions.

## Examples
```sql
-- Replace all occurrences of 'old' with 'new'
SELECT REPLACE('Hello old world old', 'old', 'new');
-- Result: 'Hello new world new'

-- Replace with empty string (removal)
SELECT REPLACE('ABCDEFABCDEF', 'ABC', '');
-- Result: 'DEFDEF'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("replace(column_name, 'search', 'replacement')"))

// Using string interpolation
df.select(col("text_column").replace("old_value", "new_value"))
```

## See Also

- StringTranslate - for character-level replacements
- RegExpReplace - for pattern-based replacements
- StringTrim - for whitespace removal
- CollationSupport - underlying collation support implementation