# StringTrim

## Overview
StringTrim is a Spark Catalyst expression that removes whitespace or specified characters from both ends of a string. It extends String2TrimExpression and supports collation-aware string trimming operations, allowing for either default whitespace trimming or custom character trimming.

## Syntax
```sql
TRIM([BOTH] [trim_string FROM] source_string)
TRIM(source_string)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
trim(col("source_column"))
trim(col("source_column"), "trim_chars")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| srcStr | Expression | The source string to be trimmed |
| trimStr | Option[Expression] | Optional characters to trim from both ends. If None, trims whitespace |

## Return Type
Returns `UTF8String` - the trimmed string result.

## Supported Data Types

- Input types: StringTypeNonCSAICollation (with trim collation support)

- Both source and trim strings must support collation-aware trimming operations

- Does not support case-sensitive accent-insensitive (CSAI) collations for trim operations

## Algorithm

- Evaluates the source string expression to get the input UTF8String

- If no trim string is specified, removes whitespace from both ends using default trimming

- If trim string is provided, removes specified characters from both ends using collation-aware trimming

- Delegates actual trimming logic to CollationSupport.StringTrim.exec() methods

- Preserves collation information throughout the trimming process

## Partitioning Behavior

- Preserves existing partitioning as it performs row-level transformations

- Does not require data shuffle since it operates independently on each row

- Can be pushed down in query optimization phases

## Edge Cases

- Null input: If source string is null, returns null

- Empty string: Returns empty string when input is empty

- Null trim string: Falls back to whitespace trimming behavior

- Empty trim string: No characters are trimmed, returns original string

- Collation handling: Respects collation rules when comparing characters for trimming

## Code Generation
This expression supports Spark's Tungsten code generation through the CollationSupport framework, enabling efficient compiled code execution for trim operations rather than falling back to interpreted mode.

## Examples
```sql
-- Basic whitespace trimming
SELECT TRIM('  hello world  ') AS result;
-- Returns: 'hello world'

-- Custom character trimming  
SELECT TRIM(BOTH 'x' FROM 'xxhello worldxx') AS result;
-- Returns: 'hello world'

-- Trimming from column
SELECT TRIM(name) FROM users;
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Basic whitespace trimming
df.select(trim(col("text_column")))

// Custom character trimming
df.select(trim(col("text_column"), "xyz"))

// Using in transformations
df.withColumn("cleaned_text", trim(col("raw_text")))
```

## See Also

- StringLTrim - trims characters from left end only

- StringRTrim - trims characters from right end only  

- String2TrimExpression - parent class for trim operations

- CollationSupport.StringTrim - underlying implementation for collation-aware trimming