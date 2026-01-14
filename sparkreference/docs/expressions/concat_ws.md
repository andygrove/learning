# ConcatWs

## Overview
The `ConcatWs` expression concatenates multiple strings or arrays of strings using a specified separator. It is the implementation of the `concat_ws` SQL function that was introduced in Spark 1.5.0 and belongs to the string functions group.

## Syntax
```sql
concat_ws(separator, str1, str2, ..., strN)
concat_ws(separator, array1, array2, ..., arrayN)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| separator | StringType | The separator string used to join the input strings |
| str1, str2, ..., strN | StringType or ArrayType(StringType) | Variable number of string expressions or string arrays to concatenate |

## Return Type
Returns the same data type as the separator (first child expression), typically `StringType` with collation support.

## Supported Data Types

- **Separator**: StringType with collation support (including trim collation)
- **Input values**: StringType with collation support or ArrayType containing StringType elements
- Both input types support trim collation operations

## Algorithm

- Flattens all input expressions by iterating through each child expression
- For string inputs, adds them directly to the flattened input list  
- For array inputs, converts ArrayData to individual UTF8String elements
- Handles null values by converting them to null UTF8String references
- Calls `UTF8String.concatWs()` with the separator and all flattened string elements

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning as it operates row-by-row
- Does not require shuffle operations
- Can be safely pushed down in query optimization

## Edge Cases

- **Null separator**: If the separator is null, the entire result is null
- **Null inputs**: Individual null string inputs are converted to null UTF8String objects and handled by the underlying concatWs implementation
- **Empty arrays**: Empty arrays contribute no elements to the concatenation
- **No arguments**: Throws QueryCompilationErrors.wrongNumArgsError requiring at least one argument
- **Mixed nulls**: Null elements within arrays or null string arguments are handled gracefully

## Code Generation
This expression supports Tungsten code generation with two optimized paths:

- **All strings path**: Generates a fixed-size UTF8String array for better performance when all children are StringType
- **Mixed types path**: Generates dynamic array sizing and complex iteration logic for handling mixed StringType and ArrayType inputs

## Examples
```sql
-- Basic string concatenation
SELECT concat_ws('-', 'apple', 'banana', 'cherry');
-- Result: 'apple-banana-cherry'

-- With null values
SELECT concat_ws(',', 'a', NULL, 'b');  
-- Result: 'a,b' (nulls are typically skipped)

-- With arrays
SELECT concat_ws('|', array('x', 'y'), array('z'));
-- Result: 'x|y|z'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(concat_ws("-", col("col1"), col("col2")))

// With array columns  
df.select(concat_ws("|", col("string_array1"), col("string_array2")))
```

## See Also

- `Concat` - concatenates without separator
- `StringConcat` - basic string concatenation operations
- Array functions like `array_join` for array-specific concatenation