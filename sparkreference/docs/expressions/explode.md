# Explode

## Overview
The `Explode` expression transforms an array or map into multiple rows, creating one row for each element in the input collection. Unlike `PosExplode`, it does not include positional information and focuses solely on extracting the values from the collection.

## Syntax
```sql
SELECT explode(array_or_map_column) FROM table_name
```

```scala
df.select(explode(col("array_or_map_column")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The array or map expression to be exploded into multiple rows |

## Return Type
- For arrays: Returns the element type of the input array
- For maps: Returns a struct with key-value pairs

## Supported Data Types

- Array types (ArrayType) with any element type
- Map types (MapType) with any key-value types

## Algorithm

- Inherits core explosion logic from `ExplodeBase` parent class
- Sets `position` flag to `false` to exclude positional information from output
- Processes each element in the input collection sequentially
- Generates one output row per collection element
- Uses copy-based child replacement for expression tree transformations

## Partitioning Behavior
- Does not preserve partitioning as it fundamentally changes row cardinality
- May require shuffle operations when used in distributed computations
- Output rows are distributed based on the partitioning of input rows containing the collections

## Edge Cases

- Null input collections result in no output rows (empty result)
- Empty arrays or maps produce no output rows
- Null elements within arrays are preserved as null values in output rows
- Map entries with null keys or values are preserved in the output

## Code Generation
Inherits code generation capabilities from the `ExplodeBase` parent class, supporting Tungsten code generation for optimized execution when possible.

## Examples
```sql
-- Array explosion
SELECT explode(array(10, 20, 30)) AS value;
-- Result:
-- 10
-- 20
-- 30

-- Map explosion  
SELECT explode(map('a', 1, 'b', 2)) AS (key, value);
-- Result:
-- a  1
-- b  2
```

```scala
// Array explosion
val df = Seq(Array(1, 2, 3), Array(4, 5)).toDF("numbers")
df.select(explode(col("numbers"))).show()

// Map explosion
val mapDf = Seq(Map("x" -> 10, "y" -> 20)).toDF("pairs") 
mapDf.select(explode(col("pairs"))).show()
```

## See Also
- `PosExplode` - Explode with positional information
- `Inline` - Explode arrays of structs into columns
- `ExplodeBase` - Parent class containing core explosion logic