# SplitPart

## Overview
The `SplitPart` expression splits a string by a specified delimiter and returns the part at a given position. It is a runtime replaceable expression that internally uses `StringSplitSQL` and `ElementAt` to extract the specified part from the split string array.

## Syntax
```sql
SPLIT_PART(str, delimiter, partNum)
```

```scala
split_part(str, delimiter, partNum)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | String | The input string to be split |
| delimiter | String | The delimiter string used to split the input |
| partNum | Integer | The 1-based position of the part to return |

## Return Type
Returns a string data type containing the specified part of the split string.

## Supported Data Types

- **str**: String types with non-CSAI collation (supports trim collation)
- **delimiter**: String types with non-CSAI collation (supports trim collation)  
- **partNum**: Integer type only

## Algorithm

- Splits the input string using `StringSplitSQL` with the provided delimiter
- Uses `ElementAt` to extract the element at the specified position from the resulting array
- Applies 1-based indexing for the part number parameter
- Returns an empty string as the default value when the specified part doesn't exist
- Supports implicit type casting for input arguments

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffling as it operates on individual rows
- Maintains existing partitioning scheme since it's a deterministic row-level transformation
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null if any input argument (str, delimiter, or partNum) is null
- **Empty string input**: Returns empty string when splitting an empty string
- **Invalid part number**: Returns empty string for part numbers that exceed the number of split parts
- **Zero or negative part numbers**: Follows ElementAt behavior for invalid indices
- **Empty delimiter**: May result in character-by-character splitting depending on underlying StringSplitSQL implementation

## Code Generation
This expression supports code generation through the Tungsten engine since it is implemented as a `RuntimeReplaceable` expression that delegates to code-gen enabled expressions (`StringSplitSQL` and `ElementAt`).

## Examples
```sql
-- Extract the third part from a dot-delimited string
SELECT SPLIT_PART('11.12.13', '.', 3);
-- Result: 13

-- Extract first part from a comma-delimited string  
SELECT SPLIT_PART('apple,banana,cherry', ',', 1);
-- Result: apple

-- Handle case where part number exceeds available parts
SELECT SPLIT_PART('a.b', '.', 5);
-- Result: (empty string)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("split_part(column_name, '.', 2)"))

// Using column references
df.select(split_part(col("str_column"), lit("."), lit(1)))
```

## See Also

- `StringSplitSQL` - The underlying string splitting expression
- `ElementAt` - Used internally to extract array elements
- `Split` - Related function that returns the full array of split parts
- `Substring` - Alternative for extracting string portions