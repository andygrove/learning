# StringSplitSQL

## Overview
StringSplitSQL is a Spark Catalyst expression that splits a string into an array of substrings using a delimiter. Unlike the `split` function which treats the pattern as a regular expression, this expression treats the delimiter as a literal string without any special regex meaning.

## Syntax
```sql
-- SQL usage (internal expression, typically used through string functions)
STRING_SPLIT_SQL(string_expr, delimiter_expr)
```

```scala
// DataFrame API usage (internal expression)
StringSplitSQL(stringColumn, delimiterColumn)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | Expression | The input string expression to be split |
| delimiter | Expression | The delimiter string used to split the input string |

## Return Type
Returns `ArrayType(StringType, containsNull = false)` - an array of strings where null values are not allowed within the array elements.

## Supported Data Types

- Input string: StringType (with collation support)
- Delimiter: StringType (with collation support)
- Both expressions must have compatible string types with collation information

## Algorithm

- Extracts collation ID from the input string's data type for proper string comparison
- Uses `CollationSupport.StringSplitSQL.exec()` to perform the actual string splitting operation
- Treats the delimiter as a literal string rather than a regex pattern
- Wraps the resulting string array in a `GenericArrayData` structure
- Supports both interpreted evaluation and code generation for performance optimization

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be applied within existing partitions independently

## Edge Cases

- **Null handling**: Expression is null intolerant - returns null if either input string or delimiter is null
- **Empty delimiter**: Behavior depends on the underlying `CollationSupport.StringSplitSQL.exec()` implementation
- **Empty string**: Returns an array with appropriate handling based on collation rules
- **Delimiter not found**: Returns array with single element containing the original string
- **Collation awareness**: Respects the collation settings of the input string type for proper character comparison

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method:

- Uses `nullSafeCodeGen` for efficient null checking
- Generates optimized Java code using `CollationSupport.StringSplitSQL.genCode()`
- Falls back to interpreted mode if code generation is not available
- Leverages Java array covariance for efficient UTF8String array handling

## Examples
```sql
-- Example SQL usage (internal function)
SELECT STRING_SPLIT_SQL('apple,banana,cherry', ',') AS fruits;
-- Result: ['apple', 'banana', 'cherry']

SELECT STRING_SPLIT_SQL('hello world test', ' ') AS words;  
-- Result: ['hello', 'world', 'test']
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.catalyst.expressions.StringSplitSQL
import org.apache.spark.sql.functions.col

// Internal expression usage
val splitExpr = StringSplitSQL(col("text"), col("delimiter"))
df.select(splitExpr.as("split_result"))
```

## See Also

- `Split` - Regular expression-based string splitting function
- `StringSplit` - Alternative string splitting implementations
- `CollationSupport` - Collation-aware string operations
- `GenericArrayData` - Array data structure used for results