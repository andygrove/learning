# Encode

## Overview
The Encode expression converts a string to binary data using a specified character encoding. It is a runtime-replaceable expression that delegates to a static method for actual encoding operations, supporting legacy charset and error handling configurations.

## Syntax
```sql
ENCODE(string_expr, charset_expr)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | String | The input string expression to be encoded |
| charset | String | The character set/encoding name to use for conversion |
| legacyCharsets | Boolean | Internal flag for legacy Java charset handling behavior |
| legacyErrorAction | Boolean | Internal flag for legacy coding error action behavior |

## Return Type
BinaryType - Returns binary data representing the encoded string.

## Supported Data Types

- Input string: StringTypeWithCollation (supports trim collation)
- Input charset: StringTypeWithCollation (supports trim collation)
- Both string inputs support collation-aware string types

## Algorithm

- Accepts a string expression and charset specification as input
- Validates input types through ImplicitCastInputTypes interface
- Delegates actual encoding to StaticInvoke calling Encode.encode static method
- Applies legacy configuration flags for charset handling and error actions
- Returns binary representation of the encoded string

## Partitioning Behavior
This expression preserves partitioning:

- Does not require data shuffling as it operates on individual rows
- Maintains existing partition boundaries since it's a deterministic row-level transformation
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- Null input string or charset results in null output
- Invalid charset names may throw runtime exceptions
- Legacy flags affect error handling behavior for malformed input
- Empty string input produces empty binary output
- Behavior varies based on SQLConf legacy settings for charset and error handling

## Code Generation
This expression uses runtime replacement pattern:

- Does not directly generate code itself
- Delegates to StaticInvoke which supports Tungsten code generation
- The underlying static method call can be code-generated for optimal performance
- Falls back to interpreted mode if code generation fails

## Examples
```sql
-- Encode string using UTF-8
SELECT ENCODE('hello world', 'UTF-8');

-- Encode with different charset
SELECT ENCODE('café', 'ISO-8859-1');
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("ENCODE(name, 'UTF-8')").as("encoded_name"))

// Using column expressions
df.select(encode(col("text_column"), lit("UTF-16")))
```

## See Also

- Decode - inverse operation to convert binary back to string
- Cast expressions for type conversions
- String manipulation functions in string_funcs group