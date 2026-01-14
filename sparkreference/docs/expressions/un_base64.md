# UnBase64

## Overview
The UnBase64 expression decodes a Base64-encoded string into binary data. It supports both lenient decoding (default) and strict validation mode when used with functions like `try_to_binary`.

## Syntax
```sql
SELECT unbase64(base64_string);
-- Or via try_to_binary function
SELECT try_to_binary(base64_string, 'base64');
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(unbase64(col("base64_column")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression (String) | The Base64-encoded string to decode |
| failOnError | Boolean | Internal flag for strict validation (default: false) |

## Return Type
BinaryType - Returns decoded binary data as a byte array.

## Supported Data Types

- StringType with collation support
- Supports trim collation for string inputs

## Algorithm

- Accepts UTF8String input and converts to string representation
- Uses Java's Base64.getMimeDecoder() for MIME-compliant Base64 decoding
- In strict mode (failOnError=true), validates Base64 format before decoding
- Throws QueryExecutionError for invalid Base64 input when validation enabled
- Returns decoded byte array as BinaryType

## Partitioning Behavior

- Preserves partitioning as it's a unary expression operating row-by-row
- No shuffle required since it's a deterministic transformation
- Can be pushed down and executed locally on each partition

## Edge Cases

- **Null handling**: Null-intolerant - returns null for null input without evaluation
- **Invalid Base64**: In lenient mode, may produce unexpected results; in strict mode throws exception
- **Empty string**: Returns empty byte array for valid empty Base64 input
- **Whitespace**: MIME decoder handles whitespace and line breaks gracefully
- **Context independence**: Foldable behavior depends on child expression's foldability

## Code Generation
Supports Tungsten code generation with optimized null-safe code paths. Generates inline Java Base64 decoding calls and conditional validation logic when strict mode is enabled.

## Examples
```sql
-- Basic Base64 decoding
SELECT unbase64('U3BhcmsgU1FM');
-- Returns binary data representing "Spark SQL"

-- Using with try_to_binary (strict validation)
SELECT try_to_binary('SGVsbG8gV29ybGQ=', 'base64');
-- Returns binary data for "Hello World"

-- Null input handling
SELECT unbase64(NULL);
-- Returns NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic decoding
df.select(unbase64(col("encoded_data")))

// With column alias
df.select(unbase64(col("base64_col")).alias("decoded_binary"))
```

## See Also

- Base64 - For encoding binary data to Base64 strings
- ToBinary - Higher-level function that uses UnBase64 internally
- FromUTF8 - For converting binary data back to strings