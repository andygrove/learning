# StringLPad

## Overview
StringLPad is a Spark Catalyst expression that performs left-padding on a string by adding characters to the beginning until it reaches a specified length. This expression is typically used to format strings to a fixed width by prepending a padding character or string.

## Syntax
```sql
LPAD(str, len, pad)
```

```scala
lpad(str, len, pad)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | Expression | The input string to be padded |
| len | Expression | The target length of the resulting string |
| pad | Expression | The padding string to be added to the left |

## Return Type
Returns a `StringType` containing the left-padded string.

## Supported Data Types

- **str**: String types (StringType)

- **len**: Integer types (IntegerType, LongType, etc.)

- **pad**: String types (StringType)

## Algorithm

- Evaluates the input string, target length, and padding string expressions

- If the input string length is already greater than or equal to the target length, truncates from the right to match the target length

- If the input string is shorter than the target length, calculates the number of characters needed for padding

- Repeats the padding string as necessary to fill the required padding length

- Concatenates the padding with the original string to achieve the target length

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle as it operates on individual rows

- Maintains existing partitioning scheme since it's a deterministic row-level transformation

- Can be safely pushed down in query optimization

## Edge Cases

- **Null handling**: Returns null if any of the input arguments (str, len, or pad) is null

- **Empty string input**: Pads empty strings normally according to the specified length and padding

- **Zero or negative length**: Returns empty string when target length is zero or negative

- **Empty padding string**: Behavior depends on implementation - may return the original string truncated to target length

- **Padding longer than needed**: Truncates the repeated padding string to fit exactly the required padding length

## Code Generation
StringLPad typically supports Spark's Tungsten code generation for optimized execution, generating efficient Java bytecode for the padding logic rather than falling back to interpreted mode.

## Examples
```sql
-- Pad numbers with leading zeros
SELECT LPAD('123', 6, '0') AS padded_number;
-- Result: '000123'

-- Pad strings with spaces
SELECT LPAD('hello', 10, ' ') AS padded_string;
-- Result: '     hello'

-- Truncate if string is longer than target length
SELECT LPAD('verylongstring', 5, 'x') AS truncated;
-- Result: 'veryl'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.lpad

df.select(lpad(col("name"), 10, " ").as("padded_name"))

// Using string interpolation
df.selectExpr("lpad(product_id, 8, '0') as formatted_id")
```

## See Also

- **StringRPad**: Right-padding equivalent function

- **Length**: To determine current string length before padding

- **Substring**: For string truncation operations

- **Concat**: For general string concatenation operations