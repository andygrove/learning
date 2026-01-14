# Chr

## Overview
The `Chr` expression converts a numeric value to its corresponding ASCII character representation. It takes a long integer input and returns a single-character string based on the lowest 8 bits of the input value, effectively implementing ASCII character code conversion.

## Syntax
```sql
CHR(numeric_expression)
```

```scala
chr(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Long | The numeric value to convert to an ASCII character (automatically cast to LongType) |

## Return Type
UTF8String - A single character string or empty string

## Supported Data Types

- Numeric types that can be implicitly cast to LongType

- The expression uses `ImplicitCastInputTypes` to automatically convert input to Long

## Algorithm

- Extract the input long value from the child expression

- If the input is negative, return an empty UTF8String

- If the lowest 8 bits equal zero (value & 0xFF == 0), return the MIN_VALUE character

- Otherwise, mask the input with 0xFF to get the lowest 8 bits and convert to character

- Convert the resulting character to a UTF8String

## Partitioning Behavior

- Preserves partitioning as it performs row-level transformation without requiring data movement

- Does not require shuffle operations

- Can be evaluated independently on each partition

## Edge Cases

- **Null handling**: Returns null if input is null (nullIntolerant = true)

- **Negative values**: Returns empty string for any negative input

- **Zero byte values**: Returns Character.MIN_VALUE when (input & 0xFF) == 0

- **Large values**: Only uses the lowest 8 bits, so values > 255 are truncated

- **Out of ASCII range**: Values are masked to 0-255 range using bitwise AND operation

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, generating optimized Java bytecode for runtime execution rather than falling back to interpreted mode.

## Examples
```sql
SELECT CHR(65) AS letter;  -- Returns 'A'
SELECT CHR(97) AS letter;  -- Returns 'a'
SELECT CHR(-1) AS letter;  -- Returns ''
SELECT CHR(321) AS letter; -- Returns 'A' (321 & 0xFF = 65)
```

```scala
import org.apache.spark.sql.functions.expr

df.select(expr("CHR(65)").as("letter"))
df.withColumn("ascii_char", expr("CHR(ascii_code_column)"))
```

## See Also

- ASCII - Convert character to numeric ASCII code
- CONCAT - String concatenation functions
- String manipulation expressions in Catalyst