# Stack

## Overview
The `Stack` expression is a table-generating function that transposes multiple columns into rows. It takes a number `n` and a series of expressions, then creates `n` rows by stacking the expressions vertically, with each row containing a subset of the input expressions as columns.

## Syntax
```sql
stack(n, expr1, expr2, ..., exprk)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("stack(3, 'A', 1, 'B', 2, 'C', 3) as (col0, col1)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| n | IntegerType | The number of rows to generate (must be foldable and > 0) |
| expr1, expr2, ... | Any | Variable number of expressions to stack into rows |

## Return Type
Returns a `StructType` with fields named `col0`, `col1`, etc. The number of columns is calculated as `ceil((total_expressions - 1) / n)`. Each column's data type is determined from the first non-null expression in that column position.

## Supported Data Types

- First argument (`n`): Must be `IntegerType` and foldable (constant)
- Remaining arguments: Any data type, but corresponding column positions across rows must have compatible types

## Algorithm

- Validates that the first argument is a positive integer constant
- Calculates the number of output columns as `ceil((children.length - 1) / numRows)`
- Groups the input expressions into rows, filling each row with `numFields` consecutive expressions
- Generates `numRows` output rows, padding with null values if insufficient expressions are provided
- Each output row is represented as an `InternalRow` with the calculated number of fields

## Partitioning Behavior
The `Stack` expression is a generator function that:

- Does not preserve partitioning as it transforms the structure of data
- Does not require shuffle as it operates row-by-row within partitions
- Each input row can generate multiple output rows independently

## Edge Cases

- **Null handling**: Null expressions are preserved as null values in the output columns
- **Insufficient expressions**: If fewer expressions are provided than needed to fill all rows and columns, missing positions are filled with null values  
- **Type mismatch**: All expressions that map to the same output column position must have the same data type
- **Invalid row count**: The first argument must be a positive integer, otherwise a `VALUE_OUT_OF_RANGE` error is thrown
- **Non-foldable n**: The row count parameter must be a compile-time constant

## Code Generation
Supports Tungsten code generation when `numRows <= 50`. For larger row counts, falls back to interpreted evaluation. The generated code creates an array of `InternalRow` objects and wraps them in a `mutable.ArraySeq`.

## Examples
```sql
-- Transform 6 values into 3 rows with 2 columns each
SELECT stack(3, 'A', 1, 'B', 2, 'C', 3) as (letter, number);
-- Result:
-- letter | number
-- A      | 1
-- B      | 2  
-- C      | 3

-- With insufficient values (padded with nulls)
SELECT stack(2, 'X', 10, 'Y') as (col0, col1);
-- Result:
-- col0 | col1
-- X    | 10
-- Y    | NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("stack(2, name, age, city, population) as (attribute, value)"))
  .show()
```

## See Also

- `explode()` - Explodes arrays or maps into multiple rows
- `posexplode()` - Similar to explode but includes position information
- `lateral view` - SQL construct often used with table-generating functions