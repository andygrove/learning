# StringDecode

## Overview
The StringDecode expression is a Catalyst expression that decodes string data using a specified character set or encoding scheme. This expression is typically used to convert byte arrays or encoded strings back into their original string representation using the specified decoding method.

## Syntax
```sql
STRING_DECODE(input, charset)
```

```scala
StringDecode(input, charset)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| input | Expression | The input data to be decoded (typically binary or encoded string data) |
| charset | Expression | The character set or encoding scheme to use for decoding |

## Return Type
Returns a `StringType` representing the decoded string value.

## Supported Data Types

- Input: `BinaryType`, `StringType`

- Charset: `StringType` (must be a valid character encoding name)

## Algorithm

- Validates that the charset parameter represents a supported character encoding

- Extracts the input data as bytes if it's in binary format

- Applies the specified character set decoding to convert bytes to string

- Returns the decoded string result

- Handles encoding errors according to the JVM's default replacement strategy

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle as it operates on individual rows

- Maintains the same partitioning scheme as the input dataset

- Can be safely pushed down to individual partitions for parallel execution

## Edge Cases

- Returns null if either input or charset arguments are null

- Throws an exception if the charset name is invalid or unsupported

- Handles malformed byte sequences according to the charset's default replacement behavior

- Empty input results in an empty string output

- Invalid byte sequences may be replaced with the charset's default replacement character

## Code Generation
This expression supports Tungsten code generation for improved performance in whole-stage code generation scenarios, falling back to interpreted evaluation when code generation is not available or feasible.

## Examples
```sql
-- Decode UTF-8 encoded binary data
SELECT STRING_DECODE(encoded_data, 'UTF-8') FROM table_name;

-- Decode base64 encoded string with specific charset
SELECT STRING_DECODE(base64_column, 'ISO-8859-1') FROM encoded_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("STRING_DECODE(binary_column, 'UTF-8')"))

// Using StringDecode expression directly
val decodeExpr = StringDecode(col("input_data").expr, lit("UTF-8").expr)
df.select(Column(decodeExpr))
```

## See Also

- StringEncode - for encoding strings to binary format

- Base64 - for base64 encoding/decoding operations

- Decode - for general decoding operations

- Cast - for general type conversions