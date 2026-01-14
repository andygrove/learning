# XxHash64

## Overview
The XxHash64 expression computes a 64-bit hash value using the XXH64 algorithm for one or more input values. It produces a deterministic hash that can be used for data distribution, partitioning, and integrity checks across Spark operations.

## Syntax
```sql
xxhash64(expr1[, expr2, ...][, seed])
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr1, expr2, ... | Any | One or more expressions of any supported data type to hash |
| seed | Long | Optional seed value for the hash function (defaults to 42L) |

## Return Type
`LongType` - Returns a 64-bit signed long integer representing the hash value.

## Supported Data Types
All Spark SQL data types are supported as input, including:

- Numeric types (IntegerType, LongType, DoubleType, etc.)
- String types (StringType)
- Binary types (BinaryType)
- Complex types (ArrayType, MapType, StructType)
- Date and timestamp types
- Boolean type

## Algorithm
The expression evaluates using the following process:

- Uses the XXH64 hashing algorithm implementation from the `XXH64` class
- Processes multiple input expressions by combining their hash values
- Applies the specified seed value (or default seed of 42L) to initialize the hash state
- Does not consider string collation rules in hash computation (`isCollationAware = false`)
- Delegates actual hash computation to `XxHash64Function.hash()` method

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning when used as a deterministic function
- Does not require shuffle operations when computing hashes within partitions
- Can be used effectively in partitioning schemes due to good hash distribution properties

## Edge Cases

- **Null handling**: Null values are handled consistently by the underlying hash function
- **Empty collections**: Empty arrays, maps, or structs produce deterministic hash values
- **Seed variation**: Different seed values produce completely different hash distributions
- **Cross-platform consistency**: Hash values are consistent across different platforms and Spark versions

## Code Generation
This expression supports Spark's Catalyst code generation (Tungsten) for optimized runtime performance, inheriting code generation capabilities from the `HashExpression` base class.

## Examples
```sql
-- Hash a single string value
SELECT xxhash64('Spark');

-- Hash multiple values with default seed
SELECT xxhash64('Spark', array(123), 2);

-- Hash with custom seed
SELECT xxhash64('data', 12345);

-- Use in partitioning context
SELECT xxhash64(user_id) % 10 as partition_key FROM users;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(xxhash64(col("name"), col("age")))

// With custom seed in raw expression
df.selectExpr("xxhash64(name, age, 12345)")

// Use for custom partitioning
df.repartition(expr("xxhash64(user_id) % 100"))
```

## See Also

- `hash()` - General hash function with different algorithm
- `md5()` - MD5 hashing function
- `sha1()`, `sha2()` - SHA family hash functions
- Partitioning functions for data distribution