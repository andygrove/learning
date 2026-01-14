# Complex Type Creator Expressions

This document covers the Spark Catalyst expressions for creating complex data types (arrays, maps, and structs) from scalar values or other expressions.

---

# CreateArray

## Overview
Creates an array containing the evaluation results of all child expressions. The expression performs type coercion to ensure all elements have a compatible common type and preserves nullability information from the input expressions.

## Syntax
```sql
array(expr1, expr2, ..., exprN)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.array
df.select(array(col("col1"), col("col2"), lit(3)))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | Variable number of expressions to be included as array elements |
| useStringTypeWhenEmpty | Boolean | Internal flag determining default element type for empty arrays (StringType vs NullType) |

## Return Type
`ArrayType` with element type determined by finding the common type among all child expressions. The array's `containsNull` flag is set to true if any child expression is nullable.

## Supported Data Types
- All primitive types (numeric, string, boolean, binary, date, timestamp)
- Complex types (arrays, maps, structs) 
- All child expressions must be coercible to a common type

## Algorithm
- Validates all child expressions have compatible types via `TypeUtils.checkForSameTypeInputExpr`
- Determines common element type using `TypeCoercion.findCommonTypeDifferentOnlyInNullFlags`
- Falls back to StringType or NullType for empty arrays based on configuration
- Creates `GenericArrayData` containing evaluated results of all children
- Uses code generation to create optimized `ArrayData` instances

## Partitioning Behavior
- Preserves partitioning as it's a pure transformation
- No shuffle required
- Can be pushed down in projections

## Edge Cases
- **Empty arrays**: Type determined by `LEGACY_CREATE_EMPTY_COLLECTION_USING_STRING_TYPE` config
- **Null elements**: Preserved in resulting array, affects `containsNull` flag
- **Type coercion failures**: Throws compilation error if no common type found
- **Mixed nullability**: Result array allows nulls if any input is nullable

## Code Generation
Full code generation support via `doGenCode`. Uses `GenArrayData.genCodeToCreateArrayData` to generate optimized array allocation and element assignment code without boxing overhead.

## Examples
```sql
-- Basic array creation
SELECT array(1, 2, 3); -- [1, 2, 3]

-- Mixed types (coerced to common type)
SELECT array(1, 2.5, 3); -- [1.0, 2.5, 3.0] (all doubles)

-- With nulls
SELECT array(1, NULL, 3); -- [1, null, 3]

