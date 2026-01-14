# V2Aggregator

## Overview
V2Aggregator is a Spark Catalyst expression that wraps a Data Source V2 aggregate function for execution within the Catalyst optimizer and code generation framework. It provides a bridge between the external V2 aggregate function interface and Spark's internal expression evaluation system, handling serialization of intermediate buffer states and type conversions.

## Syntax
```scala
V2Aggregator[BUF, OUT](
  aggregateFunction: V2AggregateFunction,
  inputAggBufferOffset: Int = 0,
  mutableAggBufferOffset: Int = 0
)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| BUF | Type Parameter | The buffer type for intermediate aggregation state, must extend java.io.Serializable |
| OUT | Type Parameter | The output type of the aggregation result |
| aggregateFunction | V2AggregateFunction | The underlying Data Source V2 aggregate function implementation |
| inputAggBufferOffset | Int | Offset for reading from input aggregation buffer during merge operations |
| mutableAggBufferOffset | Int | Offset for writing to mutable aggregation buffer during updates |

## Return Type
Returns the data type specified by the wrapped V2AggregateFunction's `resultType()` method, corresponding to the OUT type parameter.

## Supported Data Types

- Input data types are determined by the wrapped V2AggregateFunction's `inputTypes()` method
- Buffer type must implement java.io.Serializable for proper serialization across network boundaries
- Output type is specified by the V2AggregateFunction implementation
- Supports complex data types including nested structures, arrays, and maps as defined by the V2 function

## Algorithm

- Initializes aggregation buffer using the V2AggregateFunction's buffer initialization logic
- Updates buffer state by delegating to the V2AggregateFunction's update method with input values
- Merges partial aggregation buffers by deserializing buffer states and calling the V2AggregateFunction's merge method
- Produces final result by calling the V2AggregateFunction's produceResult method on the final buffer state
- Handles serialization/deserialization of buffer states for shuffle operations and network transport

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve input partitioning as it performs aggregation operations
- Requires shuffle operation when used in global aggregations or when grouping keys span multiple partitions
- May benefit from pre-shuffle aggregation (map-side combine) when buffer serialization is efficient
- Partitioning of results depends on grouping expressions used alongside the aggregator

## Edge Cases

- Null input handling is delegated to the underlying V2AggregateFunction implementation
- Empty input results in the initial buffer state being passed to produceResult()
- Buffer serialization failures will cause task failures and potential job failure
- Type mismatches between declared type parameters and V2AggregateFunction types may cause ClassCastException
- Large buffer states may cause memory pressure and serialization performance issues

## Code Generation
V2Aggregator typically falls back to interpreted mode as it wraps external V2AggregateFunction implementations that are not part of Catalyst's code generation framework. The serialization and deserialization of buffer states also limits code generation opportunities.

## Examples
```sql
-- V2Aggregator is not directly accessible from SQL
-- It is used internally when V2 data sources provide custom aggregate functions
SELECT custom_v2_agg(column1) FROM table
```

```scala
// Example DataFrame API usage (conceptual)
// V2Aggregator is typically instantiated internally by Catalyst
import org.apache.spark.sql.connector.catalog.functions.AggregateFunction

val customV2Agg = new MyCustomV2AggregateFunction()
val aggregator = V2Aggregator[MyBuffer, Double](
  aggregateFunction = customV2Agg,
  inputAggBufferOffset = 0,
  mutableAggBufferOffset = 0
)
```

## See Also

- AggregateExpression - For wrapping aggregate functions with additional metadata
- DeclarativeAggregate - For Catalyst-native aggregate expressions
- ImperativeAggregate - For aggregate expressions requiring imperative buffer management
- V2AggregateFunction - The underlying Data Source V2 interface for aggregate functions