# Spark Catalyst Collection Operations Reference

## Size

### Overview
The `Size` expression returns the total number of elements in an array or map. It provides configurable behavior for null inputs based on legacy compatibility settings, returning either -1 or null for null inputs depending on the `spark.sql.legacy.sizeOfNull` configuration.

### Syntax
```sql
SIZE(expr)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `expr` | ArrayType or MapType | The array or map whose size is to be calculated |
| `legacySizeOfNull` | Boolean (internal) | Controls null handling behavior - when true, returns -1 for null inputs; when false, returns null |

### Return Type
`IntegerType` - Returns an integer representing the number of elements.

### Supported Data Types
- `ArrayType` - Arrays of any element type
- `MapType` - Maps with any key-value types

### Algorithm
- Evaluates the child expression to get the array or map data
- For null inputs: returns -1 if `legacySizeOfNull` is true, otherwise returns null
- For ArrayType: calls `ArrayData.numElements()` to get element count
- For MapType: calls `MapData.numElements()` to get key-value pair count
- Throws `UnsupportedOperandTypeForSizeFunctionError` for unsupported types

### Partitioning Behavior
- Preserves partitioning as it's a simple unary transformation
- No shuffle required since it operates on individual rows
- Can be pushed down to data sources in many cases

### Edge Cases
- **Null handling**: Behavior depends on `legacySizeOfNull` setting
  - Legacy mode (`legacySizeOfNull = true`): returns -1 for null input
  - Standard mode (`legacySizeOfNull = false`): returns null for null input
- **Empty collections**: Returns 0 for empty arrays or maps
- **Nested structures**: Only counts top-level elements, not nested elements

### Code Generation
Supports full code generation (Tungsten). Generated code includes:
- Fast path for legacy null handling with `FalseLiteral` for `isNull`
- Direct method calls to `numElements()` on the data structures
- Optimized null checks and branching logic

### Examples
```sql
-- Array examples
SELECT SIZE(array('b', 'd', 'c', 'a'));  -- Returns: 4
SELECT SIZE(array());                     -- Returns: 0
SELECT SIZE(NULL);                        -- Returns: NULL (standard mode) or -1 (legacy mode)

-- Map examples  
SELECT SIZE(map('a', 1, 'b', 2));         -- Returns: 2
SELECT SIZE(map());                       -- Returns: 0
```

```scala
// DataFrame API usage
df.select(size(col("array_column")))
df.select(size(col("map_column")))
```

### See Also
- `ArraySize` - Array-specific size function
- `MapKeys` - Extract keys from map
- `MapValues` - Extract values from map

---

## ArraySize

### Overview
The `ArraySize` expression is a runtime-replaceable expression that specifically operates on arrays to return their size. It always returns null for null inputs, providing consistent null handling behavior regardless of legacy settings.

### Syntax
```sql
ARRAY_SIZE(array)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `array` | ArrayType | The array whose size is to be calculated |

### Return Type
`IntegerType` - Returns an integer representing the number of array elements.

### Supported Data Types
- `ArrayType` - Arrays of any element type with implicit casting support

### Algorithm
- Runtime replacement for `Size(child, legacySizeOfNull = false)`
- Delegates all evaluation logic to the underlying `Size` expression
- Enforces consistent null handling behavior

### Partitioning Behavior
- Preserves partitioning (same as `Size`)
- No shuffle required
- Supports predicate pushdown optimizations

### Edge Cases
- **Null handling**: Always returns null for null input (no legacy behavior)
- **Empty arrays**: Returns 0
- **Type validation**: Strict ArrayType input validation with helpful error messages

### Code Generation
Inherits code generation from the underlying `Size` expression with `legacySizeOfNull = false`.

### Examples
```sql
SELECT ARRAY_SIZE(array('b', 'd', 'c', 'a'));  -- Returns: 4
SELECT ARRAY_SIZE(array());                     -- Returns: 0
SELECT ARRAY_SIZE(NULL);                        -- Returns: NULL
```

### See Also
- `Size` - General size function for arrays and maps

---

## MapKeys

### Overview
The `MapKeys` expression extracts all keys from a map and returns them as an unordered array. The order of keys in the result is not guaranteed to be consistent across evaluations.

