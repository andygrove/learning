# Decode

## Overview

The `Decode` expression implements a SQL CASE-like functionality that compares an input expression against multiple search values and returns the corresponding result value when a match is found. It serves as a runtime replaceable expression that gets transformed into a more optimized internal representation during query planning.

## Syntax

```sql
DECODE(expr, search1, result1 [, search2, result2] ... [, default])
```

```scala
// DataFrame API usage would be through SQL expression or functions
df.selectExpr("DECODE(column_name, 'value1', 'result1', 'value2', 'result2', 'default')")
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| expr | Expression | The input expression to be compared against search values |
| search | Expression | Search value(s) to match against the input expression |
| result | Expression | Result value(s) to return when corresponding search value matches |
| default | Expression (Optional) | Default value to return when no search values match |

## Return Type

The return type is determined by the common type of all result expressions and the optional default value. The expression performs type coercion to find a compatible return type among all possible result values.

## Supported Data Types

The `Decode` expression supports all Spark SQL data types for input and comparison:

- Primitive types (numeric, string, boolean, binary)
- Complex types (array, map, struct)
- Temporal types (date, timestamp)
- Null types

## Algorithm

- The expression takes a variable number of parameters in groups of (search, result) pairs
- During analysis, it gets transformed by `Decode.createExpr()` into an optimized internal representation
- The evaluation compares the input expression against each search value in sequence
- Returns the corresponding result value for the first matching search value
- If no search values match and a default is provided, returns the default value
- If no matches and no default, returns null

## Partitioning Behavior

The `Decode` expression preserves partitioning characteristics:

- Does not require data shuffling as it operates row-by-row
- Maintains existing partitioning scheme since it's a deterministic transformation
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- Null input expression matches only null search values using null-safe equality
- Empty parameter list results in compilation error
- Odd number of parameters (excluding first expression) uses the last parameter as default
- Type mismatches between result expressions trigger type coercion to a common type
- If type coercion fails, the expression may throw analysis exceptions

## Code Generation

As a `RuntimeReplaceable` expression, `Decode` itself does not generate code directly. Instead, it gets replaced during analysis phase by `Decode.createExpr()` with an optimized expression tree (likely a `CaseWhen` expression) that supports Tungsten code generation for efficient evaluation.

## Examples

```sql
-- Basic decode with default
SELECT DECODE(status, 'A', 'Active', 'I', 'Inactive', 'Unknown') FROM users;

-- Decode with numeric values
SELECT DECODE(grade, 1, 'Poor', 2, 'Fair', 3, 'Good', 4, 'Excellent') FROM reviews;

-- Decode without default (returns null for non-matches)
SELECT DECODE(category, 'TECH', 'Technology', 'BIZ', 'Business') FROM articles;
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions.expr

df.select(expr("DECODE(status_code, 200, 'OK', 404, 'Not Found', 500, 'Error', 'Unknown')"))

// Using with column references
df.selectExpr("DECODE(department, 'ENG', 'Engineering', 'MKT', 'Marketing', 'Other')")
```

## See Also

- `CaseWhen` - The underlying expression that `Decode` typically gets transformed into
- `When` - For building conditional expressions in DataFrame API
- `Coalesce` - For handling null values with fallback logic