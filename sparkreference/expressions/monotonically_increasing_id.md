# MonotonicallyIncreasingID

## Overview
The `MonotonicallyIncreasingID` expression generates a unique, monotonically increasing 64-bit integer for each row within a Spark job. It combines a partition identifier with a per-partition row counter to ensure global uniqueness across all partitions while maintaining monotonic ordering within each partition.

## Syntax
```sql
SELECT monotonically_increasing_id();
```

```scala
import org.apache.spark.sql.functions._
df.withColumn("id", monotonically_increasing_id())
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | - | This function takes no arguments |

## Return Type
`LongType` - Returns a 64-bit long integer value that is never null.

## Supported Data Types
This expression does not accept input data types as it takes no arguments. It generates long integer values regardless of the input DataFrame schema.

## Algorithm
- **Partition Masking**: Uses the upper 31 bits (bit positions 33-63) to encode the partition index by left-shifting the partition index by 33 positions
- **Row Counting**: Uses the lower 33 bits (bit positions 0-32) to store a per-partition row counter that starts at 0
- **ID Generation**: Combines the partition mask with the current count using bitwise addition
- **State Management**: Maintains transient state (`count` and `partitionMask`) that resets during serialization/deserialization
- **Monotonic Guarantee**: Increments the counter after each row evaluation to ensure strict monotonic increasing behavior within partitions

## Partitioning Behavior
- **Preserves Partitioning**: Does not require data shuffling as it operates independently within each partition
- **Partition-Aware**: Encodes partition information directly into the generated ID to ensure global uniqueness
- **No Shuffle Required**: Can be evaluated in parallel across partitions without coordination

## Edge Cases
- **Null Handling**: Never returns null values (`nullable = false`)
- **Empty Partitions**: Empty partitions will not generate any IDs but do not affect the numbering scheme
- **Overflow Behavior**: Can theoretically overflow after 2^33 (8.6 billion) rows per partition, wrapping the counter portion
- **Serialization Reset**: Counter resets to 0 when the expression is serialized/deserialized due to `@transient` annotation
- **Maximum Partitions**: Supports up to 2^31 partitions before partition mask overflow

## Code Generation
This expression fully supports Tungsten code generation. It generates optimized Java code that:
- Creates mutable state for the row counter (`count`)
- Creates immutable state for the partition mask (`partitionMask`)
- Initializes both values during partition setup
- Performs efficient bitwise operations without method calls

## Examples
```sql
-- Generate unique IDs for all rows
SELECT monotonically_increasing_id() as row_id, name, age 
FROM users;

-- Result example:
-- row_id: 0, 1, 2, ... (partition 0)
-- row_id: 8589934592, 8589934593, ... (partition 1, if exists)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.range(1000).toDF("value")
val withIds = df.withColumn("unique_id", monotonically_increasing_id())

// Using in window operations for row numbering
val numbered = df.withColumn("id", monotonically_increasing_id())
  .orderBy("id")
```

## See Also
- `row_number()` - Window function for sequential numbering within partitions
- `rank()` - Window function for ranking with gaps
- `uuid()` - For generating random unique identifiers