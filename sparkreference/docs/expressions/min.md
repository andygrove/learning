# Min

## Overview
Min is a declarative aggregate expression that computes the minimum value of a column across all rows in a group or dataset. It extends DeclarativeAggregate and implements a unary aggregate function that finds the smallest value according to the natural ordering of the input data type.

## Syntax
```sql
MIN(column_expression)
```

```scala
// DataFrame API
df.agg(min("column_name"))
df.select(min($"column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression whose minimum value will be computed |

## Return Type
Returns the same data type as the input expression (`child.dataType`). The result is always nullable since the minimum of an empty set is null.

## Supported Data Types
All data types that support ordering operations, as validated by `TypeUtils.checkForOrderingExpr`. This includes:

- Numeric types (IntegerType, LongType, DoubleType, FloatType, DecimalType, etc.)
- String types (StringType)
- Date and timestamp types (DateType, TimestampType)
- Binary types that support comparison
- Any other types with defined ordering semantics

## Algorithm
The Min aggregate is implemented as a DeclarativeAggregate with the following evaluation strategy:

- Initializes the aggregate buffer with a null value of the input data type
- For each input row, updates the minimum using the `least(current_min, new_value)` function
- During merge operations (for distributed computation), combines partial minimums using `least(left_min, right_min)`
- Returns the final minimum value stored in the aggregate buffer
- Uses Catalyst's built-in `least` function for efficient comparison operations

## Partitioning Behavior
As an aggregate function, Min has specific partitioning requirements:

- Does not preserve input partitioning since it reduces multiple rows to a single result
- May require a shuffle operation when used in distributed environments to collect all values for global minimum computation
- In grouped aggregations, can be computed per partition first, then merged across partitions

## Edge Cases

- **Null handling**: Null values are ignored during minimum computation; if all values are null, returns null
- **Empty input**: Returns null when applied to an empty dataset or group
- **Single value**: Returns that single value even if it's null (following SQL semantics)
- **Mixed nulls and values**: Nulls are ignored, minimum is computed only from non-null values
- **NaN handling**: For floating-point types, NaN values follow IEEE 754 comparison semantics

## Code Generation
This expression uses DeclarativeAggregate framework, which supports Catalyst code generation (Tungsten). The underlying `least` function calls are code-generated for optimal performance, avoiding interpreted expression evaluation in tight loops.

## Examples
```sql
-- Basic minimum computation
SELECT MIN(col) FROM VALUES (10), (-1), (20) AS tab(col);
-- Result: -1

-- Grouped minimum
SELECT category, MIN(price) FROM products GROUP BY category;

-- With null handling
SELECT MIN(col) FROM VALUES (10), (NULL), (5) AS tab(col);
-- Result: 5
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.min

// Simple aggregation
df.agg(min("salary"))

// Grouped aggregation  
df.groupBy("department").agg(min("salary"))

// With column expressions
df.select(min($"price" * 0.9))
```

## See Also

- Max - computes maximum value
- least - computes minimum across multiple columns in a single row
- first - gets first value in a group
- DeclarativeAggregate - base class for aggregate expressions