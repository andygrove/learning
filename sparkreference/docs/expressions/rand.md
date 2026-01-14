# Rand

## Overview
The `Rand` expression generates pseudo-random double values uniformly distributed between 0.0 (inclusive) and 1.0 (exclusive). It uses the XORShift random number generator algorithm with configurable seeding for deterministic behavior when needed.

## Syntax
```sql
rand()
rand(seed)
```

```scala
// DataFrame API
rand()
rand(seed)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| seed | Long | Optional seed value for the random number generator. When provided, enables deterministic output |

## Return Type
`DoubleType` - Returns values between 0.0 (inclusive) and 1.0 (exclusive)

## Supported Data Types
The seed argument accepts:

- Long values (preferred)
- Integer values (implicitly converted)
- Numeric literals

## Algorithm
The expression evaluation follows these steps:

- Initializes an XORShiftRandom generator instance per partition
- Combines the provided seed with partition index to ensure different sequences per partition
- Generates pseudo-random double values using the XORShift algorithm
- Returns uniformly distributed values in the range [0.0, 1.0)
- Maintains internal state for sequential calls within the same partition

## Partitioning Behavior
How this expression affects partitioning:

- Preserves existing partitioning schemes
- Does not require shuffle operations
- Generates different random sequences per partition by adding partition index to seed
- Non-deterministic across different partition counts when using default unseeded constructor

## Edge Cases

- Null seed values are handled by the expression framework
- The function never returns null values (isNull is always false)
- Uses partition-aware seeding to ensure different sequences across partitions
- Hidden seed parameter controls SQL representation visibility
- Seed shifting is supported for creating correlated but distinct random sequences

## Code Generation
This expression supports full Tungsten code generation. It generates optimized Java code that:

- Creates XORShiftRandom instances as mutable state
- Initializes generators during partition setup
- Generates efficient nextDouble() calls without interpretation overhead

## Examples
```sql
-- Generate random values
SELECT rand() as random_value;

-- Generate deterministic random values with seed
SELECT rand(42) as seeded_random;

-- Use in WHERE clause for sampling
SELECT * FROM table WHERE rand() < 0.1;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.rand

df.select(rand())
df.select(rand(lit(42)))
df.filter(rand() < 0.1)
```

## See Also

- `randn()` - Normal distribution random numbers
- `monotonically_increasing_id()` - Unique ID generation
- `hash()` - Deterministic hash functions