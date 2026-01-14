# Murmur3Hash

## Overview
The `Murmur3Hash` expression computes a 32-bit hash value using the MurmurHash3 algorithm. It can hash multiple input values of various data types and accepts an optional seed parameter to produce different hash distributions for the same input data.

## Syntax
```sql
hash(expr1, expr2, ..., exprN)
hash(expr1, expr2, ..., exprN, seed)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.hash
hash(col("column1"), col("column2"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | One or more expressions to be hashed together |
| seed | Int | Optional seed value for hash function (default: 42) |

## Return Type
`IntegerType` - Returns a 32-bit signed integer hash value.

## Supported Data Types
All Spark SQL data types are supported as input, including:

- Primitive types (numeric, boolean, string)
- Complex types (arrays, maps, structs)
- Date and timestamp types
- Binary data

## Algorithm
The expression evaluates using the following process:

- Uses the MurmurHash3 x86_32 variant algorithm implementation
- Processes each input expression value sequentially with the specified seed
- Combines multiple input values into a single hash computation
- Returns the final 32-bit hash value as a signed integer
- Does not consider string collation differences in hash computation

## Partitioning Behavior
This expression is commonly used for partitioning operations:

- Preserves data distribution properties when used consistently
- Does not require shuffle when used for bucketing with same parameters
- Provides deterministic output for same inputs and seed values

## Edge Cases

- Null values are handled consistently in hash computation
- Empty arrays and maps produce deterministic hash values
- Different data types with same logical value may produce different hashes
- Uses legacy collation-unaware hashing for string types
- Hash collisions are possible due to 32-bit output range

## Code Generation
This expression supports Spark's Tungsten code generation framework for optimized execution in compiled code paths rather than interpreted evaluation.

## Examples
```sql
-- Hash a single string value
SELECT hash('Spark');
-- Result: 228562002

-- Hash multiple values with different types
SELECT hash('Spark', array(123), 2);
-- Result: -1321691492

-- Hash with custom seed
SELECT hash('Spark', 100);
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.hash

// Hash single column
df.select(hash($"name"))

// Hash multiple columns
df.select(hash($"name", $"id", $"category"))

// Use for bucketing
df.write
  .bucketBy(10, "id")
  .option("path", "/path/to/table")
  .saveAsTable("bucketed_table")
```

## See Also

- `xxhash64` - Alternative hash function with 64-bit output
- `md5` - Cryptographic hash function
- `sha1`, `sha2` - Secure hash algorithms
- Bucketing and partitioning operations