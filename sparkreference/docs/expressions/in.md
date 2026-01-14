# In

## Overview
The `In` expression evaluates whether a given value matches any value in a specified list of expressions. It returns true if the value is found in the list, false if not found and no nulls are present, or null if the value is null or if any list item is null but no match is found.

## Syntax
```sql
value IN (expr1, expr2, ..., exprN)
```

```scala
// DataFrame API
col("column_name").isin(value1, value2, value3)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| value | Expression | The expression to search for in the list |
| list | Seq[Expression] | A sequence of expressions to compare against the value |

## Return Type
Returns `BooleanType` - true, false, or null depending on the match result and null handling logic.

## Supported Data Types
Supports any data type that has ordering semantics defined. All expressions (value and list items) must have structurally equivalent data types, ignoring nullability. The data type must support ordering operations as verified by `TypeUtils.checkForOrderingExpr`.

## Algorithm

- If the list is empty, returns false (under current behavior) or null/false based on legacy configuration
- Evaluates the target value expression first - if null, returns null
- Iterates through each list expression, evaluating them one by one
- Uses data type-specific ordering comparison (`ordering.equiv`) to check for matches
- Returns true immediately upon finding the first match
- Tracks if any null values are encountered during list evaluation - returns null if no match found but nulls were present

## Partitioning Behavior
This expression does not directly affect partitioning behavior as it operates on individual rows. It preserves existing partitioning schemes and does not require data shuffling.

## Edge Cases

- **Null value**: If the target value is null, the result is always null regardless of list contents
- **Empty list**: Returns false under current behavior; legacy behavior returns null if value is null, false otherwise (controlled by `SQLConf.legacyNullInEmptyBehavior`)
- **Null in list**: If any list item evaluates to null and no match is found, returns null instead of false
- **Mixed nulls**: Evaluation continues through the entire list even if nulls are encountered, allowing for potential matches after null values

## Code Generation
Supports full Tungsten code generation with optimized evaluation logic. The generated code uses a state machine approach with three states: `HAS_NULL` (-1), `NOT_MATCHED` (0), and `MATCHED` (1). For large lists, expressions are split across multiple generated functions to avoid JVM method size limits.

## Examples
```sql
-- Basic usage
SELECT * FROM table WHERE col IN (1, 2, 3);

-- With null handling
SELECT col IN (1, NULL, 3) FROM table; -- Returns null if col is not 1 or 3

-- Empty list
SELECT col IN () FROM table; -- Always returns false
```

```scala
// DataFrame API usage
df.filter(col("status").isin("active", "pending"))

// With variables
val validIds = Seq(1, 2, 3, 4)
df.filter(col("id").isin(validIds: _*))
```

## See Also

- `InSet` - Optimized version for literal values that can be converted to a HashSet
- `EqualTo` - For single value equality comparison
- `Or` - Alternative approach using multiple equality conditions