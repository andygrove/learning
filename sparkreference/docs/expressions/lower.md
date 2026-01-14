# Lower

## Overview
The `Lower` expression converts all characters in a string to lowercase using appropriate collation rules. It supports various string collations and can optionally use ICU (International Components for Unicode) libraries for UTF8_BINARY collation instead of JVM's default case mappings.

## Syntax
```sql
LOWER(str)
lower(str)
```

```scala
// DataFrame API
col("column_name").lower()
lower(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | StringType | The input string expression to convert to lowercase |

## Return Type
`StringType` with the same collation as the input string.

## Supported Data Types
Supports `StringType` with any collation (UTF8_BINARY, UTF8_LCASE, UNICODE, etc.).

## Algorithm

- Extracts the collation ID from the input StringType to determine locale-specific case conversion rules
- Checks the `spark.sql.icuCaseMappingsEnabled` configuration to decide whether to use ICU or JVM case mappings for UTF8_BINARY collation
- Delegates the actual lowercase conversion to `CollationSupport.Lower.exec()` which handles collation-aware case mapping
- Preserves the original string's collation in the result
- Uses lazy evaluation for collation ID extraction and ICU flag determination

## Partitioning Behavior
This expression preserves partitioning since it operates on individual string values without changing data distribution:

- Does not require shuffle operations
- Maintains existing partition boundaries
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns `null` if input is `null` (null-intolerant behavior)
- **Empty string**: Returns empty string unchanged
- **Unicode characters**: Properly handles Unicode case conversion based on collation rules
- **Locale-specific cases**: Handles special cases like Turkish dotted/dotless i based on collation
- **Non-string types**: Only accepts StringType inputs, type checking occurs during analysis

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which generates optimized Java code using `CollationSupport.Lower.genCode()` for better performance in compiled execution paths.

## Examples
```sql
-- Basic lowercase conversion
SELECT LOWER('SparkSQL');
-- Result: sparksql

-- With mixed case and numbers
SELECT LOWER('Hello World 123');
-- Result: hello world 123

-- Null handling
SELECT LOWER(NULL);
-- Result: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(lower(col("name")))
df.select(col("description").lower())

// With column alias
df.select(lower(col("title")).alias("lowercase_title"))
```

## See Also

- `Upper` - Converts strings to uppercase
- `InitCap` - Converts strings to title case
- String collation functions for locale-specific string operations