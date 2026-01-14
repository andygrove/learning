# ArraySize

## Overview
The `ArraySize` expression returns the number of elements in an array. It is a runtime-replaceable expression that internally delegates to the `Size` expression with `legacySizeOfNull` set to false, providing consistent null handling behavior.

## Syntax
```sql
array_size(array_expr)
```

```scala
// DataFrame API
col("array_column").expr("array_size(array_column)")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The array expression whose size will be calculated |

## Return Type
Returns an `IntegerType` representing the number of elements in the array.

## Supported Data Types

- `ArrayType` - Arrays of any element type (string, numeric, complex types, etc.)

## Algorithm

- Evaluates the input array expression to get the array value

- If the array is null, returns null (non-legacy behavior)

- If the array is not null, counts the number of elements in the array

- Returns the count as an integer value

- Delegates the actual size calculation to the underlying `Size` expression

## Partitioning Behavior
This expression preserves partitioning since it operates on individual rows without requiring data movement:

- Does not require shuffle operations

- Can be executed independently on each partition

- Maintains existing data distribution

## Edge Cases

- **Null arrays**: Returns null when the input array is null (non-legacy behavior)

- **Empty arrays**: Returns 0 for arrays with no elements

- **Nested arrays**: Counts only the top-level elements, not nested array contents

- **Arrays with null elements**: Null elements within the array are counted as regular elements

## Code Generation
This expression supports code generation through its runtime replacement mechanism:

- Uses the underlying `Size` expression's code generation capabilities

- Benefits from Tungsten code generation optimizations

- Falls back to interpreted mode if code generation fails

## Examples
```sql
-- Basic array size calculation
SELECT array_size(array('b', 'd', 'c', 'a'));
-- Returns: 4

-- Empty array
SELECT array_size(array());
-- Returns: 0

-- Null array
SELECT array_size(NULL);
-- Returns: NULL

-- Array with null elements
SELECT array_size(array('a', NULL, 'c'));
-- Returns: 3
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("array_size(array_column)"))

// With array creation
df.select(expr("array_size(array('a', 'b', 'c'))"))
```

## See Also

- `Size` - The underlying expression that performs the actual size calculation
- `array` - Function to create arrays
- `cardinality` - Alternative function for getting array/map size