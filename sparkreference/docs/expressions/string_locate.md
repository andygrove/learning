# StringLocate

## Overview
The `StringLocate` expression finds the position of the first occurrence of a substring within a string, starting from a specified position. It returns a 1-based index of the substring's location, or 0 if the substring is not found or if invalid parameters are provided.

## Syntax
```sql
LOCATE(substr, str[, start])
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| substr | String | The substring to search for within the main string |
| str | String | The main string to search within |
| start | Integer | Optional starting position for the search (1-based index). Defaults to 1 if not specified |

## Return Type
`IntegerType` - Returns the 1-based position of the substring, or 0 if not found.

## Supported Data Types

- Input strings must be `StringType` with non-CSAI collation support
- Start position must be `IntegerType`
- Supports trim collation operations
- Uses UTF8String internally for string processing

## Algorithm

- Evaluates the start position first; returns 0 if start is null (Hive compatibility)
- Returns null if either substr or str parameters are null
- Returns 0 if start position is less than 1
- Converts 1-based start position to 0-based for internal processing
- Uses `CollationSupport.StringLocate.exec()` for the actual string search operation
- Converts the result back to 1-based indexing by adding 1

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null start position**: Returns 0 (conforms to Hive behavior)
- **Null substr**: Returns null
- **Null str**: Returns null  
- **Start position < 1**: Returns 0
- **Empty substring**: Behavior depends on collation implementation
- **Start position beyond string length**: Returns 0
- **Substring not found**: Returns 0

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method. The generated code:

- Performs inline null checks for all three parameters
- Uses direct CollationSupport calls for optimal performance  
- Avoids object allocation in the hot path
- Falls back to interpreted mode only if code generation fails

## Examples
```sql
-- Basic usage
SELECT LOCATE('world', 'hello world'); -- Returns 7

-- With start position  
SELECT LOCATE('o', 'hello world', 5); -- Returns 8

-- Substring not found
SELECT LOCATE('xyz', 'hello world'); -- Returns 0

-- Null handling
SELECT LOCATE(NULL, 'hello world'); -- Returns NULL
SELECT LOCATE('hello', NULL); -- Returns NULL
SELECT LOCATE('hello', 'hello world', NULL); -- Returns 0
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.locate

df.select(locate(lit("world"), col("text_column")))
df.select(locate(lit("pattern"), col("text_column"), lit(5)))
```

## See Also

- `StringInStr` - Similar functionality with different parameter order
- `SubstringIndex` - Extract substring based on delimiter and occurrence
- `RegExpExtract` - Pattern-based substring extraction