# HiveHash

## Overview

The `HiveHash` expression computes a hash value of one or more input arguments using Hive's hashing algorithm. It returns a 32-bit integer hash code that combines the hash values of all input expressions using a polynomial rolling hash with multiplier 31.

## Syntax

```sql
hive_hash(expr1, expr2, ...)
```

```scala
// DataFrame API
col("column").expr("hive_hash(col1, col2)")
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| expr1, expr2, ... | Any | One or more expressions of any supported data type to hash |

## Return Type

`IntegerType` - Returns a 32-bit signed integer hash value.

## Supported Data Types

The expression supports all Spark SQL data types:

- Primitive types: Integer, Long, Float, Double, Boolean, Byte, Short
- String types (with collation awareness)
- Binary data
- Decimal types
- Timestamp and Date types
- Calendar intervals
- Complex types: Arrays, Maps, Structs

## Algorithm

- Initializes hash value to seed 0
- For each input expression, computes its individual hash using `HiveHashFunction.hash()`
- Combines hashes using polynomial rolling hash: `hash = (31 * hash) + childHash`
- Uses collation-aware hashing for string types when applicable
- Handles nested complex types recursively (arrays use 31x multiplier, maps use XOR for key-value pairs)

## Partitioning Behavior

- Preserves partitioning when used as a partitioning expression
- Does not require shuffle when applied to already partitioned data
- Commonly used for bucketing and data distribution in Hive-compatible scenarios

## Edge Cases

- Null inputs contribute 0 to the final hash (nulls are handled safely)
- Empty arrays and maps contribute their base hash without elements
- The expression itself never returns null (always produces an integer result)
- String collation affects hash computation for non-binary-equal collations
- Decimal values are normalized before hashing to ensure consistent results

## Code Generation

This expression fully supports Tungsten code generation:

- Generates optimized Java code for hash computation
- Splits complex expressions across multiple methods to avoid JVM method size limits
- Uses unsafe memory operations for efficient byte array hashing
- Falls back to interpreted mode only in exceptional cases

## Examples

```sql
-- Hash a single column
SELECT hive_hash(user_id) FROM users;

-- Hash multiple columns for bucketing
SELECT hive_hash(customer_id, order_date) FROM orders;

-- Hash complex data types
SELECT hive_hash(array_col, map_col, struct_col) FROM complex_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("hive_hash(col1, col2)").alias("hash_value"))

// For bucketing
df.write
  .bucketBy(10, "hive_hash(customer_id)")
  .saveAsTable("bucketed_table")
```

## See Also

- `hash()` - Spark's default hash function (MurmurHash3)
- `xxhash64()` - 64-bit xxHash algorithm
- `md5()` - MD5 cryptographic hash
- `sha1()`, `sha2()` - SHA cryptographic hash functions