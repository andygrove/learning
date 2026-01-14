# MonotonicallyIncreasingID

## Overview
`MonotonicallyIncreasingID` generates monotonically increasing 64-bit integers that are guaranteed to be unique and increasing, but not consecutive. This expression is stateful and non-deterministic, as it maintains an internal counter per partition and depends on partition IDs.

## Syntax
```sql
monotonically_increasing_id()
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.monotonically_increasing_id
df.withColumn("id", monotonically_increasing_id())
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | - | This function takes no arguments |

## Return Type
`LongType` - Returns 64-bit long integers.

## Supported Data Types
This expression does not accept input data types as it takes no parameters. It always generates `Long` values.

## Algorithm
- Combines partition ID (upper 31 bits) with record number (lower 33 bits) to create unique IDs
- Maintains an internal counter (`count`) that starts at 0 for each partition and increments for each row
- Creates a partition mask by left-shifting the partition index by 33 bits (`partitionIndex << 33`)
- Returns the sum of partition mask and current count value
- Assumes less than 1 billion partitions (2^31) and less than 8 billion records per partition (2^33)

## Partitioning Behavior
- **Preserves partitioning**: Yes, this expression does not require data movement between partitions
- **Requires shuffle**: No, computation is done locally within each partition
- **Partition dependency**: The generated IDs are dependent on partition IDs, making the expression non-deterministic across different partitioning schemes

## Edge Cases
- **Null handling**: This expression never returns null (`nullable = false`)
- **Empty partitions**: Will generate partition mask but no records to increment counter
- **Overflow behavior**: Could theoretically overflow if assumptions are violated (>1 billion partitions or >8 billion records per partition)
- **Serialization**: Counter resets to 0 when expression is serialized/deserialized due to `@transient` annotation
- **Non-consecutive IDs**: IDs from different partitions will have gaps based on partition ID differences

## Code Generation
This expression supports **Tungsten code generation**. The `doGenCode` method generates optimized Java code that:
- Creates mutable state for the counter (`count`)
- Creates immutable state for the partition mask
- Initializes both values during partition initialization
- Generates inline code for incrementing and returning values

## Examples
```sql
-- Generate monotonic IDs for a table
SELECT monotonically_increasing_id() as id, name, age 
FROM users;

-- Example output (partition 0):
-- 0, John, 25
-- 1, Jane, 30
-- 2, Bob, 35

-- Example output (partition 1):
-- 8589934592, Alice, 28  -- (1 << 33) + 0
-- 8589934593, Carol, 32  -- (1 << 33) + 1
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.monotonically_increasing_id

val df = spark.range(1000000)
val dfWithId = df.withColumn("monotonic_id", monotonically_increasing_id())
dfWithId.show()

// Using in window operations for row numbering alternative
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

val windowSpec = Window.orderBy(monotonically_increasing_id())
df.withColumn("row_number", row_number().over(windowSpec))
```

## See Also
- `row_number()` - For consecutive row numbering within partitions
- `rank()` and `dense_rank()` - For ranking operations
- `uuid()` - For generating unique identifiers (if available in your Spark version)