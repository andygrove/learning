# Ascii

## Overview
The `Ascii` expression returns the ASCII code point value of the first character in a string. If the input string is empty, it returns 0.

## Syntax
```sql
ASCII(string_expr)
```

```scala
// DataFrame API
col("column_name").ascii()
// or using expr
expr("ascii(column_name)")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | StringType with Collation | The input string expression from which to extract the first character's ASCII value |

## Return Type
`IntegerType` - Returns the ASCII code point value as an integer.

## Supported Data Types

- StringType with collation support (including trim collation)

- Input is implicitly cast to string type if necessary

## Algorithm

- Extract the first character from the input UTF8String using `substring(0, 1)`

- Check if the substring contains any characters (`numChars > 0`)

- If characters exist, convert to string and get the code point at position 0 using `codePointAt(0)`

- If no characters exist (empty string), return 0

- Null inputs result in null output (null intolerant behavior)

## Partitioning Behavior
This expression preserves partitioning as it operates on individual row values without requiring data movement or shuffle operations between partitions.

## Edge Cases

- **Null handling**: Returns null for null input (null intolerant)

- **Empty string**: Returns 0 for empty strings

- **Multi-character strings**: Only processes the first character, ignoring the rest

- **Unicode characters**: Uses `codePointAt(0)` which properly handles Unicode code points beyond basic ASCII range

- **Performance optimization**: Uses `substring(0, 1)` to avoid converting the entire string unnecessarily

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, generating optimized Java code that avoids interpreted evaluation overhead.

## Examples
```sql
-- Basic ASCII value lookup
SELECT ASCII('A');  -- Returns 65

-- First character only
SELECT ASCII('Hello');  -- Returns 72 (ASCII value of 'H')

-- Empty string
SELECT ASCII('');  -- Returns 0

-- Null input
SELECT ASCII(NULL);  -- Returns NULL

-- Unicode character
SELECT ASCII('世界');  -- Returns the code point of '世'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(ascii(col("text_column")))

// Using expr
df.select(expr("ascii(text_column)"))

// With column alias
df.select(ascii(col("name")).alias("first_char_ascii"))
```

## See Also

- `Chr` - Converts ASCII code point back to character
- `Substring` - Extracts substrings from text
- `Length` - Returns string length
- Other string manipulation functions in the `string_funcs` group