# CurrentBatchTimestamp

## Overview
The `CurrentBatchTimestamp` expression represents a timestamp value that remains constant for the duration of a streaming batch. It is designed to prevent optimizer from pushing it below stateful operators and allows IncrementalExecution to substitute it with a literal value during streaming query execution.

## Syntax
```sql
current_batch_timestamp()
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| timestampMs | Long | The timestamp value in milliseconds |
| dataType | DataType | The target data type (TimestampType, TimestampNTZType, or DateType) |
| timeZoneId | Option[String] | Optional timezone identifier for timezone-aware conversions |

## Return Type
Returns one of the following data types based on the configured `dataType` parameter:

- `TimestampType` - Returns timestamp in microseconds
- `TimestampNTZType` - Returns timezone-naive timestamp in microseconds  
- `DateType` - Returns date as days since epoch

## Supported Data Types
This expression supports conversion to the following output data types:

- TimestampType (with timezone)
- TimestampNTZType (timezone-naive)
- DateType

## Algorithm
The expression evaluation follows these steps:

- Converts the input timestamp from milliseconds to microseconds using `millisToMicros()`
- For TimestampType: Returns the microsecond timestamp directly
- For TimestampNTZType: Applies timezone conversion from UTC to the specified zone using `convertTz()`
- For DateType: Converts microseconds to days since epoch using `microsToDays()`
- Returns the final literal value through `toLiteral.value`

## Partitioning Behavior
This expression has minimal impact on partitioning:

- Does not require shuffle operations as it's a leaf expression
- Preserves existing partitioning schemes
- Marked as nondeterministic to prevent inappropriate optimizations across batches

## Edge Cases

- Null handling: Expression is marked as non-nullable (`nullable = false`)
- Empty input: Returns the configured timestamp value regardless of input row content
- Timezone conversion: When no timeZoneId is provided, defaults to system timezone for conversions
- Batch consistency: Same timestamp value is returned for all rows within a single batch

## Code Generation
This expression uses `CodegenFallback`, meaning it does not support Tungsten code generation and falls back to interpreted evaluation mode. This is intentional since the expression should be replaced with a literal during query planning.

## Examples
```sql
-- Returns current batch timestamp as timestamp type
SELECT current_batch_timestamp()

-- Can be used in streaming queries to get batch processing time
SELECT id, value, current_batch_timestamp() as batch_time FROM streaming_table
```

```scala
// DataFrame API usage in streaming context
import org.apache.spark.sql.functions._

val streamingDF = spark.readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "localhost:9092")  
  .load()

val withBatchTime = streamingDF.select(
  col("value"),
  expr("current_batch_timestamp()").as("batch_time")
)
```

## See Also

- `CurrentTimestamp` - Returns current system timestamp
- `Literal` - Static literal values
- `TimeZoneAwareExpression` - Base trait for timezone-aware expressions
- `Nondeterministic` - Trait for expressions that return different values across evaluations