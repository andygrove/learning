# Sha1

## Overview
The Sha1 expression computes the SHA-1 cryptographic hash of the input data and returns it as a hexadecimal string. This expression takes binary data as input and produces a 40-character hexadecimal representation of the SHA-1 hash digest.

## Syntax
```sql
SHA1(expr)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | BINARY | The binary data to compute the SHA-1 hash for |

## Return Type
STRING - A 40-character hexadecimal string representation of the SHA-1 hash

## Supported Data Types

- BINARY: Direct binary input
- STRING: Automatically cast to binary for hash computation

## Algorithm

- Accepts input data as a binary array
- Applies SHA-1 cryptographic hash function using Apache Commons DigestUtils
- Converts the resulting hash digest to hexadecimal string format
- Returns the hexadecimal representation as a UTF8String
- Supports Catalyst code generation for optimized execution

## Partitioning Behavior
This expression preserves partitioning since it operates on individual rows without requiring data movement:

- Does not require shuffle operations
- Maintains existing data partitioning
- Can be executed independently on each partition

## Edge Cases

- **Null handling**: Returns null when input is null (nullIntolerant = true)
- **Empty input**: Produces SHA-1 hash of empty byte array
- **Implicit casting**: Non-binary types are automatically cast to binary before hashing
- **Deterministic output**: Same input always produces identical hash result

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which generates optimized Java code that directly calls `DigestUtils.sha1Hex()` for improved performance.

## Examples
```sql
-- Example SQL usage
SELECT SHA1('Spark');
-- Returns: 85f5955f4b27a9a4c2aab6ffe5d7189fc298b92c

SELECT SHA1(CAST('Hello World' AS BINARY));
-- Returns SHA-1 hash of 'Hello World' as hex string
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions.sha1

df.select(sha1($"data_column"))
df.withColumn("hash", sha1($"binary_data"))
```

## See Also

- SHA2: For SHA-2 family hash functions (SHA-224, SHA-256, SHA-384, SHA-512)
- MD5: For MD5 hash computation
- Hash: For platform-dependent hash values
- CRC32: For CRC32 checksum computation