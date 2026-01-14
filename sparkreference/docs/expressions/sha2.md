# Sha2

## Overview
The Sha2 expression computes SHA-2 family hash values for binary input data. It supports SHA-224, SHA-256, SHA-384, and SHA-512 algorithms, returning the hash as a hexadecimal string representation.

## Syntax
```sql
sha2(expr, bitLength)
```

```scala
sha2(col("column_name"), lit(256))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | BinaryType | The binary data to be hashed |
| bitLength | IntegerType | The bit length of the SHA-2 algorithm (224, 256, 384, or 512) |

## Return Type
UTF8String - Returns the SHA-2 hash as a hexadecimal string.

## Supported Data Types

- **Input**: BinaryType for data, IntegerType for bit length specification
- **Output**: StringType (UTF8String)

## Algorithm

- Validates the bit length parameter against supported SHA-2 variants (224, 256, 384, 512)
- Uses Apache Commons DigestUtils for SHA-2 hash computation
- SHA-256 is used as default when bit length is 0
- Returns null for unsupported bit length values
- Converts the computed hash digest to hexadecimal string representation

## Partitioning Behavior

- **Preserves partitioning**: Yes, this is a deterministic function that operates on individual rows
- **Requires shuffle**: No, computation is performed locally on each partition

## Edge Cases

- **Null handling**: Returns null if either input expression is null (nullIntolerant = true)
- **Invalid bit length**: Returns null for unsupported bit lengths (not 224, 256, 384, or 512)
- **Default behavior**: Bit length 0 defaults to SHA-256
- **Empty input**: Processes empty binary arrays and returns corresponding hash of empty input

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, generating optimized Java code for runtime execution rather than falling back to interpreted mode.

## Examples
```sql
-- SHA-256 hash of binary data
SELECT sha2(cast('Apache Spark' as binary), 256);

-- SHA-512 hash with explicit bit length
SELECT sha2(binary_column, 512) FROM table_name;

-- Default SHA-256 (bit length 0)
SELECT sha2(cast('test' as binary), 0);
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(sha2(col("binary_data"), lit(256)))

// Using different SHA-2 variants
df.select(
  sha2(col("data"), lit(224)).alias("sha224"),
  sha2(col("data"), lit(384)).alias("sha384")
)
```

## See Also

- **Sha1**: SHA-1 hash function
- **Md5**: MD5 hash function  
- **Hash**: General hash function for multiple algorithms
- **Crc32**: CRC32 checksum function