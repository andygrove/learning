# StringTrimRight

## Overview
StringTrimRight is a Spark Catalyst expression that removes trailing whitespace or specified characters from the right side of a string. It supports both single-argument mode (trimming whitespace) and two-argument mode (trimming specific characters) with collation-aware string operations.

## Syntax
```sql
RTRIM(string_expr)
RTRIM(string_expr, trim_chars)
```

```scala
// DataFrame API
rtrim(col("column_name"))
rtrim(col("column_name"), lit("chars_to_trim"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| srcStr | Expression | The source string expression to trim characters from |
| trimStr | Option[Expression] | Optional expression specifying characters to trim. If None, trims whitespace |

## Return Type
UTF8String - Returns a string with trailing characters removed from the input string.

## Supported Data Types
StringTypeNonCSAICollation with trim collation support - accepts string types that support collation-aware trimming operations but excludes case-sensitive accent-insensitive collations.

## Algorithm

- Evaluates the source string expression to get UTF8String input
- If trimStr is None, delegates to CollationSupport.StringTrimRight.exec(srcString) for whitespace trimming
- If trimStr is provided, evaluates the trim string and calls CollationSupport.StringTrimRight.exec(srcString, trimString, collationId)
- Uses collation-aware string operations to handle different character encodings and locale-specific rules
- Returns the trimmed UTF8String result

## Partitioning Behavior
This expression preserves partitioning:

- Does not require shuffle operations as it operates on individual rows
- Maintains existing data distribution since it's a row-level transformation
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- Null handling: If srcStr evaluates to null, returns null
- Empty string: Returns empty string unchanged
- Null trimStr: Treated as None, falls back to whitespace trimming
- Empty trimStr: No characters are trimmed, returns original string
- Collation-specific behavior applies for character matching and comparison

## Code Generation
This expression supports Catalyst code generation through the String2TrimExpression base class, enabling efficient Tungsten code generation for improved runtime performance.

## Examples
```sql
-- Trim trailing whitespace
SELECT RTRIM('  hello world  ') AS result;
-- Result: '  hello world'

-- Trim specific trailing characters
SELECT RTRIM('xxxhelloxxx', 'x') AS result;
-- Result: 'xxxhello'
```

```scala
// DataFrame API - trim whitespace
df.select(rtrim(col("text_column")))

// DataFrame API - trim specific characters
df.select(rtrim(col("text_column"), lit("xyz")))
```

## See Also

- StringTrimLeft - for trimming leading characters
- StringTrim - for trimming both leading and trailing characters
- String2TrimExpression - base class for all trim operations