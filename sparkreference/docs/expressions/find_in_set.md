# FindInSet

## Overview
The FindInSet expression searches for a substring within a comma-separated string and returns the position (1-based index) of the first occurrence. It implements the SQL `FIND_IN_SET` function which is commonly used to search for values in delimited lists stored as strings.

## Syntax
```sql
FIND_IN_SET(str, str_list)
```

```scala
// DataFrame API
col("str_list").findInSet(col("str"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left (str) | StringType | The substring to search for within the comma-separated list |
| right (str_list) | StringType | The comma-separated string list to search within |

## Return Type
`IntegerType` - Returns the 1-based position of the substring in the list, or 0 if not found.

## Supported Data Types

- Input types: `StringType` with collation support (supports trim collation)
- Both arguments must be string types and support the same collation
- Automatic type casting is applied through `ImplicitCastInputTypes`

## Algorithm

- Extracts the collation ID from the left expression's string type for consistent string comparison
- Delegates actual search logic to `CollationSupport.FindInSet.exec()` method
- Performs collation-aware string matching when comparing the search string against comma-separated values
- Returns 1-based index position of first match, or 0 if no match is found
- Uses null-safe evaluation to handle null inputs properly

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning as it operates row-by-row
- Does not require data shuffling between partitions
- Can be applied within partition boundaries independently

## Edge Cases

- **Null handling**: Expression is null-intolerant (`nullIntolerant = true`), meaning if either input is null, the result is null
- **Empty strings**: Empty search string or empty list string will return 0 (not found)
- **Collation sensitivity**: String matching behavior depends on the collation settings of the input string types
- **Exact matching**: Only finds exact substring matches within the comma-separated segments

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which generates optimized Java code using `CollationSupport.FindInSet.genCode()` for better runtime performance.

## Examples
```sql
-- Find position of 'b' in comma-separated list
SELECT FIND_IN_SET('b', 'a,b,c,d') AS position; -- Returns: 2

-- Search for non-existent value
SELECT FIND_IN_SET('x', 'a,b,c,d') AS position; -- Returns: 0

-- Handle null inputs
SELECT FIND_IN_SET(NULL, 'a,b,c') AS position; -- Returns: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(find_in_set(col("search_term"), col("csv_list")).alias("position"))

// Example with literal values
df.select(find_in_set(lit("apple"), col("fruit_list")).alias("apple_position"))
```

## See Also

- `INSTR` - Find substring position within a single string
- `LOCATE` - Similar substring search functionality  
- `SPLIT` - Convert delimited strings to arrays
- `ARRAY_CONTAINS` - Search within array data types