# Randn

## Overview
The `Randn` expression generates normally distributed random numbers (Gaussian distribution) with mean 0.0 and standard deviation 1.0. This is a non-deterministic expression that produces different values on each evaluation unless a specific seed is provided.

## Syntax
```sql
randn()           -- Uses random seed
randn(seed)       -- Uses specified seed for reproducibility
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| seed | Long | Optional. Seed value for random number generation. When provided, ensures reproducible results |

## Return Type
`DoubleType` - Returns a double-precision floating point number.

## Supported Data Types

- Seed argument accepts `LongType` expressions
- No input data transformation - generates values independently

## Algorithm

- Uses XORShiftRandom as the underlying random number generator
- Calls `nextGaussian()` method to generate normally distributed values
- Each partition gets its own RNG instance initialized with `seed + partitionIndex`
- Maintains deterministic behavior within partitions when seed is specified
- Extends `NondeterministicUnaryRDG` for proper non-deterministic handling

## Partitioning Behavior
How this expression affects partitioning:

- Preserves existing partitioning since it doesn't depend on input data
- Does not require shuffle operations
- Each partition maintains independent random state for consistent results

## Edge Cases

- Null handling: Never returns null values (`isNull = FalseLiteral`)
- Empty input: Generates values regardless of input data presence  
- Range: Can generate any finite double value following normal distribution
- Determinism: Non-deterministic by default, deterministic when seed provided
- Partition consistency: Same seed produces same sequence within each partition

## Code Generation
Supports full code generation (Tungsten). The generated code creates a partition-local XORShiftRandom instance and directly calls `nextGaussian()` method, avoiding interpreted evaluation overhead.

## Examples
```sql
-- Generate random normally distributed values
SELECT randn() as random_normal;

-- Generate reproducible random values with seed
SELECT randn(42) as seeded_random;

-- Use in data generation scenarios
SELECT id, randn(123) as noise 
FROM range(1000);
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._

// Generate random normal values
df.select(randn().alias("random_normal"))

// With specific seed for reproducibility
df.select(randn(lit(42L)).alias("seeded_random"))

// Add noise to existing column
df.withColumn("noisy_value", col("value") + randn(seed = 123))
```

## See Also

- `Rand` - Generates uniformly distributed random numbers [0.0, 1.0)
- `NondeterministicUnaryRDG` - Base class for non-deterministic random expressions
- `UnresolvedSeed` - Default seed resolution mechanism