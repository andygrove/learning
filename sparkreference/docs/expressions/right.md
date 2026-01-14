# Right

## Overview
The `Right` expression extracts a specified number of characters from the right side of a string. It is implemented as a `RuntimeReplaceable` expression that transforms into conditional logic using `Substring` operations during query planning.

## Syntax
```sql
RIGHT(str, len)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("RIGHT(column_name, length)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | String | The input string from which to extract characters |
| len | Integer | The number of characters to extract from the right side |

## Return Type
Returns a `StringType` with the same collation as the input string.

## Supported Data Types

- **Input string**: `StringTypeWithCollation` (supports trim collation)
- **Length parameter**: `IntegerType`

## Algorithm
The expression is transformed at runtime into the following conditional logic:

- If the input string is null, return null
- If the length parameter is less than or equal to 0, return an empty string
- Otherwise, use `Substring` with a negative offset (`UnaryMinus(len)`) to extract from the right
- The `Substring` operation calculates the starting position from the end of the string
- Implicit type casting is applied to ensure type compatibility

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffle as it operates on individual rows
- Maintains the same partitioning scheme as the input DataFrame
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null input**: Returns null when the input string is null
- **Zero or negative length**: Returns empty string (`UTF8String.EMPTY_UTF8`) when len ≤ 0
- **Length greater than string length**: Returns the entire string when requested length exceeds string length
- **Empty string input**: Returns empty string regardless of length parameter
- **Type coercion**: Automatically casts compatible types through `ImplicitCastInputTypes`

## Code Generation
This expression supports Tungsten code generation through its replacement mechanism:

- Transforms into `If`, `Substring`, and `UnaryMinus` expressions at planning time
- The replacement expressions support whole-stage code generation
- Benefits from optimized UTF-8 string operations in generated code

## Examples
```sql
-- Extract last 3 characters
SELECT RIGHT('Hello World', 3); -- Returns 'rld'

-- Handle edge cases
SELECT RIGHT('abc', 0);    -- Returns ''
SELECT RIGHT('abc', -1);   -- Returns ''
SELECT RIGHT('abc', 10);   -- Returns 'abc'
SELECT RIGHT(NULL, 3);     -- Returns NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("RIGHT(name, 3)"))
df.select(expr("RIGHT(description, 5)").as("suffix"))

// With column references
df.select(expr("RIGHT(text_column, length_column)"))
```

## See Also

- `Left` - Extract characters from the left side of a string
- `Substring` - Extract characters from any position in a string  
- `Length` - Get the length of a string
- `Trim` - Remove whitespace from strings