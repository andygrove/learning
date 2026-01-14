# Collation

## Overview
The `Collation` expression returns the fully qualified collation name of a string expression. This is a runtime-replaceable expression that extracts the collation information from a StringType and converts it to its human-readable name format.

## Syntax
```sql
COLLATION(string_expr)
```

```scala
// DataFrame API
col("column_name").collation()
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| string_expr | String with collation | The string expression whose collation name should be returned |

## Return Type
Returns a `StringType` containing the fully qualified collation name (e.g., "SYSTEM.BUILTIN.UTF8_BINARY").

## Supported Data Types

- StringType with any collation (supports trim collation)

## Algorithm

- Extracts the collationId from the input StringType's metadata
- Resolves the collationId to its fully qualified name using CollationFactory
- Returns the collation name as a string literal
- Expression is replaced at runtime with a Literal containing the collation name
- No actual runtime evaluation occurs since this is a RuntimeReplaceable expression

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning since it's replaced with a literal at runtime
- Does not require shuffle operations
- The replacement literal is constant across all partitions

## Edge Cases

- Null handling: Follows standard null propagation rules - null input produces null output
- Empty string input: Returns the collation name of the empty string (still has collation metadata)
- Invalid collation: Should not occur as StringType always has a valid collationId
- The expression supports trim collation, allowing operations on strings that may be trimmed

## Code Generation
This expression supports code generation through its RuntimeReplaceable nature:

- At planning time, the expression is replaced with a Literal
- The Literal supports full code generation (Tungsten)
- No interpreted fallback needed since replacement is a simple constant

## Examples
```sql
-- Get collation of a string literal
SELECT COLLATION('hello');
-- Returns: SYSTEM.BUILTIN.UTF8_BINARY

-- Get collation of a column
SELECT COLLATION(name) FROM users;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("name").collation().as("name_collation"))

// With explicit collation
df.select(collation(col("description")).as("desc_collation"))
```

## See Also

- StringType collation support
- CollationFactory for collation management
- String functions that respect collation settings