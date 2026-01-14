# Inline

## Overview
The `Inline` expression explodes an array of structs into a table, where each struct in the array becomes a separate row. It flattens the array structure by expanding each struct element into individual rows with the struct's fields as columns.

## Syntax
```sql
-- SQL syntax
INLINE(array_of_structs)
```

```scala
// DataFrame API usage
df.select(inline(col("array_column")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | An expression that evaluates to an array of struct types |

## Return Type
Returns a collection of `InternalRow` objects, where each row has the schema of the struct type contained in the input array.

## Supported Data Types

- Input: `ArrayType` containing `StructType` elements (with or without nulls)
- Output: Individual rows with the schema matching the struct fields

## Algorithm

- Evaluates the child expression to get an `ArrayData` object
- Iterates through each element in the array (from 0 to `numElements() - 1`)
- For each element, extracts the struct using `getStruct(i, numFields)`
- Returns each struct as a separate row, using `generatorNullRow` for null structs
- Returns empty collection (`Nil`) if the input array is null

## Partitioning Behavior

- Does not preserve partitioning as it generates multiple output rows from a single input row
- May require data redistribution depending on downstream operations
- The number of output rows per input row depends on the array size

## Edge Cases

- **Null array input**: Returns empty collection (`Nil`)
- **Null struct elements**: Replaced with `generatorNullRow` (a row with all null values)
- **Empty array**: Returns empty collection
- **Nullable struct fields**: Handled based on the array's `containsNull` property - if true, the output schema is made nullable using `st.asNullable`

## Code Generation
Supports Tungsten code generation through the `doGenCode` method, though the implementation delegates to the child expression's code generation.

## Examples
```sql
-- Example SQL usage
SELECT INLINE(array_of_people) 
FROM (
  SELECT array(
    struct('John' as name, 25 as age),
    struct('Jane' as name, 30 as age)
  ) as array_of_people
)
-- Results in two rows: (John, 25) and (Jane, 30)
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._

val df = Seq(
  Array(("John", 25), ("Jane", 30))
).toDF("people")

df.select(inline(col("people")))
// Results in DataFrame with columns: _1 (String), _2 (Int)
```

## See Also

- `Explode` - for exploding arrays into rows without struct expansion
- `PosExplode` - for exploding with position information
- `CollectionGenerator` - parent trait for collection-based generators