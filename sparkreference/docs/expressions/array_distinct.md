# ArrayDistinct

## Overview
The `ArrayDistinct` expression removes duplicate elements from an array while preserving the order of first occurrence. It handles null values by keeping only the first null encountered, and supports arrays containing any orderable data type.

## Syntax
```sql
array_distinct(array_expr)
```

```scala
// DataFrame API
col("array_column").distinct()
// or using expr
expr("array_distinct(array_column)")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| array_expr | ArrayType | The input array from which to remove duplicates |

## Return Type
Returns an `ArrayType` with the same element type as the input array.

## Supported Data Types
Supports arrays containing any data type that has ordering semantics:

- Numeric types (IntegerType, LongType, DoubleType, etc.)
- String types (StringType, VarcharType, CharType)
- Date and timestamp types
- Binary types
- Nested types (arrays, structs, maps) that are orderable

## Algorithm
The expression uses two different evaluation strategies based on element type:

- For types with proper equals semantics: Uses `SQLOpenHashSet` for O(1) duplicate detection with special handling for NaN and null values
- For types without proper equals: Falls back to O(n²) comparison using ordering semantics
- Maintains insertion order by using `ArrayBuffer` to collect unique elements
- Enforces maximum array size limit (`MAX_ROUNDED_ARRAY_LENGTH`) to prevent memory issues
- Handles null deduplication by tracking whether a null has already been stored

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffle as it operates on individual array elements within each partition
- Maintains the original partitioning scheme since it's a per-row transformation
- No cross-partition dependencies

## Edge Cases

- **Null arrays**: Returns null when the input array itself is null (`nullIntolerant = true`)
- **Null elements**: Preserves only the first null element encountered in the array
- **Empty arrays**: Returns an empty array of the same type
- **NaN handling**: Special logic for floating-point NaN values ensures proper deduplication
- **Size limits**: Throws `QueryExecutionErrors.arrayFunctionWithElementsExceedLimitError` if result exceeds maximum array length
- **Non-orderable types**: Fails type checking for element types that don't support ordering

## Code Generation
Supports Tungsten code generation with optimizations:

- Uses specialized hash sets for primitive types when `canUseSpecializedHashSet` is true
- Falls back to interpreted evaluation for complex types without proper equals semantics
- Generates efficient loops with minimal object allocation for supported types
- Includes bounds checking and null tracking in generated code

## Examples
```sql
-- Basic usage
SELECT array_distinct(array(1, 2, 3, 2, 1));
-- Result: [1, 2, 3]

-- With null values
SELECT array_distinct(array(1, 2, 3, null, 3, null));
-- Result: [1, 2, 3, null]

-- With strings
SELECT array_distinct(array('apple', 'banana', 'apple', 'cherry'));
-- Result: ['apple', 'banana', 'cherry']

-- Empty array
SELECT array_distinct(array());
-- Result: []
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("array_distinct(items)").as("unique_items"))

// With column reference
df.select(array_distinct(col("array_column")))
```

## See Also

- `array_union` - Combines arrays with deduplication
- `array_intersect` - Finds common elements between arrays
- `array_except` - Removes elements present in second array