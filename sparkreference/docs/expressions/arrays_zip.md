# ArraysZip

## Overview
The `ArraysZip` expression combines multiple arrays into a single array of structs by transposing elements at corresponding positions. Each resulting struct contains fields named "0", "1", "2", etc., with values from the input arrays at the same index position.

## Syntax
```sql
arrays_zip(array1, array2, ...)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | Variable number of array expressions to be zipped together |
| names | Seq[Expression] | Field names for the resulting struct fields (typically auto-generated as "0", "1", "2", etc.) |

## Return Type
Array of structs, where each struct contains fields corresponding to elements from input arrays at the same position.

## Supported Data Types
All data types are supported for array elements, including:

- Numeric types (byte, short, int, long, float, double, decimal)
- String and binary types
- Boolean type
- Date and timestamp types
- Complex types (arrays, maps, structs)
- Null values

## Algorithm

- Determines the maximum length among all input arrays
- Creates output array with length equal to the maximum input array length
- For each position index, creates a struct containing values from all input arrays at that index
- Uses null values for arrays that are shorter than the maximum length
- Assigns field names as "0", "1", "2", etc. corresponding to the input array order

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle as it operates on individual rows
- Maintains existing data partitioning scheme
- Can be executed in parallel across partitions

## Edge Cases

- **Null arrays**: If an input array is null, the corresponding field in all output structs will be null
- **Empty arrays**: Empty input arrays contribute null values to all positions in the output
- **Mismatched lengths**: Shorter arrays are padded with nulls; longer arrays determine the output length
- **All empty inputs**: Results in an empty array
- **Single array input**: Creates array of single-field structs

## Code Generation
This expression supports Catalyst code generation (Tungsten) for optimized runtime performance, avoiding interpreted evaluation overhead.

## Examples
```sql
-- Basic usage with arrays of same length
SELECT arrays_zip(array(1, 2), array(2, 3), array(3, 4));
-- Result: [{"0":1,"1":2,"2":3},{"0":2,"1":3,"2":4}]

-- Arrays with different lengths
SELECT arrays_zip(array(1, 2, 3), array('a', 'b'));
-- Result: [{"0":1,"1":"a"},{"0":2,"1":"b"},{"0":3,"1":null}]

-- With null values
SELECT arrays_zip(array(1, null, 3), array('x', 'y', 'z'));
-- Result: [{"0":1,"1":"x"},{"0":null,"1":"y"},{"0":3,"1":"z"}]
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(arrays_zip(col("array1"), col("array2"), col("array3")))

// Using with explode to create rows
df.select(explode(arrays_zip(col("array1"), col("array2"))))
```

## See Also

- `explode()` - Often used with arrays_zip to create rows from zipped arrays
- `array()` - Creates arrays that can be used as input
- `struct()` - Creates individual struct values
- `zip_with()` - Alternative for element-wise array operations with custom logic