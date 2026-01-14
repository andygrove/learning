# Levenshtein

## Overview
The Levenshtein expression computes the Levenshtein distance (also known as edit distance) between two strings. This represents the minimum number of single-character edits (insertions, deletions, or substitutions) required to transform one string into another. An optional threshold parameter can be provided to limit the maximum distance calculated.

## Syntax
```sql
LEVENSHTEIN(str1, str2)
LEVENSHTEIN(str1, str2, threshold)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str1 | String | The first input string for comparison |
| str2 | String | The second input string for comparison |
| threshold | Integer (optional) | Maximum distance to calculate; computation stops early if distance exceeds this value |

## Return Type
Integer - representing the Levenshtein distance between the two input strings.

## Supported Data Types

- **Input strings**: StringType with collation support (supports trim collation)
- **Threshold**: IntegerType
- **Output**: IntegerType

## Algorithm
The expression is evaluated using the following approach:

- Validates that 2 or 3 arguments are provided (throws compilation error otherwise)
- Performs null checks on all input expressions, returning null if any input is null
- Delegates to the UTF8String.levenshteinDistance method for the actual calculation
- Uses the optimized threshold-aware version when a threshold is provided
- Supports both code generation and interpreted evaluation modes

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be executed locally on each partition

## Edge Cases

- **Null handling**: Returns null if any input parameter (left, right, or threshold) is null
- **Empty strings**: Handles empty strings correctly - distance equals the length of the non-empty string
- **Identical strings**: Returns 0 for identical input strings
- **Threshold behavior**: When threshold is provided, computation may terminate early if distance exceeds the threshold value
- **Invalid threshold**: Negative threshold values are passed through to the underlying implementation

## Code Generation
This expression supports full code generation (Tungsten):

- Implements `doGenCode` method with optimized code paths
- Generates separate code for threshold and non-threshold variants
- Includes proper null-safe evaluation in generated code
- Falls back to UTF8String methods for the actual distance calculation

## Examples
```sql
-- Basic usage
SELECT LEVENSHTEIN('kitten', 'sitting');  -- Returns 3

-- With threshold
SELECT LEVENSHTEIN('kitten', 'sitting', 5);  -- Returns 3

-- Null handling
SELECT LEVENSHTEIN('test', NULL);  -- Returns NULL

-- Empty strings
SELECT LEVENSHTEIN('', 'abc');  -- Returns 3
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(levenshtein(col("str1"), col("str2")))

// With threshold (using expr for SQL function)
df.select(expr("levenshtein(str1, str2, 5)"))
```

## See Also

- String similarity functions
- SOUNDEX for phonetic similarity
- String manipulation expressions in the string_funcs group