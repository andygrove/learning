# Spark Expressions Reference

This section documents Apache Spark SQL expressions - the building blocks of query evaluation.

## What are Expressions?

Expressions in Spark SQL are nodes in the query tree that can be evaluated to produce a value. They include:

- **Arithmetic operations** - Add, Subtract, Multiply, Divide
- **Comparisons** - EqualTo, LessThan, GreaterThan
- **Logical operations** - And, Or, Not
- **String functions** - Substring, Concat, Upper, Lower
- **Aggregate functions** - Sum, Count, Average, Max, Min
- **Window functions** - RowNumber, Rank, Lead, Lag
- **Type conversions** - Cast, implicit coercions

## Expression Categories

### Grouping & Aggregation
- [Grouping](grouping.md) - Check if column is aggregated
- [GroupingID](grouping_id.md) - Get grouping bitmask

### Interval Operations
- [MakeInterval](make_interval.md) - Create interval from components
- [MakeDTInterval](make_dt_interval.md) - Create day-time interval
- [MakeYMInterval](make_ym_interval.md) - Create year-month interval
- [TryMakeInterval](try_make_interval.md) - Safe interval creation
- [MultiplyYMInterval](multiply_ym_interval.md) - Multiply year-month interval
- [MultiplyDTInterval](multiply_dt_interval.md) - Multiply day-time interval
- [DivideYMInterval](divide_ym_interval.md) - Divide year-month interval
- [DivideDTInterval](divide_dt_interval.md) - Divide day-time interval

### Bitwise Operations
- [BitwiseAnd](bitwise_and.md) - Bitwise AND
- [BitwiseOr](bitwise_or.md) - Bitwise OR
- [BitwiseXor](bitwise_xor.md) - Bitwise XOR
- [BitwiseNot](bitwise_not.md) - Bitwise NOT
- [BitwiseCount](bitwise_count.md) - Count set bits
- [BitwiseGet](bitwise_get.md) - Get specific bit

### String Formatting
- [ToCharacter](to_character.md) - Format number as string

### Input Metadata
- [InputFileName](input_file_name.md) - Current input file name
- [InputFileBlockStart](input_file_block_start.md) - File block start offset
- [InputFileBlockLength](input_file_block_length.md) - File block length

### System Functions
- [SparkPartitionID](spark_partition_id.md) - Current partition ID
- [MonotonicallyIncreasingID](monotonically_increasing_id.md) - Generate unique IDs
- [DirectShufflePartitionID](direct_shuffle_partition_id.md) - Shuffle partition ID

### Sorting
- [SortOrder](sort_order.md) - Sort specification
- [SortPrefix](sort_prefix.md) - Sort prefix computation

### Other
- [NamedArgumentExpression](named_argument_expression.md) - Named function arguments
- [PipeExpression](pipe_expression.md) - Pipe operator support

---

*More expressions are documented as they are generated. Run `python scripts/generate_spark_reference.py --type expressions` to generate additional pages.*
