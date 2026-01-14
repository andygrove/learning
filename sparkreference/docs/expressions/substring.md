# Substring

## Overview
The `Substring` expression extracts a portion of a string or binary array starting from a specified position with an optional length parameter. It implements SQL-compatible substring functionality with 1-based indexing, supporting both string types with collation and binary data types.

## Syntax
```sql
SUBSTRING(str, pos[, len])
-- or
SUBSTR(str, pos[, len])
```

```scala
// DataFrame API
col("column").substr(pos, len)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | StringType with collation or BinaryType | The source string or binary data to extract from |
| pos | IntegerType | Starting position (1-based indexing) |
| len | IntegerType | Maximum length of substring to extract (optional, defaults to Integer.MAX_VALUE) |

## Return Type
Returns the same data type as the input `str` argument (StringType with same collation or BinaryType).

## Supported Data Types

- StringType with collation (supports trim collation)
- BinaryType

## Algorithm

- Validates input types through implicit casting to required types
- Uses 1-based SQL indexing for position parameter
- For StringType: delegates to `UTF8String.substringSQL()` method
- For BinaryType: delegates to `ByteArray.subStringSQL()` method
- Handles variable-length extraction when length parameter is omitted

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows without requiring data movement:

- Does not require shuffle operations
- Maintains existing partitioning scheme
- Can be pushed down to individual partitions

## Edge Cases

- **Null handling**: Expression is null-intolerant, returns null if any input is null
- **Position bounds**: Positions less than 1 or beyond string length follow SQL semantics
- **Negative length**: Handled according to SQL standard behavior
- **Empty input**: Empty strings return empty results
- **Length overflow**: Uses Integer.MAX_VALUE as default when length is omitted

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method:

- Generates optimized bytecode for both StringType and BinaryType cases
- Uses `defineCodeGen` helper for efficient code generation
- Falls back to interpreted mode only when code generation context limits are exceeded

## Examples
```sql
-- Extract substring from position 2 with length 3
SELECT SUBSTRING('Apache Spark', 2, 6) AS result;
-- Returns: 'pache '

-- Extract from position 8 to end of string
SELECT SUBSTRING('Apache Spark', 8) AS result;
-- Returns: 'park'

-- Binary data extraction
SELECT SUBSTRING(CAST('binary data' AS BINARY), 1, 6) AS result;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("text").substr(2, 6).alias("substring"))

// Using substring with dynamic position
df.select(substring(col("text"), col("start_pos"), col("length")))
```

## See Also

- `Left` - Extract characters from the left side of a string
- `Right` - Extract characters from the right side of a string
- `StringTrim` - Remove leading/trailing whitespace with collation support