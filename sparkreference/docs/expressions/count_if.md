# CountIf

## Overview
CountIf is an aggregate function that counts the number of rows where a boolean condition evaluates to true. It is implemented as a runtime replaceable aggregate that internally translates to a Count expression with null handling for false values.

## Syntax
```sql
COUNT_IF(condition)
```

```scala
// DataFrame API
df.agg(count_if(col("condition")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| condition | Boolean | A boolean expression to evaluate for each row |

## Return Type
Returns a `LongType` (64-bit integer) representing the count of rows where the condition is true.

## Supported Data Types

- Input: Boolean expressions only
- Implicit casting is supported through `ImplicitCastInputTypes` trait

## Algorithm

- Evaluates the boolean condition for each row in the group
- Converts false values to null using `NullIf(child, Literal.FalseLiteral)`
- Applies standard `Count` aggregation which ignores null values
- Returns the final count as a long integer
- Uses runtime replacement pattern for efficient execution

## Partitioning Behavior
As an aggregate function, CountIf affects partitioning behavior:

- Does not preserve partitioning as it reduces multiple rows to a single count value
- May require shuffle operations when used with GROUP BY clauses
- Supports partial aggregation for improved performance in distributed environments

## Edge Cases

- **Null handling**: Null values in the condition are treated as false and do not contribute to the count
- **Empty input**: Returns 0 when applied to an empty dataset or when no rows match the condition  
- **All false conditions**: Returns 0 when all condition evaluations are false
- **Type coercion**: Non-boolean inputs are implicitly cast to boolean when possible

## Code Generation
This expression supports Spark's Tungsten code generation through its runtime replacement mechanism. The underlying `Count` and `NullIf` expressions both support code generation, ensuring efficient compiled execution.

## Examples
```sql
-- Count rows where col is NULL
SELECT COUNT_IF(col IS NULL) FROM VALUES (NULL), (0), (1), (2), (3) AS tab(col);
-- Returns: 1

-- Count rows with positive values
SELECT COUNT_IF(value > 0) FROM sales_data;

-- Count with grouping
SELECT region, COUNT_IF(sales > 1000) FROM sales_data GROUP BY region;
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Count null values
df.agg(count_if(col("column_name").isNull))

// Count with condition
df.agg(count_if(col("sales") > 1000))

// With groupBy
df.groupBy("region").agg(count_if(col("active") === true))
```

## See Also

- `Count` - Standard count aggregate function
- `Sum` - For summing numeric conditions instead of counting
- `NullIf` - The internal null handling mechanism used by CountIf
- `Case/When` - For more complex conditional logic