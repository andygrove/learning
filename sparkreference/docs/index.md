# Spark Internals Reference Guide

A comprehensive reference guide to Apache Spark SQL internals, covering expressions and physical operators.

## Structure

- **[expressions/](expressions/)** - Catalyst expression reference (functions, operators, literals)
- **[operators/](operators/)** - Physical execution operator reference (joins, aggregates, exchanges)

## Generated Pages

### Expressions (35 pages)

#### Aggregates & Grouping
- [BaseGroupingSets](expressions/base_grouping_sets.md) - CUBE, ROLLUP, GROUPING SETS
- [Grouping](expressions/grouping.md) - Grouping indicator function

#### Arithmetic & Math
- [BitwiseAnd](expressions/bitwise_and.md) - Bitwise AND operation
- [Years](expressions/years.md) - Year interval expression

#### Collection Operations
- [CreateArray](expressions/create_array.md) - Array creation
- [GetStructField](expressions/get_struct_field.md) - Struct field extraction
- [Size](expressions/size.md) - Collection size

#### String & Format
- [ToCharacter](expressions/to_character.md) - Number to string formatting
- [ToNumberBase](expressions/to_number_base.md) - String to number parsing
- [UrlEncode](expressions/url_encode.md) - URL encoding
- [CollationKey](expressions/collation_key.md) - Collation key generation

#### Date/Time
- [ExtractIntervalPart](expressions/extract_interval_part.md) - Interval extraction
- [TryMakeInterval](expressions/try_make_interval.md) - Safe interval creation

#### Window Functions
- [WindowSpecDefinition](expressions/window_spec_definition.md) - Window specification

#### UDFs
- [PythonUDF](expressions/python_udf.md) - Python user-defined functions
- [ScalaUDF](expressions/scala_udf.md) - Scala user-defined functions

#### Subqueries
- [DynamicPruningSubquery](expressions/dynamic_pruning_subquery.md) - Dynamic partition pruning
- [OuterReference](expressions/outer_reference.md) - Correlated subquery references

#### Serialization
- [CsvToStructs](expressions/csv_to_structs.md) - CSV parsing
- [FromProtobuf](expressions/from_protobuf.md) - Protobuf deserialization
- [SemiStructuredExtract](expressions/semi_structured_extract.md) - Semi-structured data extraction

#### Sketches & Approximate
- [HllSketchEstimate](expressions/hll_sketch_estimate.md) - HyperLogLog cardinality
- [ThetaSketchEstimate](expressions/theta_sketch_estimate.md) - Theta sketch operations
- [BitmapBucketNumber](expressions/bitmap_bucket_number.md) - Bitmap operations

#### Internal/System
- [SparkPartitionID](expressions/spark_partition_id.md) - Current partition ID
- [MonotonicallyIncreasingID](expressions/monotonically_increasing_id.md) - Unique ID generation
- [DirectShufflePartitionID](expressions/direct_shuffle_partition_id.md) - Shuffle partition ID
- [InputFileName](expressions/input_file_name.md) - Input file metadata

#### Other
- [ApplyFunctionExpression](expressions/apply_function_expression.md) - Function application
- [InterpretedPredicate](expressions/interpreted_predicate.md) - Predicate evaluation
- [NamedArgumentExpression](expressions/named_argument_expression.md) - Named arguments
- [PipeExpression](expressions/pipe_expression.md) - Pipe operator
- [SortOrder](expressions/sort_order.md) - Sort ordering
- [TryEval](expressions/try_eval.md) - Error handling wrapper
- [UnresolvedNamedLambdaVariable](expressions/unresolved_named_lambda_variable.md) - Lambda variables

### Operators (10 pages)

#### Joins
- [BroadcastHashJoinExec](operators/broadcast_hash_join_exec.md) - Broadcast hash join

#### Aggregation
- [ObjectHashAggregateExec](operators/object_hash_aggregate_exec.md) - Object-based aggregation
- [MergingSessionsExec](operators/merging_sessions_exec.md) - Session window merging
- [UpdatingSessionsExec](operators/updating_sessions_exec.md) - Session window updates

#### Basic Operations
- [ProjectExec](operators/project_exec.md) - Column projection
- [SortExec](operators/sort_exec.md) - Sorting
- [GenerateExec](operators/generate_exec.md) - Generator/explode
- [ExpandExec](operators/expand_exec.md) - GROUPING SETS expansion

#### Limits & Top-N
- [TakeOrderedAndProjectExec](operators/take_ordered_and_project_exec.md) - Top-N with projection

#### Code Generation
- [WholeStageCodegenExec](operators/whole_stage_codegen_exec.md) - Whole-stage codegen wrapper

## Page Structure

Each reference page includes:

### For Expressions
- Overview
- Syntax (SQL and DataFrame API)
- Arguments
- Return Type
- Supported Data Types
- Algorithm
- Partitioning Behavior
- Edge Cases
- Code Generation Support
- Examples
- See Also

### For Operators
- Overview
- When Used (planner rules)
- Input Requirements
- Output Properties
- Algorithm
- Memory Usage
- Partitioning Behavior
- Metrics
- Code Generation Support
- Configuration Options
- Edge Cases
- Examples
- See Also

