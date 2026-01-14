# Md5

## Overview
The Md5 expression computes the MD5 hash digest of binary input data and returns it as a hexadecimal string. This is a cryptographic hash function that produces a 128-bit hash value, typically represented as a 32-character hexadecimal string.

## Syntax
```sql
SELECT md5(column_name) FROM table_name;
SELECT md5('input_string');
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | BinaryType | The binary data to compute the MD5 hash for |

## Return Type
UTF8String - A 32-character hexadecimal string representing the MD5 hash digest.

## Supported Data Types

- BinaryType (primary input type)
- String types (implicitly cast to binary)

## Algorithm

- Accepts binary input data through implicit type casting if necessary
- Uses Apache Commons DigestUtils.md5Hex() method to compute the MD5 hash
- Converts the resulting hexadecimal hash string to UTF8String format
- Supports both interpreted evaluation and code generation for performance
- Implements null-intolerant behavior (nulls propagate through the expression)

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffle as it operates on individual rows
- Can be computed locally on each partition
- Output partitioning scheme remains unchanged from input

## Edge Cases

- **Null handling**: Returns null if input is null (null-intolerant behavior)
- **Empty input**: Produces MD5 hash of empty byte array (d41d8cd98f00b204e9800998ecf8427e)
- **Binary data**: Handles arbitrary binary data including non-printable bytes
- **String inputs**: Automatically converts string inputs to binary using implicit casting

## Code Generation
This expression supports Tungsten code generation for optimized performance. It generates efficient Java code that directly calls DigestUtils.md5Hex() method, avoiding the overhead of interpreted evaluation in tight loops.

## Examples
```sql
-- Example SQL usage
SELECT md5('Spark');
-- Returns: 8cde774d6f7333752ed72cacddb05126

SELECT md5(CAST('Hello World' AS BINARY));
-- Returns: b10a8db164e0754105b7a99be72e3fe5

SELECT md5(NULL);
-- Returns: NULL
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions.md5

df.select(md5(col("binary_column")))
df.select(md5(lit("Spark")))
df.withColumn("hash", md5(col("data")))
```

## See Also

- Sha1 - SHA-1 hash function
- Sha2 - SHA-2 family hash functions (SHA-224, SHA-256, SHA-384, SHA-512)
- Crc32 - CRC32 checksum function
- Hash - General purpose hash function for data distribution