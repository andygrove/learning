# ParseUrl

## Overview
The `ParseUrl` expression extracts specific components from URLs, such as protocol, host, path, query parameters, and fragments. It parses a URL string and returns the requested part as a string, with optional support for extracting specific query parameter values by name.

## Syntax
```sql
parse_url(url, partToExtract [, key])
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `url` | String | The URL string to parse |
| `partToExtract` | String | The part of the URL to extract (e.g., 'HOST', 'PATH', 'QUERY', 'PROTOCOL', 'FILE', 'AUTHORITY', 'USERINFO', 'REF') |
| `key` | String (optional) | When extracting 'QUERY', the specific query parameter name to retrieve |

## Return Type
Returns `StringType` - the extracted URL component as a string.

## Supported Data Types
Accepts string inputs with collation support:

- All arguments must be string types
- Supports string types with collation (trim collation supported)
- Input strings are converted from UTF8String internally

## Algorithm
The expression is implemented as a runtime replaceable expression with the following evaluation strategy:

- Caches constant URL, part extraction type, and key pattern as lazy vals for performance optimization
- Delegates actual URL parsing to a `ParseUrlEvaluator` object
- Uses `Invoke` expression to call the evaluator's `evaluate` method at runtime
- Validates that 2-3 arguments are provided during compilation
- Respects ANSI mode settings for error handling behavior

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffling as it operates row-by-row
- Maintains existing partitioning scheme since it's a deterministic transformation
- Can be pushed down in query optimization when inputs are deterministic

## Edge Cases

- Returns null for malformed URLs when `failOnError` is false (non-ANSI mode)
- Throws exceptions for malformed URLs when `failOnError` is true (ANSI mode)
- Returns null when the requested URL part doesn't exist
- Query parameter extraction returns null if the specified key is not found
- Null input URLs result in null output
- Empty string URLs are treated as malformed

## Code Generation
This expression uses runtime replacement rather than direct code generation:

- Implements `RuntimeReplaceable` interface
- Replaced with an `Invoke` expression that calls `ParseUrlEvaluator.evaluate`
- The replacement uses Tungsten's object invocation mechanism
- Caches constant values (URL, part, pattern) for repeated evaluation efficiency

## Examples
```sql
-- Extract host from URL
SELECT parse_url('http://spark.apache.org/path?query=1', 'HOST');
-- Returns: spark.apache.org

-- Extract specific query parameter
SELECT parse_url('http://spark.apache.org/path?query=1', 'QUERY', 'query');
-- Returns: 1

-- Extract path component
SELECT parse_url('https://example.com/docs/guide.html', 'PATH');
-- Returns: /docs/guide.html
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("parse_url(url_column, 'HOST')").as("host"))

// Extract query parameters
df.select(expr("parse_url(url_column, 'QUERY', 'param_name')").as("param_value"))
```

## See Also

- `regexp_extract` - For custom URL pattern extraction
- `split` - For simple string splitting operations
- Other URL manipulation functions in the `url_funcs` group