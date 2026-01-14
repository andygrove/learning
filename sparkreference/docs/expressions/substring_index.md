# SubstringIndex

## Overview
The `SubstringIndex` expression returns a substring from a string before a specified number of occurrences of a delimiter. It supports both positive and negative count values to extract substrings from the beginning or end of the string respectively.

## Syntax
```sql
SUBSTRING_INDEX(str, delim, count)
```

```scala
// DataFrame API
substring_index(col("column_name"), "delimiter", count)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| strExpr | StringType | The input string to extract substring from |
| delimExpr | StringType | The delimiter string to search for |
| countExpr | IntegerType | Number of delimiter occurrences (positive for left-to-right, negative for right-to-left) |

## Return Type
Returns the same `StringType` as the input string expression, preserving the original collation settings.

## Supported Data Types

- Input string: StringType with non-CSAI collations that support trim operations
- Delimiter: StringType with non-CSAI collations that support trim operations  
- Count: IntegerType only

## Algorithm
The expression evaluation follows these steps:

- Delegates actual substring extraction to `CollationSupport.SubstringIndex.exec()`
- If count is positive, searches for delimiter occurrences from left to right and returns substring before the nth occurrence
- If count is negative, searches for delimiter occurrences from right to left and returns substring after the nth occurrence from the end
- Respects the collation settings of the input string for comparison operations
- Uses collation-aware string operations through the CollationSupport framework

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffle as it operates on individual rows
- Maintains existing partitioning scheme since it's a deterministic row-level transformation
- Can be safely pushed down in query optimization

## Edge Cases

- **Null handling**: Expression is null-intolerant, returns null if any input (string, delimiter, or count) is null
- **Empty string input**: Returns empty string when input string is empty
- **Empty delimiter**: Behavior depends on CollationSupport implementation for the specific collation
- **Count of zero**: Returns empty string
- **Delimiter not found**: Returns entire original string if delimiter doesn't exist and count > 0, empty string if count < 0
- **Count exceeds occurrences**: Returns substring up to available delimiter occurrences

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which delegates to `CollationSupport.SubstringIndex.genCode()` for efficient runtime execution without interpreter overhead.

## Examples
```sql
-- Extract domain from email (everything after @)
SELECT SUBSTRING_INDEX('user@domain.com', '@', -1) AS domain;
-- Returns: 'domain.com'

-- Extract username from email (everything before @)  
SELECT SUBSTRING_INDEX('user@domain.com', '@', 1) AS username;
-- Returns: 'user'

-- Get first two path components
SELECT SUBSTRING_INDEX('/home/user/documents/file.txt', '/', 3) AS partial_path;
-- Returns: '/home/user'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(substring_index(col("email"), "@", -1).as("domain"))
df.select(substring_index(col("filepath"), "/", 2).as("base_path"))
```

## See Also

- `substring` - Extract substring by position and length
- `split` - Split string into array by delimiter
- `regexp_extract` - Extract substring using regular expressions