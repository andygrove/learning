# Contains

## Overview
The `Contains` expression is a string predicate that determines whether the left string expression contains the right string expression as a substring. It extends `StringPredicate` and supports collation-aware string matching for internationalization scenarios.

## Syntax
```sql
-- SQL syntax
string_expr1 CONTAINS string_expr2
-- or using LIKE pattern
string_expr1 LIKE '%substring%'
```

```scala
// DataFrame API usage
col("column1").contains(col("column2"))
col("column1").contains("substring")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The string expression to search within |
| right | Expression | The substring expression to search for |

## Return Type
Boolean - returns `true` if the left string contains the right string as a substring, `false` otherwise.

## Supported Data Types

- StringType with non-CSAI collation support
- Supports trim collation variations
- Both arguments must be string-compatible types
- Collation-aware matching based on the expression's collationId

## Algorithm

- Evaluates both left and right expressions to UTF8String values
- Delegates substring matching to `CollationSupport.Contains.exec()` with the appropriate collation
- Uses collation-specific comparison rules for internationalized string matching
- Returns boolean result indicating whether substring is found
- Handles collation sensitivity based on configured collationId

## Partitioning Behavior

- Preserves partitioning as it operates on individual rows without data movement
- Does not require shuffle operations
- Can be pushed down to data sources for predicate pushdown optimization
- Maintains data locality during execution

## Edge Cases

- Returns `null` if either left or right expression evaluates to `null`
- Empty right string (`""`) returns `true` for any non-null left string
- Empty left string (`""`) returns `false` for any non-empty right string
- Case sensitivity depends on the configured collation settings
- Collation-specific edge cases handled by `CollationSupport.Contains.exec()`

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method. It uses `CollationSupport.Contains.genCode()` to generate optimized bytecode for runtime execution, avoiding interpreted mode overhead.

## Examples
```sql
-- Check if product name contains keyword
SELECT * FROM products WHERE product_name CONTAINS 'smartphone';

-- Using LIKE equivalent
SELECT * FROM products WHERE product_name LIKE '%smartphone%';
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Check if description contains specific text
df.filter(col("description").contains("error"))

// Dynamic substring search
df.filter(col("title").contains(col("search_term")))

// Case with literal string
df.select(col("text").contains("pattern").as("has_pattern"))
```

## See Also

- `StartsWith` - checks if string starts with prefix
- `EndsWith` - checks if string ends with suffix
- `Like` - pattern matching with wildcards
- `RLike` - regular expression matching
- `StringPredicate` - base class for string comparison predicates