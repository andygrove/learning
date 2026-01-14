# Concat

## Overview
The `Concat` expression concatenates multiple input expressions into a single result. It supports concatenating strings with collation support, binary data, and arrays, returning a combined result of the same data type as the inputs.

## Syntax
```sql
concat(expr1, expr2, ..., exprN)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr1, expr2, ..., exprN | StringType, BinaryType, or ArrayType | Variable number of expressions to concatenate. All expressions must be of the same compatible type |

## Return Type
Returns the same data type as the input expressions:

- `StringType` for string inputs (or `StringType` if no arguments provided)
- `BinaryType` for binary inputs  
- `ArrayType(elementType, containsNull)` for array inputs

## Supported Data Types

- `StringType` with collation support (including trim collation)
- `BinaryType` 
- `ArrayType` of any element type

## Algorithm

- For empty input, returns empty string of `StringType`
- For string inputs, uses `UTF8String.concat()` to merge all input strings
- For binary inputs, uses `ByteArray.concat()` to merge all byte arrays
- For array inputs, flattens all arrays into a single array, checking total element count against `MAX_ROUNDED_ARRAY_LENGTH`
- Validates all inputs are of compatible types during type checking phase

## Partitioning Behavior
This expression does not affect partitioning:

- Preserves existing partitioning as it operates row-by-row
- Does not require shuffle operations
- Can be pushed down to individual partitions

## Edge Cases

- **Null handling**: If any input expression evaluates to null, the entire result is null
- **Empty input**: Returns empty string (`StringType`) when no arguments provided
- **Array overflow**: Throws `QueryExecutionError` if total array elements exceed `MAX_ROUNDED_ARRAY_LENGTH`
- **Type compatibility**: All inputs must be the same type - mixed types (e.g., string + binary) will fail type checking
- **Nullability**: Result is nullable if any child expression is nullable

## Code Generation
This expression supports Tungsten code generation:

- Generates optimized code paths for each supported data type (`BinaryType`, `StringType`, `ArrayType`)
- Uses `splitExpressionsWithCurrentInputs` for handling large numbers of input expressions
- Falls back to interpreted evaluation only during the code generation setup phase

## Examples
```sql
-- String concatenation
SELECT concat('Hello', ' ', 'World') AS greeting;
-- Result: 'Hello World'

-- Array concatenation  
SELECT concat(array(1, 2), array(3, 4), array(5)) AS combined_array;
-- Result: [1, 2, 3, 4, 5]

-- Null handling
SELECT concat('Hello', NULL, 'World') AS result;
-- Result: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.concat

df.select(concat($"first_name", lit(" "), $"last_name").as("full_name"))

// Array concatenation
df.select(concat($"array_col1", $"array_col2").as("combined_arrays"))
```

## See Also

- `concat_ws` - Concatenate with separator
- `array_union` - Union of array elements
- `||` operator - String concatenation operator