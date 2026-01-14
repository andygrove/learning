# Size

## Overview
The `Size` expression returns the number of elements in an array or map. It supports both legacy and modern null handling behavior, where legacy mode returns -1 for null inputs while modern mode returns null for null inputs.

## Syntax
```sql
SIZE(array_or_map_expression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | ArrayType or MapType | The array or map expression whose size is to be calculated |
| legacySizeOfNull | Boolean | Internal flag controlling null handling behavior (defaults to SQLConf.legacySizeOfNull) |

## Return Type
`IntegerType` - Returns an integer representing the number of elements.

## Supported Data Types

- `ArrayType` - Any array type regardless of element type
- `MapType` - Any map type regardless of key/value types

## Algorithm

- Evaluates the child expression to get the array or map value
- If the value is null, returns -1 (legacy mode) or null (modern mode)
- For ArrayType, calls `numElements()` on the ArrayData instance
- For MapType, calls `numElements()` on the MapData instance
- Throws an error for unsupported operand types

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows without requiring data movement:

- Does not require shuffle operations
- Maintains existing partitioning scheme
- Can be executed independently on each partition

## Edge Cases

- **Null handling**: Returns -1 in legacy mode (`legacySizeOfNull = true`) or null in modern mode for null inputs
- **Empty collections**: Returns 0 for empty arrays or maps
- **Unsupported types**: Throws `QueryExecutionErrors.unsupportedOperandTypeForSizeFunctionError` for non-array/map types
- **Nullability**: Expression is non-nullable in legacy mode, nullable in modern mode

## Code Generation
This expression supports Tungsten code generation with optimized paths:

- **Legacy mode**: Generates specialized code that sets `isNull = false` and returns -1 for null inputs
- **Modern mode**: Uses `defineCodeGen` helper for standard null-safe code generation
- Both modes generate efficient `numElements()` calls without interpretation overhead

## Examples
```sql
-- Array size
SELECT SIZE(array(1, 2, 3, 4));
-- Returns: 4

-- Map size  
SELECT SIZE(map('a', 1, 'b', 2));
-- Returns: 2

-- Empty array
SELECT SIZE(array());
-- Returns: 0

-- Null handling (legacy mode)
SELECT SIZE(null);
-- Returns: -1
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.size

df.select(size($"array_column"))
df.select(size($"map_column"))
```

## See Also

- `array` - Creates arrays
- `map` - Creates maps
- `cardinality` - Alternative function for array/map size in some SQL dialects