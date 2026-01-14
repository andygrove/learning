# IsValidUTF8

## Overview
The `IsValidUTF8` expression checks whether a binary or string input contains valid UTF-8 encoded data. It returns true if the input is valid UTF-8, false if it contains invalid UTF-8 sequences, and null if the input is null.

## Syntax
```sql
IS_VALID_UTF8(input)
```

```scala
// DataFrame API
col("column_name").expr("is_valid_utf8(column_name)")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| input | StringType with collation support | The binary or string data to validate for UTF-8 encoding |

## Return Type
`BooleanType` - Returns true for valid UTF-8, false for invalid UTF-8, null for null input.

## Supported Data Types

- StringType with collation support (including trim collation)
- Binary data that can be cast to string
- Supports implicit type casting for compatible input types

## Algorithm

- The expression is implemented as a `RuntimeReplaceable` that delegates to the `isValid` method on the input
- Uses the `Invoke` expression to call the native `isValid` method with `BooleanType` return
- Performs UTF-8 validation at the byte level to detect malformed sequences
- Returns false immediately upon encountering any invalid UTF-8 byte sequence
- Handles multi-byte UTF-8 characters by validating continuation bytes

## Partitioning Behavior
How this expression affects partitioning:

- Preserves existing partitioning as it's a deterministic row-level transformation
- Does not require shuffle operations
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null for null input (nullable = true, nullIntolerant = true)
- **Empty input**: Returns true for empty strings as they are valid UTF-8
- **Binary data**: Validates the raw byte sequence for UTF-8 compliance
- **Collation support**: Works with different string collations including trim collation
- **Malformed sequences**: Returns false for incomplete multi-byte sequences or invalid continuation bytes

## Code Generation
This expression uses runtime replacement with method invocation rather than direct code generation. It delegates to the underlying `isValid` method implementation, which may have optimized native implementations depending on the execution engine.

## Examples
```sql
-- Basic UTF-8 validation
SELECT IS_VALID_UTF8('Hello World');
-- true

-- Invalid UTF-8 sequence (from documentation example)
SELECT IS_VALID_UTF8(x'61C262');
-- false

-- Null input
SELECT IS_VALID_UTF8(NULL);
-- NULL

-- Valid multi-byte UTF-8
SELECT IS_VALID_UTF8('café');
-- true
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("text_column").expr("is_valid_utf8(text_column)").as("is_valid"))

// With binary data
df.select(expr("is_valid_utf8(binary_column)").as("utf8_valid"))
```

## See Also

- `TRY_TO_BINARY` - For safe binary conversion
- `DECODE` - For character set conversion
- String manipulation functions for UTF-8 text processing