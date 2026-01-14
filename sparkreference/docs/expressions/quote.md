# Quote

## Overview
The Quote expression adds single quotes around a string value, escaping any existing single quotes within the string by doubling them. This expression is commonly used for preparing string literals for SQL contexts or for display purposes where quoted strings are needed.

## Syntax
```sql
quote(string_expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(quote($"column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| input | StringType | The string expression to be quoted |

## Return Type
StringType - Returns a string with single quotes added around the input value.

## Supported Data Types

- StringType with collation support
- Supports trim collation semantics
- Input values are implicitly cast to string if needed

## Algorithm

- Wraps the input string with single quotes at the beginning and end
- Scans the input string for existing single quote characters
- Doubles any existing single quotes within the string to escape them properly
- Returns the properly quoted and escaped string result
- Handles null inputs by returning null

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle as it operates on individual rows
- Maintains the same partitioning scheme as the input
- Can be safely pushed down to individual partitions

## Edge Cases

- **Null handling**: Returns null when input is null (nullable = true)
- **Empty string**: Returns two single quotes ('') for empty input
- **String with quotes**: Existing single quotes are escaped by doubling them
- **Special characters**: All other special characters are preserved as-is within the quotes

## Code Generation
This expression uses RuntimeReplaceable pattern:

- Delegates actual execution to `ExpressionImplUtils.quote()` method via `StaticInvoke`
- Benefits from Catalyst's code generation optimizations through the static method call
- Supports context-independent constant folding when input is foldable

## Examples
```sql
SELECT quote('Hello World');
-- Result: 'Hello World'

SELECT quote('Don\'t');  
-- Result: 'Don''t'

SELECT quote('');
-- Result: ''

SELECT quote(NULL);
-- Result: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(quote(col("message")))
df.withColumn("quoted_text", quote($"original_text"))

// With literal values
df.select(quote(lit("Hello World")))
```

## See Also

- `concat` - For string concatenation operations
- `regexp_replace` - For pattern-based string transformations  
- `escape` - For other escaping operations
- String literal functions for SQL formatting