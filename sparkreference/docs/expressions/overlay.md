# Overlay

## Overview
The `Overlay` expression replaces a portion of a string or binary array with another string or binary array, starting at a specified position and optionally specifying the length of the portion to replace. It supports both string operations with UTF8String and binary operations with byte arrays.

## Syntax
```sql
OVERLAY(input PLACING replace FROM pos [FOR len])
```

```scala
// DataFrame API usage
overlay(input, replace, pos, len)
overlay(input, replace, pos)  // len defaults to -1
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| input | StringType/BinaryType | The original string or binary data to modify |
| replace | StringType/BinaryType | The replacement string or binary data |
| pos | IntegerType | The starting position (1-based) where replacement begins |
| len | IntegerType | Optional length of portion to replace (defaults to -1 if not specified) |

## Return Type
Returns the same data type as the input expression (StringType or BinaryType).

## Supported Data Types

- StringType with collation support (supports trim collation)
- BinaryType

Input and replace arguments must be of the same type (both string or both binary).

## Algorithm

- Validates that input and replace expressions have matching data types
- Uses position-based replacement starting from the specified 1-based position
- If length is not specified (defaults to -1), replaces from position to end
- Delegates actual calculation to `Overlay.calculate` static methods
- Supports both UTF8String operations for text and byte array operations for binary data
- Performs null-safe evaluation with null intolerance (returns null if any input is null)

## Partitioning Behavior
This expression does not affect partitioning:

- Preserves existing partitioning as it operates on individual row values
- Does not require shuffle operations
- Can be applied within partition boundaries

## Edge Cases

- Null handling: Expression is null-intolerant, returning null if any input argument is null
- Type mismatch: Fails type checking if input and replace have different data types
- Position bounds: Behavior for out-of-bounds positions is handled by the underlying calculate methods
- Negative length: When len parameter is -1 (default), replaces from position to end of input
- Empty inputs: Handled by the underlying UTF8String and byte array calculation methods

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which generates optimized bytecode that directly calls `org.apache.spark.sql.catalyst.expressions.Overlay.calculate` methods.

## Examples
```sql
-- Replace 'world' with 'Spark' starting at position 7
SELECT OVERLAY('Hello world' PLACING 'Spark' FROM 7 FOR 5) AS result;
-- Result: 'Hello Spark'

-- Replace from position without specifying length
SELECT OVERLAY('Hello world' PLACING 'Spark' FROM 7) AS result;
-- Result: 'Hello Spark'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(overlay(col("text"), lit("replacement"), lit(5), lit(3)))
df.select(overlay(col("text"), lit("replacement"), lit(5)))  // No length specified
```

## See Also

- `Substring` - Extract portions of strings
- `Replace` - Replace all occurrences of a substring
- `Concat` - Concatenate multiple strings
- String manipulation functions in `string_funcs` group