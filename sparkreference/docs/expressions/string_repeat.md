# StringRepeat

## Overview
The `StringRepeat` expression repeats a string a specified number of times by concatenating it with itself. It takes a string input and an integer count, returning a new string that contains the original string repeated the specified number of times.

## Syntax
```sql
repeat(str, n)
```

```scala
// DataFrame API
col("column_name").repeat(n)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | StringTypeWithCollation | The input string to be repeated |
| times | IntegerType | The number of times to repeat the string |

## Return Type
Returns the same data type as the input string (`str.dataType`), which is a string type with collation support.

## Supported Data Types

- **Input string**: String types with collation support (including trim collation)
- **Input count**: Integer type only
- Implicit casting is supported through `ImplicitCastInputTypes`

## Algorithm

- Validates that both input expressions are not null (null intolerant behavior)
- Casts the string input to `UTF8String` format internally
- Casts the times parameter to `Integer` type
- Calls the native `repeat()` method on the UTF8String object
- Returns the concatenated result as a UTF8String

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning since it's a row-level transformation
- Does not require shuffle operations
- Can be applied within each partition independently

## Edge Cases

- **Null handling**: Returns null if either input argument is null (null intolerant)
- **Zero repetitions**: Returns empty string when times = 0
- **Negative repetitions**: Behavior depends on underlying UTF8String.repeat() implementation
- **Empty string input**: Returns empty string regardless of repetition count
- **Large repetition counts**: May cause memory issues or overflow depending on string length

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method. It generates optimized code that directly calls the `repeat()` method on UTF8String objects, avoiding interpretation overhead.

## Examples
```sql
-- Basic usage
SELECT repeat('123', 2);
-- Result: '123123'

-- With column reference
SELECT repeat(name, 3) FROM table;

-- Zero repetitions
SELECT repeat('abc', 0);
-- Result: ''
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(repeat(col("text_column"), 3))

// With literal values
df.select(repeat(lit("hello"), 2))
```

## See Also

- `StringRepeat` - Current expression for string repetition
- `Concat` - For concatenating multiple strings
- `StringPad` - For padding strings to specific lengths
- Other string manipulation functions in the string_funcs group