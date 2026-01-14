# StartsWith

## Overview
The `StartsWith` expression is a string predicate that determines whether a string value begins with a specified prefix. It extends the `StringPredicate` class and supports collation-aware string comparison for case-sensitive and case-insensitive matching.

## Syntax
```sql
string_expr LIKE 'prefix%'
STARTSWITH(string_expr, prefix)
```

```scala
// DataFrame API
col("column_name").startsWith("prefix")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The string expression to check |
| right | Expression | The prefix string expression to match against |

## Return Type
`BooleanType` - Returns `true` if the left string starts with the right string, `false` otherwise.

## Supported Data Types

- StringType with non-CSAI (Case-Sensitive Accent-Insensitive) collations
- Supports trim collation for string normalization
- Both arguments must be string-compatible types

## Algorithm

- Delegates string comparison to `CollationSupport.StartsWith.exec()` method
- Uses the expression's `collationId` for collation-aware comparison
- Performs UTF8String-based comparison for efficient string operations
- Handles collation rules including case sensitivity and accent handling
- Returns boolean result based on prefix matching logic

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning schemes
- Does not require data shuffle operations
- Can be applied as a filter predicate without repartitioning

## Edge Cases

- Null handling: If either argument is null, the result is null
- Empty string behavior: Empty prefix (`""`) returns `true` for any string
- Empty left string with non-empty prefix returns `false`
- Collation-specific edge cases depend on the configured collation rules
- Case sensitivity depends on the collation configuration

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method:

- Uses `CollationSupport.StartsWith.genCode()` for optimized code generation
- Falls back to interpreted mode if code generation fails
- Generates efficient bytecode for runtime string comparison

## Examples
```sql
-- Check if customer names start with 'John'
SELECT * FROM customers WHERE name LIKE 'John%';

-- Using STARTSWITH function (if available)
SELECT STARTSWITH(product_name, 'iPhone') FROM products;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Filter rows where column starts with prefix
df.filter(col("name").startsWith("John"))

// Select with startsWith condition
df.select(col("*")).where(col("product_name").startsWith("iPhone"))
```

## See Also

- `EndsWith` - Check if string ends with suffix
- `Contains` - Check if string contains substring  
- `StringPredicate` - Base class for string comparison expressions
- `CollationSupport` - Collation-aware string operations