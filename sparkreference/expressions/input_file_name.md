# InputFileName

## Overview
`InputFileName` is a Spark Catalyst expression that returns the name of the file currently being read during query execution. This is a nondeterministic leaf expression that provides metadata about the input file path without requiring any arguments.

## Syntax
```sql
input_file_name()
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(input_file_name())
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | - | This expression takes no arguments |

## Return Type
`StringType` (UTF8String) - Returns the full path of the input file being processed.

## Supported Data Types
This expression does not process input data types as it operates on file metadata. It can be used with any DataFrame regardless of the underlying data types.

## Algorithm
- Accesses the thread-local `InputFileBlockHolder` to retrieve current file information
- Returns the file path stored in the holder's context during file processing
- Returns empty string if file information is not available (e.g., when not reading from files)
- No initialization logic required per partition
- Evaluation is performed for each row but returns the same value within a file block

## Partitioning Behavior
- **Preserves partitioning**: Yes, this expression does not affect data distribution
- **Requires shuffle**: No, operates purely on local file metadata
- Can be used in partitioned operations without triggering data movement

## Edge Cases
- **Null handling**: Never returns null (nullable = false), returns empty string when unavailable
- **Non-file sources**: Returns empty string when reading from non-file sources (e.g., JDBC, streaming)
- **Multiple files per partition**: Will return different values as the partition processes different files
- **Generated/synthetic data**: Returns empty string for DataFrames created programmatically

## Code Generation
Supports full code generation (Tungsten). The generated code directly calls `InputFileBlockHolder.getInputFilePath()` without falling back to interpreted mode, ensuring optimal performance.

## Examples
```sql
-- Get file names along with data
SELECT input_file_name(), * FROM parquet_table;

-- Group by file name to see record counts per file
SELECT input_file_name() as file_name, count(*) as record_count 
FROM json_files 
GROUP BY input_file_name();
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.read.parquet("path/to/files")
df.select(input_file_name().alias("source_file"), col("*"))

// Filter data from specific files
df.filter(input_file_name().contains("2023"))
```

## See Also
- `InputFileBlockStart` - Returns the start offset of the current file block
- `InputFileBlockLength` - Returns the length of the current file block

---

# InputFileBlockStart

## Overview
`InputFileBlockStart` is a Spark Catalyst expression that returns the start offset (in bytes) of the current file block being read. This nondeterministic expression provides low-level file processing metadata useful for debugging and monitoring data ingestion.

## Syntax
```sql
input_file_block_start()
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(input_file_block_start())
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | - | This expression takes no arguments |

## Return Type
`LongType` - Returns the byte offset where the current file block starts, or -1 if not available.

## Supported Data Types
This expression does not process input data types as it operates on file block metadata. Compatible with any DataFrame schema.

## Algorithm
- Queries the thread-local `InputFileBlockHolder` for current block start position
- Returns the byte offset from the beginning of the file where the current block starts
- Returns -1 when block information is unavailable (non-file sources or unsupported formats)
- No per-partition initialization required
- Block information remains constant for all rows within the same file block

## Partitioning Behavior
- **Preserves partitioning**: Yes, operates on metadata without affecting data distribution
- **Requires shuffle**: No, accesses local thread-local storage only
- Safe to use in any partitioning context without performance impact

## Edge Cases
- **Null handling**: Never returns null (nullable = false), returns -1 when unavailable
- **Non-splittable formats**: May return 0 for entire file or -1 for unsupported formats
- **Compressed files**: Behavior depends on compression format and splittability
- **Small files**: May return 0 if the entire file constitutes a single block
- **Streaming sources**: Always returns -1 as block concepts don't apply

## Code Generation
Fully supports code generation with direct method call to `InputFileBlockHolder.getStartOffset()`. No interpreted fallback, ensuring minimal runtime overhead.

## Examples
```sql
-- Monitor file block processing
SELECT input_file_block_start() as block_start, 
       input_file_block_length() as block_length,
       count(*) as records_in_block
FROM large_parquet_files
GROUP BY input_file_block_start(), input_file_block_length();

-- Identify block boundaries
SELECT input_file_name(), input_file_block_start(), * 
FROM text_files 
ORDER BY input_file_name(), input_file_block_start();
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.read.option("multiline", "false").text("large_files/*")
df.select(
  input_file_name(),
  input_file_block_start().alias("block_start"),
  input_file_block_length().alias("block_length"),
  col("value")
)

// Debug block distribution
df.groupBy(input_file_block_start())
  .count()
  .orderBy("input_file_block_start()")
```

## See Also
- `InputFileName` - Returns the name of the current input file
- `InputFileBlockLength` - Returns the length of the current file block

---

# InputFileBlockLength

## Overview
`InputFileBlockLength` returns the length (in bytes) of the current file block being processed. This nondeterministic expression complements block start information to provide complete file block boundaries for monitoring and debugging data processing operations.

## Syntax
```sql
input_file_block_length()
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(input_file_block_length())
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | - | This expression takes no arguments |

## Return Type
`LongType` - Returns the byte length of the current file block, or -1 if not available.

## Supported Data Types
This expression operates on file block metadata independently of DataFrame content types. Works with any data schema.

## Algorithm
- Retrieves block length from thread-local `InputFileBlockHolder`
- Returns the size in bytes of the current file block being processed
- Returns -1 when block length information is unavailable
- Block length remains constant for all rows processed from the same file block
- No initialization overhead per partition

## Partitioning Behavior
- **Preserves partitioning**: Yes, metadata-only operation with no data redistribution
- **Requires shuffle**: No, uses local thread context information
- Can be combined with other expressions without affecting partition strategy

## Edge Cases
- **Null handling**: Never returns null (nullable = false), uses -1 for unavailable information
- **Variable block sizes**: Different blocks within the same file may have different lengths
- **End-of-file blocks**: Last block in a file may be shorter than standard block size
- **Non-block-based formats**: May return -1 for formats that don't use block concepts
- **Memory-based DataFrames**: Returns -1 for programmatically created DataFrames
- **Compressed files**: Reports compressed block size, not uncompressed data size

## Code Generation
Implements full code generation support with direct call to `InputFileBlockHolder.getLength()`. Generates efficient bytecode without interpreted evaluation overhead.

## Examples
```sql
-- Analyze block size distribution
SELECT input_file_block_length() as block_size,
       count(*) as num_blocks,
       sum(count(*)) OVER() as total_blocks
FROM parquet_dataset
GROUP BY input_file_block_length()
ORDER BY block_size;

-- Calculate processing efficiency
SELECT input_file_name(),
       input_file_block_length() / 1024 / 1024 as block_size_mb,
       count(*) as records_per_block
FROM large_dataset
GROUP BY input_file_name(), input_file_block_length();
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.read.parquet("hdfs://path/to/files")

// Monitor block processing
df.select(
  input_file_name(),
  input_file_block_start(),
  input_file_block_length().alias("block_length"),
  (input_file_block_length() / 1024 / 1024).alias("block_size_mb")
).distinct().show()

// Identify optimal block sizes
df.groupBy(input_file_block_length())
  .agg(
    count("*").alias("record_count"),
    countDistinct(input_file_name()).alias("file_count")
  )
  .orderBy(desc("record_count"))
```

## See Also
- `InputFileName` - Returns the name of the current input file
- `InputFileBlockStart` - Returns the start offset of the current file block