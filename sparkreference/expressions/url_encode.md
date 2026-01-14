# Spark Catalyst URL Expressions

This reference documentation covers URL-related expressions in Apache Spark's Catalyst engine for encoding, decoding, and parsing URLs.

## UrlEncode

### Overview
The `UrlEncode` expression translates a string into 'application/x-www-form-urlencoded' format using UTF-8 encoding. It replaces special characters in URLs with percent-encoded equivalents to ensure safe transmission over HTTP.

### Syntax
```sql
url_encode(str)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("url_encode(column_name)"))
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | String | The string expression to be URL-encoded |

### Return Type
Returns a `String` containing the URL-encoded representation of the input.

### Supported Data Types
- String types with collation support (supports trim collation)
- Input is implicitly cast to string if needed

### Algorithm
- Uses Java's `URLEncoder.encode()` with UTF-8 charset
- Converts special characters to percent-encoded format (e.g., ':' becomes '%3A')
- Implemented as a `RuntimeReplaceable` expression using `StaticInvoke`
- Delegates to `UrlCodec.encode()` method for actual encoding
- Supports implicit casting of input types to string

### Partitioning Behavior
- Preserves partitioning as it's a deterministic transformation
- Does not require shuffle operations
- Can be pushed down in query optimization

### Edge Cases
- Null input returns null output
- Empty string returns empty string
- All UTF-8 characters are properly encoded
- No error conditions - encoding always succeeds

### Code Generation
Supports Tungsten code generation through `StaticInvoke`, providing optimized bytecode generation for better performance.

### Examples
```sql
-- Basic URL encoding
SELECT url_encode('https://spark.apache.org');
-- Result: https%3A%2F%2Fspark.apache.org

-- Encoding query parameters
SELECT url_encode('param=value&other=test');
-- Result: param%3Dvalue%26other%3Dtest
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("url_encode(url_column)"))
```

---

## UrlDecode

### Overview
The `UrlDecode` expression decodes a string in 'application/x-www-form-urlencoded' format using UTF-8 encoding. It converts percent-encoded characters back to their original form and can either throw errors or return null on invalid input.

### Syntax
```sql
url_decode(str)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("url_decode(column_name)"))
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | String | The URL-encoded string expression to decode |

### Return Type
Returns a `String` containing the decoded representation of the input.

### Supported Data Types
- String types with collation support (supports trim collation)
- Input is implicitly cast to string if needed

### Algorithm
- Uses Java's `URLDecoder.decode()` with UTF-8 charset
- Converts percent-encoded characters back to original form (e.g., '%3A' becomes ':')
- Implemented as a `RuntimeReplaceable` expression using `StaticInvoke`
- Delegates to `UrlCodec.decode()` method with `failOnError = true` by default
- Throws `QueryExecutionErrors.illegalUrlError` on malformed input when `failOnError` is true

### Partitioning Behavior
- Preserves partitioning as it's a deterministic transformation
- Does not require shuffle operations
- Can be pushed down in query optimization

### Edge Cases
- Null input returns null output
- Empty string returns empty string
- Malformed percent-encoding throws `IllegalArgumentException` wrapped in `QueryExecutionErrors.illegalUrlError`
- Invalid UTF-8 sequences cause errors when `failOnError` is true

### Code Generation
Supports Tungsten code generation through `StaticInvoke`, providing optimized bytecode generation for better performance.

### Examples
```sql
-- Basic URL decoding
SELECT url_decode('https%3A%2F%2Fspark.apache.org');
-- Result: https://spark.apache.org

-- Decoding query parameters
SELECT url_decode('param%3Dvalue%26other%3Dtest');
-- Result: param=value&other=test
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("url_decode(encoded_column)"))
```

---

## TryUrlDecode

### Overview
The `TryUrlDecode` expression is a safe version of `url_decode` that returns NULL instead of raising an error when decoding cannot be performed. It provides the same URL decoding functionality but with graceful error handling for malformed input.

### Syntax
```sql
try_url_decode(str)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("try_url_decode(column_name)"))
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | String | The URL-encoded string expression to decode |

### Return Type
Returns a `String` containing the decoded representation of the input, or `NULL` if decoding fails.

### Supported Data Types
- String types with collation support (supports trim collation)
- Input is implicitly cast to string if needed

### Algorithm
- Implemented as a `RuntimeReplaceable` expression wrapping `UrlDecode(expr, false)`
- Uses the same decoding logic as `UrlDecode` but with `failOnError = false`
- Returns null instead of throwing exceptions on malformed input
- Inherits analysis rules from the underlying `UrlDecode` expression
- Uses `InheritAnalysisRules` trait for consistent behavior

### Partitioning Behavior
- Preserves partitioning as it's a deterministic transformation
- Does not require shuffle operations
- Can be pushed down in query optimization

### Edge Cases
- Null input returns null output
- Empty string returns empty string
- Malformed percent-encoding returns null instead of throwing error
- Invalid UTF-8 sequences return null gracefully
- No exceptions are thrown regardless of input validity

### Code Generation
Inherits code generation capabilities from the underlying `UrlDecode` expression through `RuntimeReplaceable`.

### Examples
```sql
-- Successful decoding
SELECT try_url_decode('https%3A%2F%2Fspark.apache.org');
-- Result: https://spark.apache.org

