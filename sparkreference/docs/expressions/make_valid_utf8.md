# MakeValidUTF8

## Overview
The `MakeValidUTF8` expression converts invalid UTF-8 byte sequences in a string to valid UTF-8 by replacing malformed sequences. This expression ensures that string data conforms to proper UTF-8 encoding standards, making it safe for processing in systems that require valid UTF-8.

## Syntax
```sql
make_valid_utf8(str)
```

```scala
// DataFrame API
col("column_name").makeValidUTF8()
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| input | String with collation support | The input string expression that may contain invalid UTF-8 sequences |

## Return Type
Returns a string with the same collation as the input, containing only valid UTF-8 sequences.

## Supported Data Types

- String types with collation support
- Supports trim collation semantics
- Input must be compatible with `StringTypeWithCollation(supportsTrimCollation = true)`

## Algorithm

- Invokes the `makeValid` method on the input string expression
- Scans the input byte sequence for invalid UTF-8 patterns
- Replaces malformed UTF-8 byte sequences with valid replacement characters
- Preserves all valid UTF-8 sequences in their original form
- Maintains the original string's collation properties

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle as it operates row-by-row
- Maintains existing partition boundaries
- Can be pushed down to individual partitions for parallel processing

## Edge Cases

- **Null handling**: Returns null when input is null (nullIntolerant = true, but nullable = true)
- **Empty string**: Returns empty string unchanged as it's already valid UTF-8
- **Already valid UTF-8**: Returns the input string unchanged
- **Mixed valid/invalid sequences**: Only replaces the invalid portions while preserving valid UTF-8 characters
- **Collation preservation**: Maintains the input string's collation settings in the output

## Code Generation
This expression uses runtime replacement with method invocation rather than direct code generation. It falls back to interpreted mode by invoking the `makeValid` method on the string object at runtime.

## Examples
```sql
-- Fix malformed UTF-8 in user input data
SELECT make_valid_utf8(user_comment) as cleaned_comment 
FROM user_feedback;

-- Clean UTF-8 before string operations
SELECT make_valid_utf8(raw_text) as valid_text
FROM imported_data 
WHERE raw_text IS NOT NULL;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Clean a column with potentially invalid UTF-8
df.select(col("raw_text").makeValidUTF8().alias("cleaned_text"))

// Use in data cleaning pipeline
val cleanedDF = df.withColumn("valid_description", 
  col("description").makeValidUTF8())
```

## See Also

- String manipulation functions
- UTF-8 validation expressions  
- Text cleaning and normalization functions
- Collation-aware string operations