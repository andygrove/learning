# ParseToTimestamp

## Overview
ParseToTimestamp is a Spark Catalyst expression that converts string, date, timestamp, or numeric values to a timestamp data type. It supports optional format specifications for parsing string inputs and provides timezone-aware conversion capabilities with configurable error handling behavior.

## Syntax
```sql
to_timestamp(timestamp_str[, format])
```

```scala
// DataFrame API usage
df.select(to_timestamp($"timestamp_column"))
df.select(to_timestamp($"timestamp_column", "yyyy-MM-dd HH:mm:ss"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The input expression to convert to timestamp |
| format | Option[Expression] | Optional format string for parsing input |
| dataType | DataType | Target timestamp data type |
| timeZoneId | Option[String] | Optional timezone identifier for conversion |
| failOnError | Boolean | Whether to fail on conversion errors (defaults to ANSI mode setting) |

## Return Type
Returns a timestamp data type as specified by the `dataType` parameter, typically `TimestampType` or `TimestampNTZType`.

## Supported Data Types

- StringType with collation support (including trim collation)
- DateType
- TimestampType  
- TimestampNTZType
- NumericType (only when target dataType is TimestampType)

## Algorithm

- When format is specified, delegates to `GetTimestamp` expression with the provided format string
- When no format is provided, performs a `Cast` operation to the target timestamp type
- Applies timezone conversion using the specified `timeZoneId` if provided
- Handles error scenarios based on the `failOnError` flag (ANSI compliance)
- Implements `RuntimeReplaceable` pattern, replacing itself with appropriate underlying expressions during analysis

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle as it operates on individual rows
- Maintains existing partition boundaries
- Can be applied within partition operations without affecting distribution

## Edge Cases

- Null inputs are handled gracefully and typically return null outputs
- Invalid format strings will cause runtime errors when `failOnError` is true
- Unparseable timestamp strings behavior depends on ANSI mode settings
- Numeric inputs are interpreted as seconds since epoch when converting to TimestampType
- Timezone conversion edge cases (DST transitions) are handled according to Java timezone rules

## Code Generation
This expression supports Tungsten code generation through its replacement expressions (`GetTimestamp` and `Cast`). The actual code generation is delegated to the underlying replacement expression rather than being implemented directly.

## Examples
```sql
-- Basic timestamp parsing
SELECT to_timestamp('2016-12-31 00:00:00');

-- With custom format
SELECT to_timestamp('12/31/2016 00:00:00', 'MM/dd/yyyy HH:mm:ss');

-- Converting date to timestamp
SELECT to_timestamp(current_date());
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic conversion
df.select(to_timestamp($"timestamp_str"))

// With format specification
df.select(to_timestamp($"date_str", "yyyy-MM-dd"))

// Converting numeric epoch seconds
df.select(to_timestamp($"epoch_seconds"))
```

## See Also

- `GetTimestamp` - Underlying expression for formatted parsing
- `Cast` - Underlying expression for unformatted conversion
- `ParseToDate` - Similar expression for date parsing
- `UnixTimestamp` - Converting to Unix timestamp format