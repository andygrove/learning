# RandStr

## Overview
The `RandStr` expression generates a random string of a specified length using a seeded random number generator. It produces deterministic results within the same partition when given the same seed, making it suitable for reproducible random string generation in distributed computations.

## Syntax
```sql
randstr(length)
randstr(length, seed)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| length | IntegerType | The length of the random string to generate (must be non-negative) |
| seed | IntegerType or LongType | Optional seed value for the random number generator (defaults to UnresolvedSeed) |

## Return Type
UTF8String - Returns a randomly generated string of the specified length.

## Supported Data Types

- **length**: IntegerType only
- **seed**: IntegerType or LongType

## Algorithm

- Uses XORShiftRandom as the underlying random number generator for performance
- Initializes the RNG with seed + partitionIndex to ensure different random sequences per partition
- Generates random characters using ExpressionImplUtils.randStr() utility method
- Validates that the length parameter is non-negative at evaluation time
- Requires both length and seed parameters to be foldable (constant) expressions

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it doesn't require data movement between partitions
- Does not require shuffle operations
- Each partition uses a different effective seed (seed + partitionIndex) to avoid duplicate strings across partitions

## Edge Cases

- **Null handling**: Expression is marked as non-nullable and always returns a valid string
- **Negative length**: Throws QueryExecutionErrors.unexpectedValueForLengthInFunctionError at runtime
- **Zero length**: Returns an empty string
- **Non-foldable inputs**: Validation fails with DataTypeMismatch error for non-constant length or seed values
- **Seed behavior**: When hideSeed is true, the seed parameter is not shown in SQL output

## Code Generation
This expression supports Tungsten code generation. It generates optimized code that:

- Creates a mutable XORShiftRandom state variable per partition
- Initializes the RNG during partition setup phase
- Calls ExpressionImplUtils.randStr() directly in generated code for better performance

## Examples
```sql
-- Generate a random string of length 10
SELECT randstr(10) AS random_id;

-- Generate a random string with specific seed for reproducibility
SELECT randstr(5, 12345) AS seeded_random;

-- Use in table operations
SELECT user_id, randstr(8) AS session_token FROM users;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.withColumn("random_string", expr("randstr(10)"))
df.withColumn("seeded_string", expr("randstr(6, 98765)"))
```

## See Also

- `rand()` - Generate random double values
- `randn()` - Generate normally distributed random numbers
- `uuid()` - Generate UUID strings
- Random number generation functions in the string_funcs group