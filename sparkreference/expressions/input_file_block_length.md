# InputFileBlockLength

## Overview
The `InputFileBlockLength` expression returns the length of the HDFS block that contains the current input file being processed during query execution. This is a non-deterministic expression that provides information about the underlying storage block size, which can be useful for performance analysis and debugging.

## Syntax
```sql
INPUT_FILE_BLOCK_LENGTH()
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("input_file_block_length()"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | N/A | This function takes no arguments |

## Return Type
`LongType` - Returns a 64-bit signed integer representing the block length in bytes.

## Supported Data Types
This expression does not operate on input data types as it takes no arguments. It returns file system metadata regardless of the data being processed.

## Algorithm
- Retrieves the current block length from the `InputFileBlockHolder` singleton
- The `InputFileBlockHolder` maintains thread-local state about the current input file block
- Returns the block length as a Long value during query execution
- The value is determined by the underlying file system (typically HDFS) block configuration
- No computation is performed on the data itself

## Partitioning Behavior
- **Preserves partitioning**: Yes, this expression does not affect data partitioning
- **Requires shuffle**: No, this is a leaf expression that only reads metadata
- The expression returns different values per input block, but doesn't change data distribution

## Edge Cases
- **Null handling**: Never returns null (`nullable = false`)
- **Non-HDFS sources**: May return -1 or default values for non-block-based file systems
- **Empty files**: Returns the block size of the block containing the file, not the file size itself
- **Multiple blocks**: For files spanning multiple blocks, returns the length of the current block being processed
- **Nested queries**: The value corresponds to the input file of the outermost scan operation

## Code Generation
This expression **supports Tungsten code generation**. The `doGenCode` method generates efficient Java code that directly calls `InputFileBlockHolder.getLength()` without boxing/unboxing overhead or null checks.

## Examples
```sql
-- Get block length for each input file
SELECT input_file_block_length(), input_file_name(), count(*) 
FROM my_table 
GROUP BY input_file_block_length(), input_file_name();

-- Example output
SELECT INPUT_FILE_BLOCK_LENGTH();
-- Returns: 134217728 (128MB default HDFS block size)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.read.parquet("hdfs://path/to/data")
df.select(
  expr("input_file_block_length()").alias("block_length"),
  expr("input_file_name()").alias("file_name"),
  count("*").alias("record_count")
).groupBy("block_length", "file_name").show()

// Using with other file metadata functions
df.select(
  expr("input_file_block_length()"),
  expr("input_file_block_start()"),
  col("data_column")
).show()
```

## See Also
- `InputFileBlockStart` - Returns the starting offset of the current input file block
- `InputFileName` - Returns the name of the current input file being processed  
- `MonotonicallyIncreasingId` - Another non-deterministic expression for generating unique identifiers