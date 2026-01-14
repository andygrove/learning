# PosExplode

## Overview
PosExplode is a Spark Catalyst expression that explodes an array or map into multiple rows, with each row containing a position/index column followed by the element value. It extends the ExplodeBase class and enables position tracking by setting the position flag to true.

## Syntax
```sql
SELECT posexplode(array_column) FROM table_name
```

```scala
df.select(posexplode(col("array_column")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The array or map expression to be exploded |

## Return Type
Returns a struct containing two columns:

- Position column (IntegerType): Zero-based index of the element
- Value column: The actual element from the array/map (type depends on input)

## Supported Data Types

- ArrayType with any element type
- MapType with any key/value types

## Algorithm

- Iterates through each element in the input array or map
- Generates a new row for each element with its zero-based position
- For arrays: position is the array index, value is the array element
- For maps: position is the iteration order index, value is the key-value pair
- Maintains the position tracking flag set to true throughout evaluation

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve partitioning as it generates multiple output rows from single input rows
- Does not require shuffle as it operates row-by-row within each partition
- Output row count is unpredictable, depending on array/map sizes

## Edge Cases

- Null input: Returns no rows (empty result set)
- Empty array/map: Returns no rows
- Nested complex types: Only explodes the top-level array/map structure
- Large arrays: Position counter uses standard integer indexing (potential overflow with extremely large arrays)

## Code Generation
This expression inherits code generation capabilities from ExplodeBase. It supports Tungsten code generation for optimized runtime performance when processing large datasets.

## Examples
```sql
-- Example SQL usage
SELECT posexplode(array(10, 20, 30));
-- Returns:
-- 0  10
-- 1  20  
-- 2  30

SELECT posexplode(map('a', 1, 'b', 2));
-- Returns:
-- 0  {"key": "a", "value": 1}
-- 1  {"key": "b", "value": 2}
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._

df.select(posexplode(col("items")))
  .toDF("pos", "item")
  
// With column renaming
df.select(posexplode(col("array_col")).as(Seq("position", "value")))
```

## See Also

- Explode: Similar functionality without position information
- ExplodeBase: Parent class providing core explosion functionality
- Inline: For exploding arrays of structs into columns