-- Empty array
SELECT array(); -- [] (type depends on config)
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._
df.select(array(col("id"), lit(100)))
df.select(array(col("name"), col("description")))
```

## See Also
- CreateMap - for creating map structures
- CreateNamedStruct - for creating struct types

---

# CreateMap

## Overview
Creates a map containing key-value pairs from a flattened sequence of expressions. Children are interpreted as alternating keys and values (key1, value1, key2, value2, ...), with type coercion applied separately to keys and values.

## Syntax
```sql
map(key1, value1, key2, value2, ...)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.map
df.select(map(lit("key1"), col("value1"), lit("key2"), col("value2")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | Even-length sequence of expressions alternating between keys and values |
| useStringTypeWhenEmpty | Boolean | Internal flag for empty map type resolution |

## Return Type
`MapType` with key type as common type of odd-indexed children and value type as common type of even-indexed children. `valueContainsNull` set based on value expression nullability.

## Supported Data Types
- **Keys**: Must be valid map key types (primitive types, no complex types)
- **Values**: All data types supported
- All keys must be coercible to common type; all values must be coercible to common type

## Algorithm
- Validates even number of children expressions
- Separates odd-indexed (keys) and even-indexed (values) expressions
- Performs type checking ensuring all keys have same type and all values have same type
- Validates key type is acceptable for maps via `TypeUtils.checkForMapKeyType`
- Uses `ArrayBasedMapBuilder` for efficient map construction
- Applies type coercion to determine final key and value types

## Partitioning Behavior
- Preserves partitioning as pure transformation
- No shuffle required
- Can be pushed down in projections

## Edge Cases
- **Odd number of arguments**: Compilation error
- **Null keys**: Runtime behavior depends on map implementation
- **Duplicate keys**: Later values overwrite earlier ones
- **Empty maps**: Type determined by configuration flag
- **Invalid key types**: Complex types (arrays, maps, structs) not allowed as keys

## Code Generation
Full code generation support. Generates separate array creation code for keys and values, then uses `ArrayBasedMapBuilder.from()` method for efficient map construction.

## Examples
```sql
-- Basic map creation
SELECT map('a', 1, 'b', 2); -- {'a': 1, 'b': 2}

-- Mixed value types (coerced)
SELECT map('int', 1, 'double', 2.5); -- {'int': 1.0, 'double': 2.5}

-- With null values
SELECT map('key1', NULL, 'key2', 'value'); -- {'key1': null, 'key2': 'value'}
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._
df.select(map(lit("status"), col("status_code")))
df.select(map(col("key_col"), col("value_col")))
```

## See Also
- MapFromArrays - creates maps from separate key and value arrays
- StringToMap - creates maps by parsing delimited strings

---

# MapFromArrays

## Overview
Creates a map from two separate array expressions, where the first array provides keys and the second provides corresponding values. Requires both arrays to have the same length and keys to be non-null.

## Syntax
```sql
map_from_arrays(keys_array, values_array)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.map_from_arrays
df.select(map_from_arrays(col("keys"), col("values")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | Array expression providing map keys |
| right | Expression | Array expression providing map values |

## Return Type
`MapType` where key type matches the element type of the left array and value type matches the element type of the right array. Inherits `containsNull` from the right array's specification.

## Supported Data Types
- **Left (keys)**: ArrayType with valid map key element types (primitives only)
- **Right (values)**: ArrayType with any element type
- Both inputs must be array types

## Algorithm
- Validates both inputs are ArrayType via `ExpectsInputTypes`
- Checks left array element type is valid for map keys
- Copies both input arrays to avoid mutation
- Uses `ArrayBasedMapBuilder.from()` for efficient map construction from array data
- Preserves value nullability from right array specification

## Partitioning Behavior
- Preserves partitioning as pure transformation
- No shuffle required
- Null intolerant - returns null if either input array is null

## Edge Cases
- **Null inputs**: Returns null (null intolerant behavior)
- **Mismatched array lengths**: Runtime behavior undefined, may cause errors
- **Null keys**: May cause runtime errors depending on map implementation
- **Invalid key types**: Compilation error if left array contains complex types
- **Empty arrays**: Creates empty map

## Code Generation
Full code generation support. Uses `nullSafeCodeGen` to handle null inputs and generates code calling `ArrayBasedMapBuilder.from()` with copied array data.

## Examples
```sql
-- Basic usage
SELECT map_from_arrays(array('a', 'b'), array(1, 2)); -- {'a': 1, 'b': 2}

-- With null values
SELECT map_from_arrays(array('x', 'y'), array(1, NULL)); -- {'x': 1, 'y': null}

-- From column arrays
SELECT map_from_arrays(key_array_col, value_array_col) FROM table;
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._
df.select(map_from_arrays(col("key_array"), col("value_array")))
```

## See Also
- CreateMap - creates maps from flattened key-value pairs
- StringToMap - creates maps by parsing strings

---

# CreateNamedStruct

## Overview
Creates a struct with explicitly named fields from a flattened sequence of name-value pairs. Unlike CreateArray or CreateMap, this expression requires field names to be compile-time constants and supports metadata preservation from named expressions.

## Syntax
```sql
named_struct(name1, value1, name2, value2, ...)
-- or
struct(value1, value2, ...) -- uses generated names
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.struct
df.select(struct(col("col1").as("field1"), col("col2").as("field2")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | Alternating field names (must be string literals) and values |

## Return Type
`StructType` with fields defined by name-value pairs. Field nullability matches the corresponding value expression nullability. Preserves metadata from NamedExpression and GetStructField inputs.

## Supported Data Types
- **Field names**: Must be foldable string expressions (typically literals)
- **Field values**: All data types supported
- Names cannot be null after evaluation

## Algorithm
- Validates even number of children (name-value pairs)
- Extracts name expressions and validates they are foldable string types
- Evaluates name expressions at compile time to get field names
- Validates no null names exist
- Creates StructType with fields preserving value nullability and metadata
- Generates InternalRow containing evaluated values

## Partitioning Behavior
- Preserves partitioning as pure transformation
- No shuffle required  
- Can be pushed down in projections
- Individual fields can be accessed without reconstructing entire struct

## Edge Cases
- **Odd number of arguments**: Compilation error
- **Non-string names**: Compilation error  
- **Non-foldable names**: Compilation error
- **Null names**: Compilation error
- **Duplicate field names**: Allowed, creates struct with duplicate fields
- **Empty struct**: Not allowed, must have at least one field

## Code Generation
Full code generation support. Creates Object array for field values, populates with generated code for each value expression, then constructs GenericInternalRow. Includes optimizations to null the temporary array after use.

## Examples
```sql
-- Named struct
SELECT named_struct('name', 'John', 'age', 25); -- {'name': 'John', 'age': 25}

-- Auto-named struct  
SELECT struct(name, age); -- {'name': 'John', 'age': 25} (uses column names)

-- Nested structs
SELECT named_struct('person', struct(name, age), 'id', id);
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._
df.select(struct(col("name"), col("age"))) // Auto-named
df.select(struct(col("name").as("full_name"), col("age"))) // Mixed naming
```

## See Also
- CreateArray - for array creation
- CreateMap - for map creation  
- UpdateFields - for modifying existing structs

---

# StringToMap

## Overview
Creates a map by parsing a delimited string into key-value pairs using configurable delimiters. Supports regex-based splitting with customizable pair and key-value separators, with proper collation awareness.

## Syntax
```sql
str_to_map(text[, pairDelim[, keyValueDelim]])
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.str_to_map
df.select(str_to_map(col("text"), lit(","), lit(":")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| text | Expression | String expression to parse |
| pairDelim | Expression | Delimiter separating key-value pairs (default: ",") |
| keyValueDelim | Expression | Delimiter separating keys from values (default: ":") |

## Return Type
`MapType(StringType, StringType)` with the same string type and collation as the input text. Values can be null if no key-value delimiter found.

## Supported Data Types
- All three arguments must be StringType with non-case-sensitive-accent-insensitive collation
- Input text collation is preserved in output map key and value types

## Algorithm
- Splits input text using pairDelim regex to get key-value pair strings
- For each pair, splits using keyValueDelim regex (limit 2) to separate key and value
- If no key-value delimiter found, uses entire string as key with null value
- Uses `CollationAwareUTF8String.splitSQL` for proper collation handling
- Builds map using `ArrayBasedMapBuilder` for efficiency
- Respects `LEGACY_TRUNCATE_FOR_EMPTY_REGEX_SPLIT` configuration

## Partitioning Behavior
- Preserves partitioning as pure transformation
- No shuffle required
- Null intolerant - returns null if any input is null

## Edge Cases
- **Null inputs**: Returns null
- **Empty string**: Returns empty map
- **No pair delimiter**: Single key-value pair
- **No key-value delimiter**: Key with null value
- **Multiple key-value delimiters**: Only first delimiter used (splits with limit 2)
- **Duplicate keys**: Later occurrences overwrite earlier ones
- **Empty regex patterns**: Behavior depends on legacy configuration flag

## Code Generation
Full code generation support with collation awareness. Generates optimized splitting code using `CollationAwareUTF8String.splitSQL` and efficient map building loops.

## Examples
```sql
-- Basic usage
SELECT str_to_map('a:1,b:2,c:3'); -- {'a':'1', 'b':'2', 'c':'3'}

-- Custom delimiters  
SELECT str_to_map('a=1;b=2', ';', '='); -- {'a':'1', 'b':'2'}

-- Missing values
SELECT str_to_map('a:1,b,c:3'); -- {'a':'1', 'b':null, 'c':'3'}

-- Single pair
SELECT str_to_map('key:value'); -- {'key':'value'}
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._
df.select(str_to_map(col("config_string")))
df.select(str_to_map(col("params"), lit(";"), lit("=")))
```

## See Also
- CreateMap - for creating maps from expressions
- MapFromArrays - for creating maps from arrays

---

# UpdateFields

## Overview
Enables adding, replacing, or dropping fields in existing struct expressions through a sequence of field operations. Supports nested field access and modification while preserving the original struct's nullability.

## Syntax
```sql
-- Internal expression, typically used via higher-level functions
-- Not directly callable in SQL
```

```scala
// Used internally by struct manipulation functions
// Not part of public DataFrame API
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| structExpr | Expression | Base struct expression to modify |
| fieldOps | Seq[StructFieldsOperation] | Sequence of field operations (WithField, DropField) |

## Return Type
`StructType` with fields modified according to the field operations. Preserves nullability of the original struct expression.

## Supported Data Types
- **structExpr**: Must be StructType
- **Field operations**: Support all data types for field values
- Field names must be valid identifiers

## Algorithm
- Validates input is a StructType
- Extracts existing field expressions (from CreateNamedStruct or via GetStructField)
-