# Apache Spark Catalyst Number Format Expressions

## ToNumberBase

### Overview
ToNumberBase is an abstract base class that implements number parsing functionality for converting string representations to decimal values based on format patterns. It serves as the foundation for both `to_number` and `try_to_number` functions, with the key difference being error handling behavior.

### Syntax
```sql
-- Implemented by concrete subclasses
TO_NUMBER(expr, fmt)
TRY_TO_NUMBER(expr, fmt)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression (String) | The input string expression to be converted |
| right | Expression (String) | The format pattern string (must be foldable/constant) |
| errorOnFail | Boolean | Internal flag determining whether to throw exceptions or return null on parsing failures |

### Return Type
Returns `DecimalType` - either the parsed decimal type determined by the format pattern, or `DecimalType.USER_DEFAULT` if the formatter is null.

### Supported Data Types
- **Input**: `StringTypeWithCollation` (supports trim collation for both arguments)
- **Output**: `DecimalType` with precision and scale determined by the format pattern

### Algorithm
- Format pattern is parsed once during initialization using `ToNumberParser` with uppercase normalization
- Input validation ensures the format expression is foldable (constant)
- String parsing occurs through `ToNumberParser.parse()` method
- Decimal type inference is performed based on format pattern analysis
- Null propagation follows null-intolerant semantics (any null input produces null output)

### Partitioning Behavior
- **Preserves partitioning**: Yes, as this is a deterministic row-level transformation
- **Requires shuffle**: No, operates independently on each row
- **Partition-wise operation**: Safe for partition-wise operations

### Edge Cases
- **Null handling**: Null-intolerant - any null input (string or format) returns null
- **Invalid format**: Non-foldable format expressions cause compilation errors
- **Parse failures**: Behavior depends on `errorOnFail` flag (exception vs null)
- **Empty format**: Null format string passes type checking but results in null formatter

### Code Generation
Supports Tungsten code generation with optimized execution:
- Format parser is stored as a reference object in the generated code context
- Avoids repeated format parsing during execution
- Generated code includes inline null checking and value extraction

---

## ToNumber

### Overview
ToNumber converts string expressions to decimal values using a specified format pattern. It throws exceptions when the input string fails to match the format pattern, making it suitable for scenarios where data quality issues should halt processing.

### Syntax
```sql
TO_NUMBER(expr, fmt)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | String | The input string to convert to a number |
| fmt | String | Format pattern (must be constant) |

### Return Type
`DecimalType` with precision and scale inferred from the format pattern.

### Supported Data Types
- **Input**: String expressions with collation support
- **Format patterns**: Supports 0, 9, D/., G/,, $, S/MI, PR format characters

### Algorithm
- Inherits parsing logic from `ToNumberBase` with `errorOnFail = true`
- Uses `ToNumberParser` for format validation and string-to-decimal conversion
- Performs compile-time validation of format pattern syntax
- Runtime parsing with exception propagation on failures

### Partitioning Behavior
- **Preserves partitioning**: Yes, deterministic row-level operation
- **Requires shuffle**: No
- **Failure behavior**: Exceptions can terminate partition processing

### Edge Cases
- **Null handling**: Returns null for null inputs
- **Parse failures**: Throws runtime exceptions
- **Invalid format characters**: Compilation-time errors
- **Grouping separator mismatches**: Runtime parsing exceptions

### Code Generation
Full Tungsten code generation support with exception handling in generated code.

### Examples
```sql
-- Basic digit conversion
SELECT TO_NUMBER('454', '999');
-- Result: 454

-- Decimal formatting
SELECT TO_NUMBER('454.00', '000.00');
-- Result: 454.00

-- Grouping separators
SELECT TO_NUMBER('12,454', '99,999');
-- Result: 12454

-- Currency symbol
SELECT TO_NUMBER('$78.12', '$99.99');
-- Result: 78.12

-- Signed numbers
SELECT TO_NUMBER('12,454.8-', '99,999.9S');
-- Result: -12454.8
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("TO_NUMBER(amount_str, '999,999.99')"))
```

---

## TryToNumber

### Overview
TryToNumber provides the same string-to-decimal conversion functionality as ToNumber but returns NULL instead of throwing exceptions when parsing fails. This makes it suitable for ETL scenarios where data quality issues should be handled gracefully.

### Syntax
```sql
TRY_TO_NUMBER(expr, fmt)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | String | The input string to convert to a number |
| fmt | String | Format pattern (must be constant) |

### Return Type
`DecimalType` (nullable) with precision and scale inferred from the format pattern.

### Supported Data Types
Identical to ToNumber - string inputs with comprehensive format pattern support.

### Algorithm
- Inherits from `ToNumberBase` with `errorOnFail = false`
- Same parsing logic as ToNumber but with null return on failures
- Always nullable due to potential parse failures

### Partitioning Behavior
- **Preserves partitioning**: Yes
- **Requires shuffle**: No
- **Failure behavior**: Graceful null return, no partition interruption

### Edge Cases
- **Null handling**: Returns null for null inputs
- **Parse failures**: Returns null instead of throwing exceptions
- **Invalid characters**: Returns null for unparseable input
- **Format mismatches**: Returns null rather than failing

### Code Generation
Identical code generation to ToNumber with different error handling in the parser.

### Examples
```sql
-- Valid conversion
SELECT TRY_TO_NUMBER('454', '999');
-- Result: 454

