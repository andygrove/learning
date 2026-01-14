# CollationAwareMurmur3Hash

## Overview
CollationAwareMurmur3Hash is a Spark Catalyst expression that computes MurmurHash3 (32-bit x86 variant) hash values for input expressions while being aware of string collation rules. It extends the base MurmurHash3 functionality to handle collation-sensitive string comparisons and hashing, ensuring consistent hash values for strings that should be considered equivalent under specific collation rules.

## Syntax
```sql
-- Internal function, typically not called directly in SQL
hash(expr1, expr2, ..., exprN)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.catalyst.expressions.CollationAwareMurmur3Hash
CollationAwareMurmur3Hash(Seq(col1, col2), seed = 42)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | Sequence of expressions to compute hash values for |
| seed | Int | Initial seed value for the hash function (default varies by implementation) |

## Return Type
Returns a `LongType` value representing the computed hash.

## Supported Data Types

- Numeric types (IntegerType, LongType, FloatType, DoubleType, DecimalType)
- String types (StringType with collation awareness)
- Binary types (BinaryType)
- Date and timestamp types
- Boolean type
- Complex types (arrays, maps, structs - processed recursively)

## Algorithm

- Initializes MurmurHash3 algorithm with the provided seed value
- Iterates through each child expression in the sequence
- For each expression, converts the value to bytes using collation-aware rules for strings
- Calls the underlying `hashUnsafeBytes` method using Murmur3_x86_32 implementation
- Combines hash values from all children expressions using MurmurHash3 mixing functions
- Returns the final 64-bit hash value (though internally uses 32-bit algorithm)

## Partitioning Behavior
- Preserves partitioning when used as a partitioning expression
- Does not require shuffle operations when used for bucketing
- Enables hash-based partitioning strategies in Spark SQL optimization
- Consistent hash values across different nodes for the same input and collation rules

## Edge Cases

- Null values are handled by contributing a specific null hash value to the final result
- Empty strings are hashed differently from null values based on collation rules
- For collation-sensitive strings, equivalent strings under the collation produce identical hash values
- Seed value of 0 uses the algorithm's default initialization
- Empty children sequence returns the seed value as hash

## Code Generation
This expression supports Spark's Tungsten code generation framework, generating efficient Java bytecode for hash computation at runtime rather than falling back to interpreted evaluation mode.

## Examples
```sql
-- Used internally by Spark for operations like:
SELECT * FROM table1 WHERE hash(col1, col2) = hash('value1', 'value2');
```

```scala
// DataFrame API usage in custom expressions
import org.apache.spark.sql.functions._
import org.apache.spark.sql.catalyst.expressions.CollationAwareMurmur3Hash

val df = spark.range(10).select($"id", lit("text"))
val hashExpr = CollationAwareMurmur3Hash(Seq($"id".expr, $"value".expr), seed = 42)
```

## See Also

- MurmurHash3Hash - Base non-collation-aware version
- XxHash64 - Alternative hash function implementation
- HashPartitioning - Partitioning strategy using hash functions
- BucketSpec - Bucketing implementation using hash expressions