# Like

## Overview
The `Like` expression implements SQL LIKE pattern matching for string comparisons using wildcard characters. It converts SQL LIKE patterns to regular expressions and performs pattern matching against input strings, with support for custom escape characters.

## Syntax
```sql
string_expr LIKE pattern_expr [ESCAPE escape_char]
```

```scala
// DataFrame API
col("column_name").like("pattern")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The string expression to match against |
| right | Expression | The pattern expression containing wildcards |
| escapeChar | Char | Character used to escape wildcards (default: '\\') |

## Return Type
Returns `BooleanType` - true if the string matches the pattern, false otherwise.

## Supported Data Types
Supports string-like data types that can be converted to UTF8String:

- StringType
- UTF8String
- Any expression that evaluates to a string representation

## Algorithm
The expression evaluation follows these steps:

- Convert the SQL LIKE pattern to a regular expression using `StringUtils.escapeLikeRegex`
- Compile the escaped pattern into a Java `Pattern` object with appropriate collation flags  
- Use `Pattern.matcher().matches()` to perform full string matching against the input
- Handle null values by returning null when either operand is null
- Cache compiled patterns when the right operand is foldable (constant)

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffling as it operates on individual rows
- Can be pushed down to data sources that support LIKE operations
- Maintains existing partitioning scheme when used in filters

## Edge Cases

- **Null handling**: Returns null if either the input string or pattern is null
- **Empty pattern**: Empty string pattern matches only empty strings
- **Invalid regex**: Malformed patterns after conversion will cause runtime exceptions
- **Escape character**: Custom escape characters must be single characters; invalid escape expressions throw exceptions
- **Case sensitivity**: Matching behavior depends on collation settings via `collationRegexFlags`

## Code Generation
Supports Tungsten code generation with optimizations:

- **Constant patterns**: Pre-compiles patterns at code generation time when right operand is foldable
- **Variable patterns**: Generates code to compile patterns at runtime for non-constant patterns
- **Null safety**: Generates efficient null-checking code without re-evaluating expressions
- **Java escaping**: Properly escapes special characters for valid generated Java code

## Examples
```sql
-- Basic wildcard matching
SELECT * FROM table WHERE name LIKE 'John%'

-- Custom escape character
SELECT * FROM table WHERE description LIKE 'Price: $100\%' ESCAPE '\'

-- Multiple wildcards
SELECT * FROM table WHERE email LIKE '%@%.com'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.filter(col("name").like("John%"))
df.filter(col("description").like("Price: $100\\%"))
```

## See Also

- `RLike` - Regular expression matching with standard regex syntax
- `ILike` - Case-insensitive LIKE matching
- `StringRegexExpression` - Base class for string pattern matching expressions