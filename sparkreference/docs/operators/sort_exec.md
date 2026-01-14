# SortExec

## Overview

SortExec performs external sorting of input rows based on specified sort orders. It can perform either local sorting within each partition or global sorting across all partitions by shuffling data first if necessary.

## When Used

The query planner chooses SortExec when:
- An ORDER BY clause requires sorting
- A global sort is needed across all partitions (`global = true`)
- Local sorting is required within partitions to satisfy downstream operators
- Sort-merge joins require pre-sorted inputs

## Input Requirements

- **Expected input partitioning**: Any partitioning (inherits child's partitioning)
- **Expected input ordering**: No specific ordering required
- **Number of children**: Unary operator (exactly one child)

## Output Properties

- **Output partitioning**: Preserves the child operator's output partitioning
- **Output ordering**: Produces the specified `sortOrder` sequence
- **Output schema**: Identical to child's output schema (`child.output`)

## Algorithm

• Creates an `UnsafeExternalRowSorter` instance per task using a ThreadLocal variable
• Generates prefix comparators and computers for efficient sorting based on the first sort expression
• Determines if radix sort can be used (when `enableRadixSort` is true, single sort column, and prefix-sortable)
• Iterates through input rows, inserting each into the sorter
• Performs the actual sort operation, which may spill to disk if memory is insufficient
• Returns a sorted iterator over the rows
• Tracks and reports sorting metrics (time, memory usage, spill size)

## Memory Usage

- **Spills to disk**: Yes, uses `UnsafeExternalRowSorter` for external sorting
- **Memory requirements**: Configurable page size from `SparkEnv.get.memoryManager.pageSizeBytes`
- **Buffering behavior**: Accumulates all input rows in memory before sorting, spilling when necessary

## Partitioning Behavior

- **Data distribution**: Local sort preserves partitioning; global sort requires `OrderedDistribution`
- **Shuffle requirements**: Global sort (`global = true`) requires shuffle to achieve ordered distribution
- **Partition count changes**: No change in partition count

## Supported Join/Aggregation Types

Not applicable - SortExec is a sorting operator, not a join or aggregation operator.

## Metrics

- **sortTime**: Time spent sorting data (in milliseconds)
- **peakMemory**: Peak memory usage during sorting operation
- **spillSize**: Amount of data spilled to disk during sorting

## Code Generation

Yes, SortExec supports whole-stage code generation by extending `BlockingOperatorWithCodegen`. It generates code to:
- Create and initialize the sorter
- Insert input rows into the sorter via `doConsume`
- Iterate through sorted results via `doProduce`

## Configuration Options

- **spark.sql.sort.enableRadixSort**: Enables radix sort optimization for applicable single-column sorts
- **testSpillFrequency**: Test-only parameter to force periodic spilling every N records
- Memory manager settings affect page size and spilling behavior

## Edge Cases

- **Null handling**: Handled by prefix comparators and row ordering implementations
- **Empty partition handling**: Creates sorter but processes no rows, safely handles cleanup
- **Resource cleanup**: Overrides `cleanupResources()` to properly close `UnsafeExternalRowSorter`
- **ThreadLocal management**: Each task gets its own sorter instance to avoid concurrency issues

## Examples

```
*(5) Sort [col1#0 ASC NULLS FIRST], true, 0
+- *(4) Project [col1#0, col2#1]
   +- *(4) Filter isnotnull(col1#0)
      +- *(4) FileScan parquet [col1#0,col2#1]
```

Global sort with shuffle:
```
SortExec [amount#5 DESC], true
+- Exchange rangepartitioning(amount#5 DESC, 200)
   +- FileScan parquet [id#4,amount#5]
```

## See Also

- **TakeOrderedAndProjectExec**: For TOP-N queries with sorting
- **SortMergeJoinExec**: Uses SortExec to pre-sort join inputs  
- **Exchange**: Often precedes SortExec for global sorts
- **UnsafeExternalRowSorter**: The underlying sorting implementation