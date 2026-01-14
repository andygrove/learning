# Greatest

## Overview
The `Greatest` expression returns the largest value among all provided arguments. It performs element-wise comparison using the data type's natural ordering to determine the maximum value across multiple expressions.

## Syntax
```sql
SELECT greatest(expr1, expr2, ..., exprN)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.greatest
df.select(greatest(col("col1"), col("col2"), col("col3")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | Variable number of expressions (minimum 2) to compare for finding the maximum value |

## Return Type
Returns the same data type as the input expressions after type coercion. All input expressions must be coercible to a common type.

## Supported Data Types
All data types that support ordering comparison:

- Numeric types (Byte, Short, Integer, Long, Float, Double, Decimal)
- String types
- Date and Timestamp types
- Boolean type
- Binary type (lexicographic ordering)

## Algorithm

- Performs left-fold operation across all child expressions
- Evaluates each expression against the current input row
- Compares non-null values using the data type's interpreted ordering
- Updates the result when a larger value is found
- Preserves null values according to null handling rules

## Partitioning Behavior
The `Greatest` expression does not affect partitioning:

- Preserves existing partitioning as it operates row-by-row
- Does not require data shuffle since it's a per-row computation
- Can be pushed down to individual partitions independently

## Edge Cases

- **Null handling**: If all arguments are null, returns null. If some arguments are null, ignores null values and returns the greatest non-null value
- **Single argument**: Throws `QueryCompilationErrors.wrongNumArgsError` - requires more than one argument
- **Type mismatch**: Throws `DataTypeMismatch` error if input types cannot be coerced to a common type
- **Non-orderable types**: Validation fails for complex types that don't support ordering (arrays, maps, structs without natural ordering)

## Code Generation
This expression supports Tungsten code generation with optimizations:

- Generates efficient Java code for comparison operations
- Uses `ctx.reassignIfGreater` for optimized comparison logic
- Implements expression splitting for handling large numbers of arguments
- Falls back to interpreted mode only if code generation context limits are exceeded

## Examples
```sql
-- Basic numeric comparison
SELECT greatest(10, 9, 2, 4, 3);
-- Returns: 10

-- String comparison
SELECT greatest('apple', 'banana', 'cherry');
-- Returns: 'cherry'

-- With null values
SELECT greatest(1, NULL, 3, NULL, 2);
-- Returns: 3

-- Date comparison
SELECT greatest('2023-01-01', '2023-12-31', '2023-06-15');
-- Returns: '2023-12-31'
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.greatest

// Numeric columns
df.select(greatest($"price1", $"price2", $"price3"))

// Mixed with literals
df.select(greatest($"score", lit(100)))

// String comparison
df.select(greatest($"name1", $"name2", $"name3"))
```

## See Also

- `Least` - Returns the smallest value among arguments
- `Max` - Aggregate function for finding maximum in a group
- `Coalesce` - Returns first non-null value
- `Case/When` - Conditional expressions for complex comparisons