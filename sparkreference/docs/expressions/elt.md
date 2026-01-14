# Elt

## Overview
The `Elt` expression returns the N-th element from a list of string or binary expressions, where N is specified by an integer index parameter. It corresponds to the SQL `ELT()` function and uses 1-based indexing, returning null if the index is out of range or null.

## Syntax
```sql
ELT(index, str1, str2, str3, ...)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| index | Integer | 1-based index specifying which element to return |
| str1, str2, ... | String or Binary | Variable number of string or binary expressions to select from |

## Return Type
Returns the same data type as the input string/binary expressions. Defaults to `StringType` if no input expressions are provided.

## Supported Data Types

- **Index parameter**: Must be `IntegerType`
- **Input expressions**: Must be `StringType` or `BinaryType`
- All input expressions must have the same data type

## Algorithm

- Evaluates the index expression to get the position
- Returns null immediately if the index is null
- Checks if index is within valid range (1 to number of input expressions)
- If index is out of range, either throws an error (ANSI mode) or returns null
- If index is valid, evaluates and returns the expression at position (index - 1)

## Partitioning Behavior
This expression preserves partitioning as it operates row-by-row without requiring data movement:

- Does not require shuffle operations
- Maintains existing data partitioning
- Can be executed locally on each partition

## Edge Cases

- Returns null if index parameter is null
- Returns null if index is <= 0 or > number of input expressions (non-ANSI mode)
- Throws `QueryExecutionErrors.invalidArrayIndexError` for out-of-range indices (ANSI mode)
- Requires at least 2 arguments (index + at least one input expression)
- All input expressions must be the same type (String or Binary)

## Code Generation
This expression supports Tungsten code generation with optimized codegen paths:

- Generates specialized code for index evaluation and bounds checking
- Uses `splitExpressionsWithCurrentInputs` for handling large numbers of input expressions
- Includes optimized null handling and error checking in generated code

## Examples
```sql
-- Basic usage
SELECT ELT(2, 'apple', 'banana', 'cherry') AS result;  -- Returns 'banana'

-- Out of range index
SELECT ELT(5, 'apple', 'banana', 'cherry') AS result;  -- Returns NULL

-- With null index
SELECT ELT(NULL, 'apple', 'banana', 'cherry') AS result;  -- Returns NULL

-- Using with binary data
SELECT ELT(1, X'41424344', X'45464748') AS result;  -- Returns X'41424344'
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.range(3).select(
  expr("ELT(1, 'first', 'second', 'third')").as("result1"),
  expr("ELT(id + 1, 'zero', 'one', 'two')").as("result2")
)
```

## See Also

- `array` - Creates arrays that can be indexed with array access
- `case` / `when` - Alternative conditional expression selection
- `coalesce` - Returns first non-null value from a list