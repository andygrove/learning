# SampleExec

## Overview
SampleExec is a physical operator that performs statistical sampling on input data by randomly selecting a fraction of rows. It supports both sampling with replacement (using Poisson distribution) and without replacement (using Bernoulli sampling) to produce a representative subset of the input dataset.

## When Used
The query planner chooses SampleExec when executing SQL TABLESAMPLE clauses or DataFrame sample() operations. It is selected when the logical plan contains a Sample node that specifies sampling bounds and replacement strategy.

## Input Requirements
- **Expected input partitioning**: No specific partitioning requirements - preserves child's partitioning
- **Expected input ordering**: No ordering requirements - sampling is performed independently of row order
- **Number of children**: Unary operator (extends UnaryExecNode) - requires exactly one child SparkPlan

## Output Properties
- **Output partitioning**: Identical to child's output partitioning (`child.outputPartitioning`)
- **Output ordering**: No guaranteed ordering - sampling may alter the relative order of rows
- **How output schema is derived**: Output schema is identical to child's schema (`child.output`)

## Algorithm
- Calculate the sampling fraction as `upperBound - lowerBound`
- For sampling with replacement: Use `PoissonSampler` with `PartitionwiseSampledRDD` to allow multiple copies of the same row
- For sampling without replacement: Use `BernoulliCellSampler` via `randomSampleWithRange()` to ensure each row appears at most once
- Apply partition-specific random seeds to ensure deterministic results across partitions
- Generate random decisions for each input row independently
- Emit rows that pass the sampling test while tracking output row count metrics
- Preserve partitioning structure to avoid unnecessary shuffles

## Memory Usage
- **Does it spill to disk?**: No - SampleExec performs streaming sampling without materialization
- **Memory requirements/configuration**: Minimal memory footprint - only maintains sampler state and random number generators
- **Buffering behavior**: Gap sampling is explicitly disabled for replacement sampling to avoid buffering overhead

## Partitioning Behavior
- **How it affects data distribution**: Reduces data volume while preserving relative distribution across partitions
- **Shuffle requirements**: None - operates within existing partitions (`preservesPartitioning = true`)
- **Partition count changes**: Maintains the same number of partitions as the child operator

## Supported Join/Aggregation Types
Not applicable - SampleExec is a sampling operator, not a join or aggregation operator.

## Metrics
- **numOutputRows**: Tracks the total number of rows produced after sampling (SQLMetrics.createMetric)

## Code Generation
Yes, SampleExec implements `CodegenSupport` for whole-stage code generation. It generates inline sampling logic using either `PoissonSampler` or `BernoulliCellSampler` depending on the replacement strategy, with partition-aware seed initialization.

## Configuration Options
- Sampling behavior is controlled by operator parameters rather than global Spark configurations
- Random seed can be specified for reproducible sampling results
- Gap sampling is hardcoded as disabled for replacement sampling

## Edge Cases
- **Null handling**: Preserves null values in sampled rows - nulls are treated like any other row value
- **Empty partition handling**: Empty partitions remain empty after sampling
- **Skew handling**: Sampling may amplify or reduce skew depending on data distribution and sampling parameters

## Examples
```
+- Sample 0.0, 0.3, false, 1234
   +- FileScan parquet [id, name, value]
```

Example SQL query:
```sql
SELECT * FROM table TABLESAMPLE (30 PERCENT) REPEATABLE (1234)
```

## See Also
- **FilterExec**: For deterministic row filtering based on predicates
- **LimitExec**: For taking a fixed number of rows from the beginning
- **PartitionwiseSampledRDD**: The underlying RDD implementation for replacement sampling