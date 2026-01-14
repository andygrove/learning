# Uuid

## Overview
The Uuid expression generates universally unique identifiers (UUIDs) using a pseudo-random number generator. This is a non-deterministic, stateful expression that produces different UUID values on each evaluation while maintaining reproducibility when a seed is provided.

## Syntax
```sql
UUID()
```

```scala
// DataFrame API
df.withColumn("id", expr("uuid()"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| seed (optional) | Long | Optional random seed for deterministic UUID generation across runs |

## Return Type
String (UTF8String internally) - Returns a standard UUID string format.

## Supported Data Types
This expression does not accept input data types as it's a leaf expression (generator function). The optional seed parameter accepts numeric types that can be converted to Long.

## Algorithm

- Uses an internal `RandomUUIDGenerator` initialized with a seed value
- The seed combines the provided seed (or random seed) with the partition index
- Each evaluation calls `getNextUUIDUTF8String()` to generate the next UUID in sequence
- The generator maintains state across evaluations within the same partition
- UUIDs are generated using pseudo-random algorithms for reproducibility when seeded

## Partitioning Behavior
How this expression affects partitioning:

- Preserves existing partitioning as it's a generator expression
- Does not require shuffle operations
- Each partition gets its own generator instance with a unique seed (base seed + partition index)
- Ensures different UUIDs across partitions even with the same base seed

## Edge Cases

- Null handling: Never returns null values (`nullable = false`)
- Unresolved state: Expression remains unresolved until a seed is provided (explicitly or implicitly)
- Partition consistency: Same partition with same seed will generate identical UUID sequences
- Cross-execution determinism: Requires explicit seed for reproducible results across different Spark jobs

## Code Generation
Supports full code generation (Tungsten). The generated code creates a mutable state variable for the `RandomUUIDGenerator` and initializes it during partition setup, avoiding object creation overhead during evaluation.

## Examples
```sql
-- Generate random UUIDs
SELECT uuid() as random_id FROM table;

-- Note: SQL doesn't support direct seed specification
-- Seeding typically done through configuration or DataFrame API
```

```scala
// Generate random UUIDs
df.withColumn("uuid", expr("uuid()"))

// For deterministic UUIDs (via internal constructor)
// This requires direct expression construction
val seededUuid = new Uuid(lit(12345L))
df.select(Column(seededUuid).alias("deterministic_uuid"))
```

## See Also

- `rand()` - Random number generation
- `randn()` - Normal distribution random numbers
- Other non-deterministic expressions for random value generation