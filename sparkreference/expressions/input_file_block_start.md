# InputFileBlockStart

## Overview

The `InputFileBlockStart` expression returns the start offset in bytes of the current input file block being processed during query execution. This is a nondeterministic expression that provides metadata about the physical file layout during data processing, particularly useful for debugging and monitoring file access patterns.

## Syntax

```sql
input_file_block_start()
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("input_file_block_start()"))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| (none) | - | This expression takes no arguments |

## Return Type

`LongType` - Returns a 64-bit signed integer representing the byte offset.

## Supported Data Types

This expression does not operate on input data types as it takes no arguments. It returns file metadata regardless of the underlying data schema.

## Algorithm

- Accesses the thread-local `InputFileBlockHolder` to retrieve the current block's start offset
- Returns the start offset as a `Long` value without any transformations
- The offset represents the byte position where the current file block begins
- The value is determined by the underlying file system and Spark's block management
- No validation or bounds checking is performed on the returned value

## Partitioning Behavior

- **Preserves partitioning**: Yes, this expression does not affect data distribution
- **Requires shuffle**: No, operates locally on each partition
- The expression returns different values for different file blocks within the same partition
- Results may vary across task retries due to different block assignments

## Edge Cases

- **Null handling**: This expression is marked as non-nullable (`nullable = false`) and will never return null
- **Empty input**: Returns the block start offset even for empty blocks
- **File format dependency**: Behavior may vary depending on the underlying file format (Parquet, ORC, etc.)
- **Block unavailable**: Returns the value from `InputFileBlockHolder.getStartOffset()`, which may return -1 if no block context is available
- **Multiple files per partition**: Different blocks within the same task execution may return different offsets

## Code Generation

This expression supports Tungsten code generation. The generated code directly calls the static method `InputFileBlockHolder.getStartOffset()` without creating expression object instances, providing optimal performance during query execution.

## Examples

```sql
-- Get block start offsets for all records
SELECT input_file_block_start(), * FROM my_table;

-- Group by block start to see records per block
SELECT input_file_block_start() as block_start, count(*) 
FROM my_table 
GROUP BY input_file_block_start();

-- Example output showing block boundaries
-- -1 (when no block context available)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.read.parquet("path/to/files")

// Add block start information
df.select(
  col("*"),
  expr("input_file_block_start()").as("block_start")
).show()

// Analyze block distribution
df.select(expr("input_file_block_start()"))
  .groupBy("input_file_block_start()")
  .count()
  .show()
```

## See Also

- `input_file_block_length()` - Returns the length of the current input file block
- `input_file_name()` - Returns the name of the current input file
- `spark_partition_id()` - Returns the current partition ID