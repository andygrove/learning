# BoolOr

## Overview
BoolOr is an aggregate function that returns true if at least one of the input boolean values is true, otherwise returns false. It is implemented as a runtime-replaceable aggregate that delegates to the Max function internally, treating true as the maximum boolean value.

## Syntax
```sql
bool_or(column)
SELECT bool_or(col) FROM table_name;
```

```scala
// DataFrame API
df.agg(expr("bool_or(column_name)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The boolean expression or column to aggregate |

## Return Type
Returns `BooleanType` - either true, false, or null.

## Supported Data Types

- BooleanType only
- Input values are implicitly cast to boolean if needed due to ImplicitCastInputTypes trait

## Algorithm

- Internally replaced with Max(child) aggregate function at runtime
- Leverages the fact that true > false in boolean ordering
- Max function handles the aggregation logic for finding the maximum boolean value
- Null values are ignored during aggregation (standard Max behavior)
- Returns null only if all input values are null

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve partitioning as it's an aggregate function
- Requires shuffle for global aggregation across partitions
- Partial aggregation can be performed within partitions before shuffle

## Edge Cases

- **Null handling**: Null values are ignored; function returns false if all non-null values are false
- **All nulls**: Returns null if all input values are null
- **Empty input**: Returns null for empty input sets
- **Mixed nulls**: `bool_or(true, null, false)` returns true; `bool_or(false, null, false)` returns false

## Code Generation
This expression supports Tungsten code generation through its replacement with Max aggregate function, which has codegen support for boolean types.

## Examples
```sql
-- Basic usage
SELECT bool_or(col) FROM VALUES (false), (false), (NULL) AS tab(col);
-- Result: false

-- Mixed true/false
SELECT bool_or(col) FROM VALUES (true), (false), (false) AS tab(col);
-- Result: true

-- All nulls
SELECT bool_or(col) FROM VALUES (NULL), (NULL) AS tab(col);
-- Result: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.agg(expr("bool_or(is_active)")).show()

// Groupby usage
df.groupBy("category").agg(expr("bool_or(has_discount)")).show()
```

## See Also

- BoolAnd - logical AND aggregate function
- Max - underlying implementation for boolean maximum
- Any - similar logical OR semantics in some SQL dialects