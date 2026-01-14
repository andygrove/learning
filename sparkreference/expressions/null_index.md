# NullIndex

## Overview
`NullIndex` is a window function expression that tracks consecutive null values in a sequence, resetting the counter to 0 when a non-null value is encountered. This expression is specifically designed for the Pandas API on Spark to provide pandas-compatible null indexing behavior within window operations.

## Syntax
```sql
null_index(column_expression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| input | Expression | The input expression to analyze for null values |

## Return Type
`IntegerType` - Returns integer values representing the index of consecutive nulls.

## Supported Data Types
All data types are supported as input since the expression only checks for null values using `IsNull`, which works with any data type.

## Algorithm
- Maintains an internal counter (`index`) initialized to 0
- For each row in the window frame:
  - If the input value is null, increment the counter by 1
  - If the input value is non-null, reset the counter to 0
- Returns the current counter value for each row

## Partitioning Behavior
As an `AggregateWindowFunction`, this expression:
- Operates within window partitions defined by the window specification
- Does not require shuffle if used with existing partitioning that matches the window partition columns
- Maintains state independently across different window partitions

## Edge Cases
- **Null handling**: Null values are the primary focus - they increment the internal counter
- **Non-null values**: Any non-null value (including empty strings, zeros, false) resets the counter to 0
- **Empty partitions**: Would not produce any output rows
- **Integer overflow**: Theoretical possibility if consecutive nulls exceed `Integer.MAX_VALUE`, but would require extremely large datasets

## Code Generation
This expression extends `AggregateWindowFunction` and uses standard Catalyst expressions (`If`, `IsNull`, `Literal`) in its `updateExpressions`, which should support Tungsten code generation for the underlying operations.

## Examples
```sql
-- Example with window function
SELECT 
  value,
  null_index(value) OVER (ORDER BY id) as null_idx
FROM table_name
```

```scala
// DataFrame API usage (Pandas API on Spark context)
import org.apache.spark.sql.expressions.Window

val windowSpec = Window.orderBy("id")
df.select($"value", 
  expr("null_index(value)").over(windowSpec).as("null_idx"))
```

**Example Input/Output:**
```
Input:  null, 1, 2, 3, null, null, null, 5, null, null
Output: 1,    0, 0, 0, 1,    2,    3,    0, 1,    2
```

## See Also
- `Lag` - For accessing previous row values in windows
- `Lead` - For accessing subsequent row values in windows  
- `IsNull` - The underlying null checking expression used internally
- Other `AggregateWindowFunction` implementations for similar stateful window operations