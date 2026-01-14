# InputFileName

## Overview
The `InputFileName` expression returns the name of the file currently being processed during query execution. This is a non-deterministic expression that provides access to the input file path through the `InputFileBlockHolder` mechanism, allowing users to identify which file contributed specific rows in their query results.

## Syntax
```sql
INPUT_FILE_NAME()
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
`StringType` - Returns a UTF-8 encoded string containing the input file path.

## Supported Data Types
This expression does not operate on input data types as it takes no arguments. It generates string output regardless of the underlying data being processed.

## Algorithm
- Expression extends `LeafExpression` with no child expressions to evaluate
- During execution, calls `InputFileBlockHolder.getInputFilePath` to retrieve the current file path
- Returns the file path as a `UTF8String` without any transformation
- Initialization per partition is a no-op (`initializeInternal` does nothing)
- File path context is maintained externally by Spark's execution engine

## Partitioning Behavior
- **Preserves partitioning**: This expression does not affect data partitioning as it only adds metadata
- **No shuffle required**: The expression is evaluated locally on each partition without requiring data movement
- Each partition will return file paths for the files it processes locally

## Edge Cases
- **Null handling**: Expression is marked as non-nullable (`nullable = false`), so it will never return null values
- **Missing file context**: If called outside of file-based data source context, behavior depends on `InputFileBlockHolder` state
- **Multiple files per partition**: When a partition processes multiple files, the returned file name corresponds to the file being processed for each specific row
- **Non-file data sources**: May return empty or undefined results when used with data sources that don't have file-based origins

## Code Generation
This expression supports Tungsten code generation. The generated code directly calls `InputFileBlockHolder.getInputFilePath()` and sets `isNull = false`, avoiding the overhead of interpreted evaluation in tight loops.

## Examples
```sql
-- Get file names along with data
SELECT input_file_name() as source_file, * 
FROM parquet.`/path/to/files/*.parquet`;

-- Group by source file to analyze data distribution
SELECT input_file_name() as file, count(*) as row_count
FROM delta.`/path/to/table`
GROUP BY input_file_name();
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.read.parquet("/path/to/files/*.parquet")
df.select(input_file_name().alias("source_file"), col("*")).show()

// Analyze data distribution across files
df.groupBy(input_file_name().alias("file"))
  .count()
  .show()
```

## See Also
- `InputFileBlockSize` - Returns the size of the current input file block
- `MonotonicallyIncreasingId` - Another non-deterministic expression for generating unique identifiers
- File-based data sources (Parquet, JSON, CSV) that populate the input file context