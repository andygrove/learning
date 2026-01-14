# Mask

## Overview
The Mask expression masks characters in string input by replacing different character types (uppercase, lowercase, digits, and other characters) with specified replacement characters. It provides data obfuscation functionality while preserving the original string structure and length.

## Syntax
```sql
mask(input, upperChar, lowerChar, digitChar, otherChar)
mask(input, upperChar, lowerChar, digitChar)
mask(input, upperChar, lowerChar)
mask(input, upperChar)
mask(input)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| input | String | The input string to be masked |
| upperChar | String | Single character to replace uppercase letters (default: 'X') |
| lowerChar | String | Single character to replace lowercase letters (default: 'x') |
| digitChar | String | Single character to replace digits (default: 'n') |
| otherChar | String | Single character to replace other characters (default: null - no replacement) |

## Return Type
Returns the same data type as the input expression (typically StringType with collation support).

## Supported Data Types

- Input: StringTypeWithCollation (supports trim collation)

- Replacement characters: StringTypeWithCollation (supports trim collation)

- All replacement character expressions must be foldable (compile-time constants)

- Each replacement character must be exactly one character long

## Algorithm

- Evaluates all child expressions to get the input string and replacement characters

- Delegates actual transformation logic to `Mask.transformInput()` utility method

- Processes each character in the input string based on its type (uppercase, lowercase, digit, other)

- Replaces characters according to the specified replacement mappings

- Preserves original string length and non-alphabetic/non-digit characters (unless otherChar is specified)

## Partitioning Behavior

- Preserves partitioning as it operates on individual rows without requiring data movement

- Does not require shuffle operations

- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- Returns null if the input string is null (only first child determines nullability)

- Non-foldable replacement character expressions cause compilation errors

- Replacement characters with length != 1 cause validation errors

- Empty input strings return empty strings

- When otherChar is null (default), other characters remain unchanged

- All replacement character expressions are evaluated even if input is null (for validation)

## Code Generation
Supports Tungsten code generation through `doGenCode()` method. Generated code calls the static `Mask.transformInput()` method directly, enabling efficient execution without interpreter overhead.

## Examples
```sql
-- Basic masking with defaults
SELECT mask('Hello123!') -- Returns 'Xxxxx999!'

-- Custom replacement characters  
SELECT mask('Hello123!', 'U', 'l', '#', '*') -- Returns 'Ullll###*'

-- Partial customization
SELECT mask('Hello123!', 'A', 'b') -- Returns 'Abbbb999!'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic masking
df.select(expr("mask(name)"))

// Custom masking
df.select(expr("mask(ssn, 'X', 'x', '#', '-')"))

// Using constructors programmatically
val maskExpr = new Mask(col("input").expr)
```

## See Also

- String manipulation functions (substring, regexp_replace)

- Data obfuscation and anonymization functions

- QuinaryExpression base class for five-argument expressions