# UrlEncode

## Overview
The `UrlEncode` expression performs URL encoding (percent encoding) on a string input, converting special characters to their percent-encoded equivalents. This expression is implemented as a runtime replaceable expression that delegates to the `UrlCodec.encode` method for the actual encoding logic.

## Syntax
```sql
url_encode(str)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(url_encode(col("url_column")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | String | The input string to be URL encoded |

## Return Type
Returns a `String` containing the URL-encoded version of the input string.

## Supported Data Types

- String types with collation support (specifically `StringTypeWithCollation` with trim collation support)

## Algorithm

- Accepts a single string expression as input through the `child` parameter
- Delegates the actual encoding logic to `UrlCodec.encode` via `StaticInvoke`
- Uses runtime replacement pattern, meaning the expression is replaced with a `StaticInvoke` call during query planning
- Applies URL percent encoding rules to convert special characters to their `%XX` hexadecimal representation
- Preserves the string collation properties of the input

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffling as it operates on individual rows
- Maintains the same partitioning scheme as the input data
- Can be safely pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Follows standard Spark null propagation - null input returns null output
- **Empty string**: Empty strings are processed normally and return empty strings
- **Already encoded strings**: No special handling - characters like `%` will be encoded again (e.g., `%` becomes `%25`)
- **Unicode characters**: Unicode characters are properly encoded according to URL encoding standards

## Code Generation
This expression uses runtime replacement with `StaticInvoke`, which supports Tungsten code generation. The actual URL encoding is performed by calling the static `UrlCodec.encode` method, allowing for efficient code generation rather than falling back to interpreted mode.

## Examples
```sql
-- Basic URL encoding
SELECT url_encode('https://spark.apache.org') AS encoded_url;
-- Returns: https%3A%2F%2Fspark.apache.org

-- Encoding special characters
SELECT url_encode('hello world!@#$%') AS encoded_special;
-- Returns: hello+world%21%40%23%24%25

-- Handling null values
SELECT url_encode(NULL) AS encoded_null;
-- Returns: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = Seq(
  "https://spark.apache.org",
  "hello world!",
  null
).toDF("url")

df.select(url_encode(col("url")).alias("encoded_url")).show()

// Direct usage in transformations
df.withColumn("encoded_url", url_encode(col("url")))
```

## See Also

- `UrlDecode` - For decoding URL-encoded strings
- `Base64` - For Base64 encoding operations
- String manipulation functions in the `url_funcs` group