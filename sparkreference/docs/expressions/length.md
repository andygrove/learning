# Length

## Overview
The Length expression calculates the number of characters in a string or the number of bytes in a binary value. It is a unary expression that supports implicit type casting and returns an integer representing the length of the input data.

## Syntax
```sql
LENGTH(str)
```

```scala
// DataFrame API
col("column_name").length
length(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression containing string or binary data to measure |

## Return Type
`IntegerType` - Returns an integer representing the length of the input.

## Supported Data Types

- `StringType` with collation support (including trim collation)
- `BinaryType`

## Algorithm

- For string inputs, calculates the number of Unicode characters using `UTF8String.numChars()`
- For binary inputs, returns the byte array length using `Array[Byte].length`
- Supports implicit type casting to convert compatible input types
- Uses null-safe evaluation with null intolerance (returns null for null inputs)
- Leverages context-independent foldability for constant folding optimizations

## Partitioning Behavior
This expression preserves partitioning as it:

- Does not require data movement between partitions
- Operates on individual rows independently
- Does not require shuffle operations

## Edge Cases

- **Null handling**: Returns null for null inputs (null intolerant behavior)
- **Empty strings**: Returns 0 for empty strings
- **Empty binary**: Returns 0 for empty byte arrays
- **Unicode strings**: Correctly counts Unicode characters, not bytes
- **Collation support**: Handles string collations including trim collation variants

## Code Generation
This expression supports Tungsten code generation:

- For string types: Generates `($c).numChars()` code
- For binary types: Generates `($c).length` code
- Falls back to interpreted mode only if code generation context doesn't support it

## Examples
```sql
-- String length examples
SELECT LENGTH('hello') AS len1;          -- Returns: 5
SELECT LENGTH('') AS len2;               -- Returns: 0
SELECT LENGTH(NULL) AS len3;             -- Returns: NULL
SELECT LENGTH('café') AS len4;           -- Returns: 4 (Unicode characters)

-- Binary length examples  
SELECT LENGTH(CAST('hello' AS BINARY)) AS bin_len;  -- Returns: 5
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic usage
df.select(length(col("name")).as("name_length"))

// With column method
df.select(col("description").length.as("desc_length"))

// In filter conditions
df.filter(length(col("code")) > 10)
```

## See Also

- `Substring` - Extract portions of strings
- `Concat` - Combine multiple strings
- `Trim` - Remove whitespace (works with trim collation)
- `Octet_Length` - Get byte length of strings