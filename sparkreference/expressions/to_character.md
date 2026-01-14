# ToCharacter

## Overview

The `ToCharacter` expression converts numeric decimal values to formatted string representations using a specified format pattern. It provides precise control over number formatting including decimal places, thousands separators, currency symbols, and sign handling, throwing an exception if the conversion fails.

## Syntax

```sql
TO_CHAR(expr, format)
```

```scala
// DataFrame API
df.select(expr("to_char(column_name, format_string)"))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `expr` | DecimalType | The numeric decimal value to be converted to a string |
| `format` | StringType | The format pattern specifying how the number should be formatted (must be foldable/constant) |

## Return Type

Returns `StringType` - a formatted string representation of the input decimal value.

## Supported Data Types

- **Input Expression**: DecimalType only
- **Format Pattern**: StringType with collation support (must be a compile-time constant)

## Algorithm

- Validates that the format parameter is foldable (compile-time constant) during analysis phase
- Creates a `ToNumberParser` instance with the uppercase format string and error-on-fail mode enabled
- Converts the input decimal value to a formatted string using the parser's `format()` method
- Supports format characters: '0', '9' (digits), '.', 'D' (decimal point), ',', 'G' (grouping), '$' (currency), 'S', 'MI' (signs), 'PR' (negative brackets)
- Throws exceptions for invalid format patterns or conversion failures

## Partitioning Behavior

- **Preserves Partitioning**: Yes, this is a row-level transformation that doesn't require data movement
- **Shuffle Required**: No, operates independently on each row within partitions

## Edge Cases

- **Null Handling**: Returns null if either input expression or format pattern evaluates to null (null intolerant)
- **Invalid Format**: Throws `QueryCompilationErrors` if format string is invalid during analysis
- **Non-foldable Format**: Compilation error if format parameter is not a constant expression
- **Null Format at Runtime**: Returns null if the format parser cannot be initialized
- **Conversion Failures**: Throws runtime exceptions when formatting fails (errorOnFail = true)

## Code Generation

Supports Tungsten code generation with optimized bytecode. The generated code:
- Pre-initializes the `ToNumberParser` as a reference object in the code generation context
- Performs null checks before invoking the formatter
- Directly calls the parser's `format()` method on the decimal input

## Examples

```sql
-- Basic number formatting
SELECT TO_CHAR(454, '999');
-- Result: '454'

-- Decimal formatting with padding
SELECT TO_CHAR(454.00, '000D00');
-- Result: '454.00'

-- Thousands separator
SELECT TO_CHAR(12454, '99G999');
-- Result: '12,454'

-- Currency formatting
SELECT TO_CHAR(78.12, '$99.99');
-- Result: '$78.12'

-- Negative number with trailing sign
SELECT TO_CHAR(-12454.8, '99G999D9S');
-- Result: '12,454.8-'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("to_char(amount, '$999,999.99')").as("formatted_amount"))

// With column references
df.select(expr("to_char(price * quantity, '999,999.00')").as("total"))
```

## See Also

- `ToNumber` - Parses formatted strings back to decimal values
- `TryToNumber` - Similar to ToNumber but returns null on parse failures
- `ToCharacterBuilder` - Expression builder that handles multiple data types including datetime and binary
- `Cast` - General type conversion expression
- `DateFormatClass` - For datetime formatting