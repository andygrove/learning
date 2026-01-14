# UrlDecode

## Overview
The `UrlDecode` expression decodes URL-encoded strings by converting percent-encoded characters back to their original form. This expression is implemented as a runtime replaceable expression that delegates to the `UrlCodec.decode` method with configurable error handling behavior.

## Syntax
```sql
url_decode(url_string)
url_decode(url_string, fail_on_error)
```

```scala
// DataFrame API
col("url_column").expr("url_decode(url_column)")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | StringType | The URL-encoded string to decode |
| failOnError | Boolean | Whether to fail on malformed input (default: true) |

## Return Type
Returns `StringType` - the decoded URL string.

## Supported Data Types

- StringType with collation support (supports trim collation)
- Input must be a valid string expression

## Algorithm

- Delegates processing to `UrlCodec.decode` through `StaticInvoke`
- Uses runtime replacement pattern for code generation optimization  
- Applies percent-decoding to convert encoded characters (e.g., %20 → space)
- Error handling behavior controlled by `failOnError` parameter
- Supports collation-aware string processing with trim collation support

## Partitioning Behavior
This expression preserves partitioning:

- Does not require data shuffle as it operates on individual string values
- Can be applied per-partition independently
- Does not affect partition keys or distribution

## Edge Cases

- Null input returns null output (standard null propagation)
- Empty string input returns empty string
- Malformed percent-encoding behavior depends on `failOnError` flag
- When `failOnError` is true, invalid encoding throws exception
- When `failOnError` is false, invalid sequences may be left unchanged or handled gracefully
- Supports trim collation for string comparison operations

## Code Generation
This expression supports Tungsten code generation:

- Implemented as `RuntimeReplaceable` for efficient code generation
- Generates direct calls to `UrlCodec.decode` static method
- Avoids interpreted expression evaluation overhead
- Optimized through Catalyst's code generation framework

## Examples
```sql
-- Basic URL decoding
SELECT url_decode('Hello%20World') AS decoded;
-- Result: "Hello World"

-- Decode with error handling
SELECT url_decode('user%40domain.com', true) AS email;  
-- Result: "user@domain.com"

-- Decode complex URL parameters
SELECT url_decode('param%3Dvalue%26other%3D123') AS params;
-- Result: "param=value&other=123"
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("url_decode(encoded_url)").as("decoded"))

// With explicit error handling
df.select(expr("url_decode(encoded_url, false)").as("decoded"))
```

## See Also

- `UrlEncode` - Companion expression for URL encoding
- String manipulation functions in `url_funcs` group
- `StaticInvoke` expression for method delegation
- Collation-aware string expressions