# Crc32

## Overview
The `Crc32` expression computes the CRC-32 (Cyclic Redundancy Check) checksum of binary data. It takes binary input and returns a 64-bit long value representing the CRC-32 checksum, which is commonly used for data integrity verification and error detection.

## Syntax
```sql
crc32(expr)
```

```scala
crc32(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Binary | The binary data for which to compute the CRC-32 checksum |

## Return Type
`LongType` - Returns a 64-bit long integer representing the CRC-32 checksum value.

## Supported Data Types

- `BinaryType` - Input is implicitly cast to binary type if not already binary

## Algorithm

- Uses Java's `java.util.zip.CRC32` class to compute the checksum
- Creates a new CRC32 instance for each evaluation
- Updates the checksum with the entire byte array using the `update(bytes, offset, length)` method
- Returns the final checksum value as a long integer
- Implements null-safe evaluation with null intolerance

## Partitioning Behavior
- Preserves partitioning as it's a deterministic row-level transformation
- Does not require shuffle operations
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null if input is null (null intolerant behavior)
- **Empty input**: Accepts empty byte arrays and computes CRC-32 for zero-length data
- **Binary conversion**: Non-binary inputs are implicitly cast to binary type before processing
- **Deterministic output**: Same input always produces the same CRC-32 value

## Code Generation
Supports Tungsten code generation for optimized performance. The generated code creates a `java.util.zip.CRC32` instance inline and performs the checksum calculation without object allocation overhead in the hot path.

## Examples
```sql
-- Compute CRC-32 of a string literal
SELECT crc32('Spark');
-- Result: 1557323817

-- Compute CRC-32 of a binary column
SELECT crc32(binary_column) FROM table_name;

-- Compute CRC-32 of string data (implicitly cast to binary)
SELECT crc32(CAST('Hello World' AS BINARY));
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.crc32

df.select(crc32(col("data_column")))

// With string data (implicit cast to binary)
df.select(crc32(col("string_column").cast("binary")))

// Computing CRC-32 for data integrity checking
df.withColumn("checksum", crc32(col("payload")))
```

## See Also

- `hash()` - General hash function for multiple columns
- `md5()` - MD5 hash function
- `sha1()`, `sha2()` - SHA hash functions
- `murmur3hash()` - MurmurHash function