-- Invalid input returns NULL
SELECT TRY_TO_NUMBER('abc', '999');
-- Result: NULL

-- Partial matches return NULL
SELECT TRY_TO_NUMBER('12.34.56', '99.99');
-- Result: NULL
```

---

## ToCharacter

### Overview
ToCharacter converts decimal values to formatted string representations using number format patterns. It provides the inverse functionality of the ToNumber family, transforming numeric data into human-readable strings with specific formatting requirements.

### Syntax
```sql
TO_CHAR(expr, format)
-- Built via ToCharacterBuilder for different input types
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Decimal | The numeric expression to format |
| format | String | Format pattern string (must be foldable) |

### Return Type
`StringType` - formatted string representation of the input decimal.

### Supported Data Types
- **Input**: `DecimalType` expressions
- **Format**: String expressions with collation support
- **Output**: String with default collation

### Algorithm
- Uses same `ToNumberParser` class but calls `format()` instead of `parse()`
- Format pattern parsing and validation during expression initialization
- Decimal-to-string conversion with padding, grouping, and sign formatting
- Left-padding with zeros or spaces based on format pattern rules

### Partitioning Behavior
- **Preserves partitioning**: Yes, deterministic transformation
- **Requires shuffle**: No
- **String output**: May affect downstream string-based partitioning schemes

### Edge Cases
- **Null handling**: Null-intolerant, returns null for null inputs
- **Precision overflow**: Behavior depends on format pattern constraints
- **Zero padding**: Applied based on format pattern position and leading characters
- **Sign formatting**: Supports multiple sign representation modes (S, MI, PR)

### Code Generation
Full code generation support using reference objects for the number formatter.

### Examples
```sql
-- Basic formatting
SELECT TO_CHAR(454, '999');
-- Result: '454'

-- Decimal places
SELECT TO_CHAR(454.00, '000D00');
-- Result: '454.00'

-- Grouping separators
SELECT TO_CHAR(12454, '99G999');
-- Result: '12,454'

-- Currency formatting
SELECT TO_CHAR(78.12, '$99.99');
-- Result: '$78.12'

-- Signed formatting
SELECT TO_CHAR(-12454.8, '99G999D9S');
-- Result: '12,454.8-'
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("TO_CHAR(amount, '$999,999.99')"))
```

---

## ToCharacterBuilder

### Overview
ToCharacterBuilder is an expression builder that creates appropriate conversion expressions based on input data types. It handles routing to different formatting implementations for datetime, binary, and numeric data types.

### Syntax
```sql
TO_CHAR(expr, format) -- Dispatches to appropriate implementation
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expressions | Seq[Expression] | Must contain exactly 2 expressions: input and format |

### Return Type
Returns different expression types based on input:
- `DateFormatClass` for datetime types
- `Base64`, `Hex`, or `Decode` for binary types  
- `ToCharacter` for numeric types

### Supported Data Types
- **DatetimeType**: Routes to datetime formatting
- **BinaryType**: Supports base64, hex, utf-8 encoding formats
- **Other types**: Routes to `ToCharacter` for numeric formatting

### Algorithm
- Validates exactly 2 arguments provided
- Pattern matches on first expression's data type
- For binary types, validates format is foldable and matches supported encodings
- Creates appropriate expression instance based on type routing

### Partitioning Behavior
Depends on the created expression type - generally preserves partitioning for deterministic conversions.

### Edge Cases
- **Wrong argument count**: Throws compilation error for non-2 argument calls
- **Invalid binary format**: Throws error for unsupported binary format strings
- **Null format for binary**: Throws null argument error
- **Non-foldable binary format**: Throws non-foldable argument error

### Code Generation
Not applicable - this is a builder that creates other expressions.

### Examples
```sql
-- Numeric formatting (creates ToCharacter)
SELECT TO_CHAR(123.45, '999.99');

-- Date formatting (creates DateFormatClass) 
SELECT TO_CHAR(DATE '2016-04-08', 'y');

-- Binary base64 (creates Base64)
SELECT TO_CHAR(X'537061726b2053514c', 'base64');

-- Binary hex (creates Hex)
SELECT TO_CHAR(X'537061726b2053514c', 'hex');

-- Binary UTF-8 (creates Decode)
SELECT TO_CHAR(ENCODE('abc', 'utf-8'), 'utf-8');
```

## See Also
- `Cast` expressions for basic type conversions
- `DateFormatClass` for datetime string formatting  
- `Base64`, `Hex`, `Decode` for binary data encoding
- `ToNumberParser` utility class for format pattern handling