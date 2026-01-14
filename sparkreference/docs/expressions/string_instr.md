# StringInstr

## Overview
The `StringInstr` expression finds the position of the first occurrence of a substring within a string. It returns a 1-based index where the substring begins, or 0 if the substring is not found.

## Syntax
```sql
INSTR(string, substring)
```

```scala
// DataFrame API
col("string_column").instr("substring")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | Expression (String) | The input string to search within |
| substr | Expression (String) | The substring to search for |

## Return Type
`IntegerType` - Returns an integer representing the 1-based position of the substring.

## Supported Data Types

- Input: `StringTypeNonCSAICollation` with trim collation support for both arguments
- The expression supports collation-aware string matching based on the collation ID of the left operand
- Both string arguments must be compatible string types

## Algorithm

- Extracts the collation ID from the left operand's StringType
- Uses `CollationSupport.StringInstr.exec()` to perform collation-aware substring search
- The internal search returns a 0-based index which is incremented by 1 for SQL compatibility
- Handles UTF8String operations for efficient string processing
- Preserves collation semantics throughout the evaluation process

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning as it operates on individual rows
- Does not require data shuffling
- Can be executed locally on each partition

## Edge Cases

- **Null handling**: Expression is null intolerant - returns null if either input is null
- **Empty string behavior**: Returns 1 when searching for empty string in any non-null string
- **Case sensitivity**: Behavior depends on the collation settings of the input string type
- **Not found**: Returns 0 when substring is not found in the target string
- **Collation mismatch**: Uses the collation ID from the left operand for comparison logic

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method:

- Generates optimized bytecode using `defineCodeGen`
- Leverages `CollationSupport.StringInstr.genCode()` for collation-aware code generation
- Adds 1 to the generated result to maintain 1-based indexing
- Falls back to interpreted mode if code generation is disabled

## Examples
```sql
-- Find position of substring
SELECT INSTR('hello world', 'world'); -- Returns 7

-- Substring not found
SELECT INSTR('hello', 'xyz'); -- Returns 0

-- Case sensitivity depends on collation
SELECT INSTR('Hello', 'hello'); -- Result varies by collation
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("text").instr("pattern").as("position"))

// With string literals
df.select(instr(col("message"), lit("error")).as("error_pos"))
```

## See Also

- `SubstringIndex` - Extract substring based on delimiter and occurrence
- `StringLocate` - Similar functionality with different parameter ordering
- `StringSplit` - Split strings into arrays based on patterns
- `RegExpExtract` - Pattern-based string extraction with regular expressions