# EndsWith

## Overview
The EndsWith expression is a string predicate that determines whether a given string ends with a specified suffix. It supports collation-aware string matching and implements both interpreted and code-generated execution paths for optimal performance.

## Syntax
```sql
-- SQL function syntax
ENDSWITH(string_expr, suffix_expr)

-- Alternative pattern matching
string_expr LIKE '%suffix'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.filter(col("column_name").endsWith("suffix"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The string expression to be checked |
| right | Expression | The suffix expression to match against |

## Return Type
Boolean - returns `true` if the left string ends with the right string, `false` otherwise.

## Supported Data Types

- StringType with non-CSAI (Case-Sensitive, Accent-Insensitive) collations
- Supports trim collations
- Both arguments must be string-compatible types

## Algorithm

- Extracts UTF8String representations from both left and right expressions
- Delegates the actual comparison logic to `CollationSupport.EndsWith.exec()` method
- Uses the configured `collationId` to perform collation-aware string matching
- Returns boolean result based on suffix matching
- Handles collation-specific character equivalences during comparison

## Partitioning Behavior
- **Preserves partitioning**: This expression does not affect data partitioning as it's a row-level predicate
- **No shuffle required**: Operates independently on each row without requiring data movement
- Can be pushed down as a filter predicate in query optimization

## Edge Cases

- **Null handling**: If either left or right expression evaluates to null, the result is null
- **Empty suffix**: An empty string suffix will match any string (returns true)
- **Empty string**: An empty left string will only match an empty suffix
- **Collation sensitivity**: Results depend on the configured collation rules for case and accent handling
- **Unicode handling**: Properly handles multi-byte UTF-8 characters according to collation rules

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method. It uses `CollationSupport.EndsWith.genCode()` to generate optimized bytecode, falling back to interpreted mode only when code generation is disabled or fails.

## Examples
```sql
-- Basic usage
SELECT ENDSWITH('Hello World', 'World') AS result;
-- Returns: true

-- Case sensitivity depends on collation
SELECT ENDSWITH('Hello World', 'world') AS result;
-- Returns: depends on collation settings

-- With null values
SELECT ENDSWITH('Hello', NULL) AS result;
-- Returns: null

-- Empty suffix
SELECT ENDSWITH('Hello', '') AS result;
-- Returns: true
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Filter rows where column ends with suffix
df.filter(col("name").endsWith("son"))

// Select with endsWith condition
df.select(col("*"), col("email").endsWith(".com").as("is_com_email"))

// Complex condition
df.filter(col("filename").endsWith(".txt") || col("filename").endsWith(".csv"))
```

## See Also

- StartsWith - Check if string starts with prefix
- Contains - Check if string contains substring
- StringPredicate - Base class for string comparison predicates
- CollationSupport - Collation-aware string operations