### Syntax
```sql
MAP_KEYS(map)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `map` | MapType | The map from which to extract keys |

### Return Type
`ArrayType` with element type matching the map's key type.

### Supported Data Types
- `MapType` - Maps with any key and value types

### Algorithm
- Validates input is MapType during analysis phase
- Calls `MapData.keyArray()` to extract the underlying key array
- Returns the key array directly without copying or reordering

### Partitioning Behavior
- Preserves partitioning as it's a unary transformation
- No shuffle required
- Output partitioning depends on input map distribution

### Edge Cases
- **Null handling**: Returns null for null map input (null intolerant)
- **Empty maps**: Returns empty array
- **Key ordering**: No guarantee on key order in result array
- **Duplicate keys**: Not applicable (maps have unique keys by definition)

### Code Generation
Generates efficient code using `nullSafeCodeGen`:
```java
ev.value = (input).keyArray();
```

### Examples
```sql
SELECT MAP_KEYS(map(1, 'a', 2, 'b'));     -- Returns: [1,2] (order not guaranteed)
SELECT MAP_KEYS(map());                    -- Returns: []
SELECT MAP_KEYS(NULL);                     -- Returns: NULL
```

### See Also
- `MapValues` - Extract values from map
- `MapEntries` - Extract key-value pairs as structs

---

## MapContainsKey

### Overview
The `MapContainsKey` expression checks if a map contains a specified key, returning a boolean result. It's implemented as a runtime-replaceable expression that delegates to `ArrayContains(MapKeys(map), key)`.

### Syntax
```sql
MAP_CONTAINS_KEY(map, key)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `map` | MapType | The map to search in |
| `key` | Same as map key type | The key to search for |

### Return Type
`BooleanType` - Returns true if the key exists, false otherwise.

### Supported Data Types
- Maps with any key type that supports ordering/comparison
- Automatic type coercion between map key type and search key type

### Algorithm
- Runtime replacement that expands to `ArrayContains(MapKeys(left), right)`
- Extracts map keys and performs array containment check
- Requires ordering support for the key type

### Partitioning Behavior
- Preserves partitioning
- No shuffle required for the operation itself
- Performance depends on map size and key distribution

### Edge Cases
- **Null handling**: Returns null if map is null or key is null
- **Type coercion**: Automatic widening of key types where possible
- **Ordering requirement**: Key type must support ordering operations
- **Empty maps**: Returns false for any key

### Code Generation
Inherits code generation from the underlying `ArrayContains` expression.

### Examples
```sql
SELECT MAP_CONTAINS_KEY(map(1, 'a', 2, 'b'), 1);    -- Returns: true
SELECT MAP_CONTAINS_KEY(map(1, 'a', 2, 'b'), 3);    -- Returns: false
SELECT MAP_CONTAINS_KEY(NULL, 1);                    -- Returns: NULL
```

### See Also
- `MapKeys` - Extract map keys
- `ArrayContains` - Underlying implementation

---

## ArraysZip

### Overview
The `ArraysZip` expression merges multiple arrays element-wise into an array of structs, where the N-th struct contains all N-th values from the input arrays. It handles arrays of different lengths by using null for missing elements.

### Syntax
```sql
ARRAYS_ZIP(array1, array2, ...)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `array1, array2, ...` | ArrayType | Variable number of arrays to zip together |
| `names` | Seq[Expression] (internal) | Field names for the resulting struct fields |

### Return Type
`ArrayType` containing `StructType` with fields corresponding to input arrays.

### Supported Data Types
- Any number of `ArrayType` inputs with any element types
- Automatic field naming based on input expression names

### Algorithm
- Determines the maximum length among all input arrays (biggestCardinality)
- Creates struct array with length equal to maximum input array length
- For each position i, creates struct with values from position i of each input array
- Uses null for missing elements when arrays have different lengths
- Returns null if any input array is null

### Partitioning Behavior
- Preserves partitioning as it's a row-wise transformation
- No shuffle required
- Output size depends on longest input array

### Edge Cases
- **Null arrays**: Returns null if any input array is null
- **Empty arrays**: Returns empty result array
- **Different lengths**: Shorter arrays contribute null values for missing positions
- **Field naming**: Uses expression names or defaults to positional names ("0", "1", etc.)

### Code Generation
Complex code generation with optimizations:
- Splits expressions to avoid large methods
- Efficient null checking and early termination
- Direct memory operations for better performance
- Separate handling for empty input case

### Examples
```sql
SELECT ARRAYS_ZIP(array(1, 2, 3), array(2, 3, 4));
-- Returns: [{"0":1,"1":2},{"0":2,"1":3},{"0":3,"1":4}]

