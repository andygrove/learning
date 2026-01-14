# TryElementAt

## Overview
`TryElementAt` is a Spark Catalyst expression that safely extracts an element from an array or map at a specified index or key position. Unlike the standard `element_at` function, this expression returns null instead of throwing an error when the index is out of bounds or the key doesn't exist.

## Syntax
```sql
try_element_at(collection, index_or_key)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| collection | Array or Map | The source collection (array or map) to extract from |
| index_or_key | Integer or matching key type | For arrays: 1-based index position. For maps: the key to look up |

## Return Type
Returns the element type of the input collection (array element type or map value type). Returns null if the position/key is invalid.

## Supported Data Types

- **Arrays**: Any array type with integer index access
- **Maps**: Any map type with key-based access
- **Index/Key types**: Integer for arrays, any valid key type for maps

## Algorithm

- Creates a `RuntimeReplaceable` wrapper around the core `ElementAt` expression
- Sets `failOnError = false` to enable safe access without exceptions  
- Delegates actual evaluation to `ElementAt` with null fallback behavior
- Uses inheritance of analysis rules from the underlying `ElementAt` implementation
- Maintains the same evaluation logic as `ElementAt` but with error suppression

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffle as it operates on individual rows
- Maintains existing partitioning scheme since it's a row-level transformation
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null collection**: Returns null when the input collection is null
- **Null index/key**: Returns null when the index or key parameter is null
- **Out of bounds**: Returns null for array indices outside valid range (arrays are 1-based)
- **Missing keys**: Returns null when map key doesn't exist
- **Zero/negative indices**: Returns null for invalid array positions

## Code Generation
This expression supports Catalyst code generation through its `RuntimeReplaceable` nature. The underlying `ElementAt` expression handles Tungsten code generation, providing optimized bytecode for the actual element access logic.

## Examples
```sql
-- Array access examples
SELECT try_element_at(array(1, 2, 3), 2);  -- Returns 2
SELECT try_element_at(array(1, 2, 3), 5);  -- Returns null (out of bounds)

-- Map access example  
SELECT try_element_at(map(1, 'a', 2, 'b'), 2);  -- Returns 'b'
SELECT try_element_at(map(1, 'a', 2, 'b'), 3);  -- Returns null (key not found)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("try_element_at(array_col, 2)"))
df.select(expr("try_element_at(map_col, 'key')"))
```

## See Also

- `element_at` - Similar function that throws errors on invalid access
- `array` - Creates arrays for use with try_element_at
- `map` - Creates maps for use with try_element_at
- `size` - Gets collection size for bounds checking