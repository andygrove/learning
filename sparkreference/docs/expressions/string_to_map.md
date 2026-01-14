# StringToMap

## Overview
StringToMap is a Spark Catalyst expression that converts a string representation into a MapType by parsing key-value pairs using configurable delimiters. It takes a text string and splits it into map entries based on specified pair and key-value delimiters.

## Syntax
```sql
str_to_map(text, pairDelim, keyValueDelim)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| text | Expression | The input string to be parsed into a map |
| pairDelim | Expression | The delimiter used to separate key-value pairs |
| keyValueDelim | Expression | The delimiter used to separate keys from values within each pair |

## Return Type
MapType with StringType keys and StringType values (Map[String, String])

## Supported Data Types

- **text**: StringType or expressions that can be cast to StringType
- **pairDelim**: StringType literals or expressions
- **keyValueDelim**: StringType literals or expressions

## Algorithm

- Splits the input text string using the pair delimiter to extract individual key-value pair strings
- For each pair string, splits it using the key-value delimiter to separate the key and value components
- Constructs a map data structure from the extracted key-value pairs
- Handles malformed pairs by either skipping them or applying default null handling behavior
- Returns the resulting map with string keys and string values

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it operates on individual rows without requiring data movement
- Does not require shuffle operations since it's a row-level transformation
- Can be pushed down and executed within existing partitions

## Edge Cases

- **Null handling**: Returns null when the input text is null
- **Empty input**: Returns an empty map when input string is empty
- **Missing delimiters**: Handles cases where delimiters are not found in the expected positions
- **Duplicate keys**: Later occurrences of the same key may overwrite earlier ones
- **Malformed pairs**: Pairs that don't contain the key-value delimiter may be skipped or result in null values
- **Empty keys or values**: Supports empty strings as valid keys or values

## Code Generation
This expression likely supports Spark's code generation (Tungsten) for optimized execution, as it performs straightforward string operations that can be efficiently compiled to Java bytecode.

## Examples
```sql
-- Basic usage with comma and colon delimiters
SELECT str_to_map('key1:value1,key2:value2', ',', ':') AS result;
-- Returns: {"key1":"value1", "key2":"value2"}

-- Using different delimiters
SELECT str_to_map('a=1;b=2;c=3', ';', '=') AS result;
-- Returns: {"a":"1", "b":"2", "c":"3"}

-- Handling null values in the result
SELECT str_to_map('a:,b:value2', ',', ':') AS result;
-- Returns: {"a":null, "b":"value2"}
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("str_to_map(text_column, ',', ':')").as("parsed_map"))

// Using with column references
df.select(expr("str_to_map(input_text, pair_delim_col, kv_delim_col)").as("result"))
```

## See Also

- **MapType**: The return type of this expression
- **CreateMap**: Expression for creating maps from explicit key-value pairs
- **MapKeys/MapValues**: Functions for extracting keys or values from maps
- **Split**: Related string splitting functionality