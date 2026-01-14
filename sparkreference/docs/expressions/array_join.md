# ArrayJoin

## Overview
The `ArrayJoin` expression concatenates all elements of an array into a single string using a specified delimiter. It provides optional null replacement functionality to handle null elements within the array, either by replacing them with a custom string or ignoring them entirely.

## Syntax
```sql
array_join(array, delimiter [, nullReplacement])
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(array_join(col("array_column"), " ", "NULL"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| array | Array[String] | The input array containing string elements to be joined |
| delimiter | String | The separator string used between array elements |
| nullReplacement | String (optional) | Optional replacement string for null array elements |

## Return Type
Returns a `StringType` with the same collation settings as the input array element type.

## Supported Data Types

- Input array must be of type `AbstractArrayType(StringTypeWithCollation)`
- Delimiter must be of type `StringTypeWithCollation` 
- Optional null replacement must be of type `StringTypeWithCollation`
- All string types must support trim collation

## Algorithm

- Evaluates the input array, delimiter, and optional null replacement expressions
- Returns null if any required expression evaluates to null
- Iterates through array elements using a UTF8StringBuilder for efficient concatenation
- For non-null elements: appends delimiter (except before first element) then appends the element value
- For null elements: either ignores them or replaces with the specified replacement string

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows without requiring data movement:

- Does not require shuffle operations
- Maintains existing partitioning scheme
- Can be executed in parallel across partitions

## Edge Cases

- Returns null if the input array is null
- Returns null if the delimiter is null
- Returns null if null replacement parameter is provided but evaluates to null
- Empty arrays produce empty strings
- Arrays with only null elements produce empty strings (when no replacement specified) or only delimiters with replacements
- Single element arrays return just that element (no delimiter added)

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method:

- Generates optimized Java code for array iteration and string building
- Uses `UTF8StringBuilder` for efficient string concatenation
- Includes null-safe execution paths when inputs are nullable
- Falls back to interpreted mode only if code generation context limits are exceeded

## Examples
```sql
-- Basic usage
SELECT array_join(array('hello', 'world'), ' ');
-- Result: "hello world"

-- With null replacement
SELECT array_join(array('hello', null, 'world'), ' ', 'NULL');
-- Result: "hello NULL world"

-- Ignoring nulls (default behavior)
SELECT array_join(array('hello', null, 'world'), ' ');  
-- Result: "hello world"

-- Custom delimiter
SELECT array_join(array('a', 'b', 'c'), ', ');
-- Result: "a, b, c"
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Basic join with space delimiter
df.select(array_join(col("tags"), " "))

// Join with null replacement
df.select(array_join(col("values"), ",", "MISSING"))

// Complex example with array creation
df.select(array_join(array(col("first"), col("last")), " - "))
```

## See Also

- `split` - Splits strings into arrays (inverse operation)
- `concat` - Concatenates multiple string columns
- `concat_ws` - Concatenates strings with separator
- `array` - Creates arrays from multiple columns