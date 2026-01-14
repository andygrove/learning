# ToCharacter

## Overview
The `ToCharacter` expression converts decimal numbers to formatted string representations using a specified format pattern. It implements the `to_char` function that formats numeric values according to Oracle-style number formatting patterns with locale-aware formatting rules.

## Syntax
```sql
to_char(decimal_value, format_string)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("to_char(decimal_column, 'format_pattern')"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| decimal_value | DecimalType | The decimal number to be formatted |
| format_string | StringType | The format pattern string (must be a foldable/constant expression) |

## Return Type
Returns `StringType` - a formatted string representation of the input decimal number.

## Supported Data Types
- **Input**: DecimalType for the numeric value, StringType with collation support for the format pattern
- **Output**: StringType with default string-producing expression behavior
- The format string supports trim collation operations

## Algorithm
- The format string is parsed at initialization time using `ToNumberParser` with uppercase locale conversion
- Input validation ensures the format pattern is a compile-time constant (foldable expression)
- During evaluation, the decimal input is converted using the pre-compiled number formatter
- Null inputs in either argument result in null output (null-intolerant behavior)
- The formatter applies Oracle-style number formatting rules to generate the string output

## Partitioning Behavior
- **Preserves partitioning**: Yes, this is a row-level transformation that doesn't change data distribution
- **Requires shuffle**: No, operates independently on each row within partitions
- Safe for use in partition-preserving operations and can be pushed down in optimization

## Edge Cases
- **Null handling**: Returns null if either the decimal value or format string is null (nullIntolerant = true)
- **Invalid format**: Compilation fails if the format string contains invalid patterns
- **Non-foldable format**: Throws `DataTypeMismatch` error if format string is not a constant expression
- **Runtime format validation**: Additional format validation occurs during the type checking phase
- **Locale handling**: Format patterns are converted to uppercase using ROOT locale for consistency

## Code Generation
Supports Tungsten code generation with optimized performance:
- Pre-compiles the format parser as a referenced object in the generated code
- Generates efficient null-checking logic that avoids unnecessary formatting calls
- Directly calls the formatter's format method in generated code without interpretation overhead
- Uses `CodeGenerator.javaType` and `CodeGenerator.defaultValue` for type-safe code generation

## Examples
```sql
-- Format decimal with currency pattern
SELECT to_char(1234.56, '$999,999.99') as formatted_currency;

-- Format with leading zeros
SELECT to_char(42.7, '000.000') as padded_number;

-- Scientific notation formatting
SELECT to_char(0.00123, '9.999EEEE') as scientific;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Format currency values
df.select(expr("to_char(price, '$999,999.99')").alias("formatted_price"))

// Format with specific decimal places
df.select(expr("to_char(decimal_col, '999.999')").alias("formatted_decimal"))
```

## See Also
- `ToNumber` - Converts formatted strings back to numeric values
- `FormatNumber` - Simpler numeric formatting with fixed patterns
- `Cast` - Basic type conversion operations
- `DecimalType` expressions for decimal arithmetic operations