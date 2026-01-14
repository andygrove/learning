# Collate

## Overview
The `Collate` expression marks a given expression with a specified collation without modifying the input data. This is a pass-through function that only updates type metadata to associate collation information with string data.

## Syntax
```sql
COLLATE(expression, collation)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expression | StringTypeWithCollation | The input expression to be marked with collation |
| collation | AnyDataType | The collation specification to apply to the expression |

## Return Type
Returns the same data type as the collation parameter, which contains the collation metadata.

## Supported Data Types

- String types with collation support (including trim collation support)
- The collation parameter can be of any data type

## Algorithm

- Evaluates the child expression without any modification to the actual data
- Passes through the result value unchanged during evaluation
- Updates only the type metadata to include collation information
- Uses simple passthrough for code generation without custom logic
- Maintains the foldable property of the child expression

## Partitioning Behavior
This expression preserves partitioning behavior since it's a metadata-only operation:

- Does not affect data distribution or partitioning
- No shuffle operations are required
- Maintains the same partitioning as the input expression

## Edge Cases

- Null values are passed through unchanged from the child expression
- Empty strings maintain their empty state with updated collation metadata
- The expression inherits the foldable behavior from its child expression
- Evaluation behavior is identical to the child expression since no data transformation occurs

## Code Generation
This expression supports Tungsten code generation through simple passthrough. It uses `child.genCode(ctx)` directly and explicitly throws an error if `doGenCode` is called, indicating it relies entirely on the child's code generation.

## Examples
```sql
-- Apply UTF8_BINARY collation to a string column
SELECT COLLATE(name, 'UTF8_BINARY') FROM users;

-- Mark a string literal with specific collation
SELECT COLLATE('Hello World', 'UTF8_LCASE') AS greeting;
```

```scala
// DataFrame API usage with collate function
import org.apache.spark.sql.functions._
df.select(collate(col("name"), lit("UTF8_BINARY")))

// Using in column expressions
df.withColumn("collated_name", collate(col("name"), lit("UTF8_LCASE")))
```

## See Also

- String collation functions
- Type casting expressions
- Metadata manipulation expressions