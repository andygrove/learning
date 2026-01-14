# Conv

## Overview
The `Conv` expression converts a number from one base (radix) to another base. It takes a string representation of a number in a source base and converts it to a string representation in a target base, supporting bases from 2 to 36.

## Syntax
```sql
conv(num, from_base, to_base)
```

```scala
conv(col("num"), lit(from_base), lit(to_base))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| num | String | The number to convert (as a string) |
| from_base | Integer | The source base/radix (2-36) |
| to_base | Integer | The target base/radix (2-36) |

## Return Type
Returns a string data type with the same collation as the input number string.

## Supported Data Types

- **Input**: String (with collation support, including trim-supporting collations), Integer, Integer
- **Output**: String (preserves input string collation)

## Algorithm

- Trims whitespace from the input number string using UTF8String.trim()
- Converts the trimmed string bytes to the source base representation
- Performs base conversion using the NumberConverter utility class
- Returns the result as a string in the target base
- Supports ANSI mode for stricter error handling during conversion
- Uses query context for error reporting when ANSI mode is enabled

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows without requiring data redistribution:

- Does not require shuffle operations
- Can be pushed down to individual partitions
- Maintains partition boundaries during execution

## Edge Cases

- **Null handling**: Returns null if any input argument is null (null intolerant)
- **Empty input**: Empty strings are handled by the NumberConverter utility
- **Invalid base**: Bases outside the 2-36 range may cause conversion failures
- **Invalid numbers**: Numbers that cannot be parsed in the source base return null in non-ANSI mode
- **ANSI mode**: When enabled, invalid conversions throw exceptions instead of returning null
- **Whitespace**: Leading and trailing whitespace is automatically trimmed from the input number

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method:

- Generates optimized bytecode using `nullSafeCodeGen`
- Uses direct calls to `NumberConverter.convert()` in generated code
- Includes null checking and ANSI mode handling in generated code

## Examples
```sql
-- Convert decimal 15 to hexadecimal (base 16)
SELECT conv('15', 10, 16);
-- Returns: 'F'

-- Convert binary to decimal
SELECT conv('1111', 2, 10);
-- Returns: '15'

-- Convert hexadecimal to octal
SELECT conv('FF', 16, 8);
-- Returns: '377'

-- Example from source code
SELECT conv(-10, 16, -10);
-- Returns: '-16'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(conv(col("hex_value"), lit(16), lit(10)).as("decimal_value"))

// Convert multiple columns
df.select(
  conv(col("binary_col"), lit(2), lit(10)).as("decimal"),
  conv(col("decimal_col"), lit(10), lit(16)).as("hex")
)
```

## See Also

- Mathematical functions: `hex()`, `unhex()`, `bin()`
- String functions for number formatting
- `NumberConverter` utility class for base conversion implementation