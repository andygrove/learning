# StringSpace

## Overview
The `StringSpace` expression creates a string consisting of a specified number of space characters. It takes an integer argument representing the desired length and returns a UTF-8 string filled with that many spaces.

## Syntax
```sql
SPACE(length)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
space(col("length_column"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| length | Integer | The number of space characters to generate |

## Return Type
`UTF8String` - A string containing the specified number of space characters.

## Supported Data Types

- Input: `IntegerType` only
- Implicit casting is supported for compatible numeric types that can be cast to integer

## Algorithm

- Validates that the input is an integer type through implicit cast input types
- Evaluates the length parameter as an integer value
- If the length is negative, it defaults to 0 (no spaces)
- Uses `UTF8String.blankString()` to efficiently generate a string of spaces
- Returns the resulting UTF-8 string with the specified number of spaces

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require shuffle operations
- Can be evaluated independently on each partition
- Does not affect data distribution or partitioning scheme

## Edge Cases

- **Null handling**: Expression is null-intolerant, meaning null inputs result in null output
- **Negative values**: Negative length values are treated as 0, resulting in an empty string
- **Zero length**: Returns an empty string when length is 0
- **Large values**: Limited by available memory and UTF8String implementation constraints

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method:

- Implements `nullSafeCodeGen` for efficient compiled code execution
- Generates optimized bytecode that avoids object creation overhead
- Falls back to interpreted mode only when code generation is disabled

## Examples
```sql
-- Basic usage
SELECT SPACE(5);
-- Result: '     ' (5 spaces)

-- With negative number
SELECT SPACE(-3);
-- Result: '' (empty string)

-- Combined with other functions
SELECT CONCAT(SPACE(2), '1');
-- Result: '  1'

-- Using with column values
SELECT name, SPACE(padding_length) AS spaces FROM table;
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Basic usage
df.select(space(lit(5)))

// With column reference
df.select(space(col("length_column")))

// Combined with other functions
df.select(concat(space(lit(3)), col("text")))
```

## See Also

- `CONCAT` - For combining the space string with other strings
- `REPEAT` - For repeating other characters besides spaces
- `LPAD`/`RPAD` - For padding strings with spaces or other characters