SELECT ARRAYS_ZIP(array(1, 2), array(2, 3), array(3, 4));  
-- Returns: [{"0":1,"1":2,"2":3},{"0":2,"1":3,"2":4}]

SELECT ARRAYS_ZIP(array(1, 2), array('a'));
-- Returns: [{"0":1,"1":"a"},{"0":2,"1":null}]
```

### See Also
- Related array transformation functions

---

## MapValues

### Overview
The `MapValues` expression extracts all values from a map and returns them as an unordered array. The order of values corresponds to the order of keys but is not guaranteed to be consistent across evaluations.

### Syntax
```sql
MAP_VALUES(map)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `map` | MapType | The map from which to extract values |

### Return Type
`ArrayType` with element type matching the map's value type.

### Supported Data Types
- `MapType` - Maps with any key and value types

### Algorithm
- Validates input is MapType during analysis phase
- Calls `MapData.valueArray()` to extract the underlying value array
- Returns the value array directly without copying or reordering

### Partitioning Behavior
- Preserves partitioning as it's a unary transformation
- No shuffle required
- Output partitioning depends on input map distribution

### Edge Cases
- **Null handling**: Returns null for null map input (null intolerant)
- **Empty maps**: Returns empty array
- **Value ordering**: Order corresponds to key order but not guaranteed stable
- **Null values**: Preserves null values that exist in the map

### Code Generation
Generates efficient code using `nullSafeCodeGen`:
```java
ev.value = (input).valueArray();
```

### Examples
```sql
SELECT MAP_VALUES(map(1, 'a', 2, 'b'));   -- Returns: ["a","b"] (order not guaranteed)
SELECT MAP_VALUES(map());                  -- Returns: []
SELECT MAP_VALUES(NULL);                   -- Returns: NULL
```

### See Also
- `MapKeys` - Extract keys from map
- `MapEntries` - Extract key-value pairs as structs

---

## SortArray

### Overview
The `SortArray` expression sorts an input array in ascending or descending order according to the natural ordering of elements. It handles null elements by placing them at the beginning (ascending) or end (descending) of the result.

### Syntax
```sql
SORT_ARRAY(array[, ascendingOrder])
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `array` | ArrayType | The array to be sorted |
| `ascendingOrder` | BooleanType | Optional flag for sort direction (default: true) |

### Return Type
`ArrayType` with the same element type as input array.

### Supported Data Types
- Arrays with any orderable element type (numeric, string, date, timestamp, etc.)
- Element type must support `RowOrdering.isOrderable`

### Algorithm
- Validates element type supports ordering operations
- Converts ArrayData to object array for sorting
- Uses `java.util.Arrays.parallelSort` with custom comparator
- Null handling: nulls first for ascending, nulls last for descending
- Special handling for NaN values in float/double (NaN > non-NaN)

### Partitioning Behavior
- Preserves partitioning (operates on individual arrays within rows)
- No shuffle required
- Can benefit from predicate pushdown in some cases

### Edge Cases
- **Null elements**: Placed at beginning (ascending) or end (descending)
- **NaN handling**: For float/double, NaN is considered greater than any non-NaN value
- **Empty arrays**: Returns empty array unchanged
- **Single element**: Returns array unchanged
- **Foldable requirement**: `ascendingOrder` must be a compile-time constant

### Code Generation
Sophisticated code generation with optimizations:
- Fast path for non-null primitive arrays using native Java sorting
- Custom comparator generation for complex types
- Optimized null handling in generated comparators
- Falls back to generic object array sorting when necessary

### Examples
```sql
SELECT SORT_ARRAY(array('b', 'd', null, 'c', 'a'), true);   
-- Returns: [null,"a","b","c","d"]

SELECT SORT_ARRAY(array('b', 'd', null, 'c', 'a'), false);  
-- Returns: ["d","c","b","a",null]

SELECT SORT_ARRAY(array(3, 1, 4, 1, 5));  
-- Returns: [1,1,3,4,5]
```

### See Also
- `Reverse` - Reverse array elements
- `Shuffle` - Random permutation of array elements