-- Graceful handling of malformed input
SELECT try_url_decode('invalid%ZZ');
-- Result: NULL (instead of error)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("try_url_decode(potentially_malformed_column)"))
```

---

## ParseUrl

### Overview
The `ParseUrl` expression extracts specific parts from a URL string such as protocol, host, path, query parameters, or individual query values. It supports both general URL part extraction and specific query parameter retrieval with configurable error handling.

### Syntax
```sql
parse_url(url, partToExtract[, key])
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("parse_url(url_column, 'HOST')"))
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| url | String | The URL string to parse |
| partToExtract | String | The part of URL to extract (HOST, PATH, QUERY, etc.) |
| key | String (optional) | Specific query parameter key to extract from QUERY part |

### Return Type
Returns a `String` containing the extracted URL part, or `NULL` if the part doesn't exist or parsing fails.

### Supported Data Types
- All arguments must be string types with collation support (supports trim collation)
- Inputs are implicitly cast to string if needed
- Accepts 2 or 3 arguments only

### Algorithm
- Uses `ParseUrlEvaluator` for actual URL parsing and part extraction
- Caches URL object, extract part, and pattern when inputs are literals for performance
- Implemented as `RuntimeReplaceable` using `Invoke` on cached evaluator instance
- Validates argument count (2-3 arguments) during type checking
- Respects ANSI mode setting for error handling (`SQLConf.get.ansiEnabled`)

### Partitioning Behavior
- Preserves partitioning as it's a deterministic transformation
- Does not require shuffle operations
- Can be pushed down in query optimization
- Benefits from constant folding when inputs are literals

### Edge Cases
- Null URL input returns null output
- Invalid URL format throws error when `failOnError = true`, returns null when `failOnError = false`
- Non-existent query parameters return null
- Empty URL parts return empty string or null depending on the part
- Case-sensitive part extraction (HOST, PATH, QUERY, etc.)

### Code Generation
Supports code generation through `Invoke` expression, allowing optimized bytecode generation with cached evaluator objects.

### Examples
```sql
-- Extract host from URL
SELECT parse_url('http://spark.apache.org/path?query=1', 'HOST');
-- Result: spark.apache.org

-- Extract entire query string
SELECT parse_url('http://spark.apache.org/path?query=1', 'QUERY');
-- Result: query=1

-- Extract specific query parameter
SELECT parse_url('http://spark.apache.org/path?query=1', 'QUERY', 'query');
-- Result: 1

-- Extract path
SELECT parse_url('http://spark.apache.org/path?query=1', 'PATH');
-- Result: /path
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(
  expr("parse_url(url_column, 'HOST')").as("host"),
  expr("parse_url(url_column, 'QUERY', 'param_name')").as("param_value")
)
```

---

## TryParseUrl

### Overview
The `TryParseUrl` expression is a safe version of `parse_url` that returns NULL instead of raising an error when URL parsing cannot be performed. It provides the same URL parsing functionality but with graceful error handling for malformed URLs.

### Syntax
```sql
try_parse_url(url, partToExtract[, key])
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("try_parse_url(url_column, 'HOST')"))
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| url | String | The URL string to parse |
| partToExtract | String | The part of URL to extract (HOST, PATH, QUERY, etc.) |
| key | String (optional) | Specific query parameter key to extract from QUERY part |

### Return Type
Returns a `String` containing the extracted URL part, or `NULL` if parsing fails or the part doesn't exist.

### Supported Data Types
- All arguments must be string types with collation support (supports trim collation)
- Inputs are implicitly cast to string if needed
- Accepts 2 or 3 arguments only

### Algorithm
- Implemented as a `RuntimeReplaceable` expression wrapping `ParseUrl(children, false)`
- Uses the same parsing logic as `ParseUrl` but with `failOnError = false`
- Returns null instead of throwing exceptions on malformed URLs
- Inherits analysis rules from the underlying `ParseUrl` expression
- Uses `InheritAnalysisRules` trait for consistent behavior

### Partitioning Behavior
- Preserves partitioning as it's a deterministic transformation
- Does not require shuffle operations
- Can be pushed down in query optimization
- Benefits from constant folding when inputs are literals

### Edge Cases
- Null URL input returns null output
- Invalid URL format returns null instead of throwing error
- Non-existent query parameters return null
- Malformed URLs return null gracefully
- No exceptions are thrown regardless of URL validity

### Code Generation
Inherits code generation capabilities from the underlying `ParseUrl` expression through `RuntimeReplaceable`.

### Examples
```sql
-- Successful URL parsing
SELECT try_parse_url('http://spark.apache.org/path?query=1', 'HOST');
-- Result: spark.apache.org

-- Graceful handling of invalid URL
SELECT try_parse_url('inva lid://spark.apache.org/path?query=1', 'QUERY');
-- Result: NULL (instead of error)

-- Extract query parameter safely
SELECT try_parse_url('http://spark.apache.org/path?query=1', 'QUERY', 'query');
-- Result: 1
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("try_parse_url(potentially_invalid_url, 'HOST')"))
```

## See Also
- String functions for text manipulation
- HTTP-related expressions
- Cast expressions for type conversion
- Error handling expressions (`try_cast`, `try_*` variants)