# Complex Type Extractors

## Overview

The complex type extractors are a family of expressions in Apache Spark Catalyst that extract values from nested data structures including structs, arrays, and maps. These expressions provide type-safe access to nested fields with compile-time and runtime validation.

---

# GetStructField

## Overview
Extracts a specific field from a struct by ordinal position. This expression provides efficient access to struct fields while preserving the original field name for display purposes and maintaining proper null handling semantics.

## Syntax
```sql
struct_expression.field_name
-- or
struct_expression[field_name]
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The struct expression to extract from |
| ordinal | Int | Zero-based index of the field in the struct |
| name | Option[String] | Optional field name for display/toString purposes |

## Return Type
Returns the data type of the specified field in the struct schema.

## Supported Data Types
- Input: `StructType` only
- Output: Any data type supported by Spark (depends on the field's type)

## Algorithm
- Validates input is a struct type during analysis
- Accesses the field directly by ordinal position from the InternalRow
- Preserves field metadata from the original struct schema
- Uses zero-copy access when possible through InternalRow.get()

## Partitioning Behavior
- **Preserves partitioning**: This is a projection operation that doesn't change row distribution
- **No shuffle required**: Field extraction is a local operation per partition

## Edge Cases
- **Null struct**: Returns null if the input struct is null
- **Null field**: Returns null if the specific field is null, even if the struct is non-null
- **Field nullability**: Result nullability is the union of child nullability and field nullability
- **Case sensitivity**: Field resolution respects the configured case sensitivity resolver

## Code Generation
Supports full code generation (Tungsten). Generates efficient Java bytecode that:
- Performs null checks only when necessary
- Uses direct field access via `InternalRow.get(ordinal, dataType)`
- Eliminates virtual method calls in the hot path

## Examples
```sql
-- Extract year field from a date struct
SELECT order_date.year FROM orders;

-- Access nested struct fields
SELECT customer.address.street FROM orders;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.col
df.select(col("customer.name"), col("customer.address.city"))

// Programmatic construction
GetStructField(structExpr, ordinal = 0, Some("customer_name"))
```

## See Also
- `GetArrayStructFields` - Extract fields from array of structs
- `ExtractValue` - General purpose extractor factory

---

# GetArrayStructFields

## Overview
Extracts a specific field from all elements in an array of structs, returning a new array containing only the extracted field values. This expression efficiently transforms arrays of structs into arrays of primitive or complex values.

## Syntax
```sql
array_of_structs_expression.field_name
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | Array of structs expression |
| field | StructField | The field definition to extract |
| ordinal | Int | Zero-based index of the field in each struct |
| numFields | Int | Total number of fields in the struct schema |
| containsNull | Boolean | Whether result array can contain null elements |

## Return Type
Returns `ArrayType(field.dataType, containsNull)` where the element type matches the extracted field type.

## Supported Data Types
- Input: `ArrayType(StructType, _)` only
- Output: `ArrayType` with element type matching the extracted field

## Algorithm
- Iterates through each array element
- For non-null struct elements, extracts the field at the specified ordinal
- Handles null array elements and null field values appropriately
- Constructs a new GenericArrayData with extracted values
- Preserves array ordering

## Partitioning Behavior
- **Preserves partitioning**: Array transformation doesn't change row distribution
- **No shuffle required**: Field extraction is performed locally within each partition

## Edge Cases
- **Null array**: Returns null if input array is null
- **Null array elements**: Preserves null elements in the result array
- **Null field values**: Individual null field values become null array elements
- **Empty arrays**: Returns empty array of the target field type
- **Nested nullability**: Result containsNull combines array nullability with field nullability

## Code Generation
Full code generation support with optimized loops:
- Generates efficient for-loop over array elements
- Minimizes null checks based on schema information
- Uses direct struct field access for non-null elements
- Allocates result array once and populates in-place

## Examples
```sql
-- Extract all names from array of person structs
SELECT customers.name FROM orders;

-- Extract nested field from array elements
SELECT order_items.product.category FROM orders;
```

```scala
// DataFrame API - automatically uses GetArrayStructFields
df.select(col("employees.salary"))

// Programmatic construction
GetArrayStructFields(
  child = arrayExpr,
  field = StructField("name", StringType, nullable = true),
  ordinal = 0,
  numFields = 3,
  containsNull = true
)
```

## See Also
- `GetStructField` - Extract single field from struct
- `GetArrayItem` - Access array element by index

---

# GetArrayItem

## Overview
Retrieves an element from an array at the specified index position. Supports both positive indices (0-based from start) and handles out-of-bounds access according to ANSI SQL compliance settings.

## Syntax
```sql
array_expression[index_expression]
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | Array expression to index into |
| ordinal | Expression | Integer index expression (0-based) |
| failOnError | Boolean | Whether to throw exception on invalid indices (default: SQLConf.ansiEnabled) |

## Return Type
Returns the element type of the input array (`ArrayType.elementType`).

## Supported Data Types
- Array child: Any `ArrayType`
- Index ordinal: Any `IntegralType` (converted to int)

## Algorithm
- Evaluates array and index expressions
- Validates index is within bounds [0, array.length)
- Returns array element at index or handles out-of-bounds based on failOnError
- Preserves null array elements as null results
- Uses ArrayData.get() for type-safe element access

## Partitioning Behavior
- **Preserves partitioning**: Element access doesn't redistribute data
- **No shuffle required**: Indexing is a local operation per partition

## Edge Cases
- **Null array**: Returns null
- **Null index**: Returns null  
- **Negative index**: Treated as out-of-bounds
- **Index >= array.length**: Out-of-bounds handling
  - `failOnError = true`: Throws `QueryExecutionErrors.invalidArrayIndexError`
  - `failOnError = false`: Returns null
- **Null array elements**: Returns null if array[index] is null

## Code Generation
Supports full code generation with optimized bounds checking:
- Generates inline bounds validation
- Conditional exception throwing based on failOnError
- Direct ArrayData access without boxing overhead
- Optimized null checking for array elements

## Examples
```sql
-- Access first element (ANSI mode throws on out-of-bounds)
SELECT arr[0] FROM table1;

-- Safe access in non-ANSI mode (returns null for invalid index)  
SELECT arr[10] FROM table1;

-- Dynamic indexing
SELECT arr[position - 1] FROM table1;
```

```scala
// DataFrame API
df.select(col("items")(0)) // First element
df.select(col("items")(col("index"))) // Dynamic index

// Programmatic construction  
GetArrayItem(arrayExpr, Literal(0), failOnError = true)
```

## See Also
- `ElementAt` - Array/map element access with 1-based indexing
- `GetArrayStructFields` - Extract fields from array of structs

---

# GetMapValue

## Overview
Retrieves the value associated with a specific key from a map. Performs key lookup using the map's key type equality semantics and returns the corresponding value or null if the key is not found.

## Syntax
```sql
map_expression[key_expression]
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | Map expression to lookup in |
| key | Expression | Key expression to search for |

## Return Type
Returns the value type of the input map (`MapType.valueType`).

## Supported Data Types
- Map child: Any `MapType`
- Key: Must match the map's key type and be orderable
- Result: Map's value type

## Algorithm
- Validates key type matches map's key type during analysis
- Performs linear search through map's key array (O(n) complexity)
- Uses TypeUtils.getInterpretedOrdering for key comparison
- Returns corresponding value from value array if key found
- Returns null if key not found or if found value is null

## Partitioning Behavior
- **Preserves partitioning**: Map lookup doesn't change data distribution
- **No shuffle required**: Key lookup is performed locally within each partition

## Edge Cases
- **Null map**: Returns null
- **Null key**: Returns null (null keys don't match any stored keys)
- **Key not found**: Returns null
- **Null values**: Returns null if the key exists but maps to null
- **Duplicate keys**: Implementation finds first matching key (maps should not have duplicates)
- **Non-orderable keys**: Compilation error during analysis

## Code Generation
Full code generation support with optimized key search:
- Generates efficient while-loop for key scanning
- Uses direct key comparison with type-specific equality
- Minimizes null checks based on map schema
- Direct ArrayData access for keys and values

## Examples
```sql
-- Lookup value by string key
SELECT user_prefs['theme'] FROM users;

-- Dynamic key lookup  
SELECT metrics[metric_name] FROM measurements;

-- Nested map access
SELECT config['database']['host'] FROM applications;
```

```scala
// DataFrame API
df.select(col("preferences")("language"))
df.select(col("scores")(col("player_name")))

// Programmatic construction
GetMapValue(mapExpr, Literal("key1"))
GetMapValue(mapExpr, keyExpr)
```

## See Also
- `ElementAt` - Map/array element access with different null handling
- `MapKeys` - Extract all keys from a map
- `MapValues` - Extract all values from a map

---

# ExtractValue (Factory Object)

## Overview
Factory object that provides intelligent routing to the appropriate concrete extractor expression based on the input data types. Handles type analysis and resolution to create the most efficient extractor for struct, array, and map access patterns.

## Syntax
Used internally by the Catalyst analyzer, not directly accessible in SQL.

## Arguments
| Method | Arguments | Description |
|--------|-----------|-------------|
| apply | child: Expression, extraction: Expression, resolver: Resolver | Returns resolved ExtractValue, throws on failure |
| extractValue | child: Expression, extraction: Expression, resolver: Resolver | Returns Either[Expression, Throwable] |
| isExtractable | attribute: Attribute, nestedFields: Seq[String], extractorKey: Option[Expression], resolver: Resolver | Tests if extraction path is valid |

## Return Type
Returns appropriate concrete ExtractValue subclass or error information.

## Supported Data Types
Routing logic based on child and extraction types:
- `(StructType, StringLiteral)` → `GetStructField`
- `(ArrayType(StructType), StringLiteral)` → `GetArrayStructFields`  
- `(ArrayType, IntegralType)` → `GetArrayItem`
- `(MapType, KeyType)` → `GetMapValue`

## Algorithm
- Pattern matches on (child.dataType, extraction) tuple
- For struct access: resolves field name and finds ordinal
- For array struct access: validates field exists in struct schema
- For array/map access: delegates to appropriate concrete expression
- Handles field name resolution with case sensitivity
- Provides detailed error messages for unsupported combinations

## Partitioning Behavior
N/A - Factory object for creating other expressions.

## Edge Cases
- **Ambiguous field names**: Reports error when multiple fields match (case-insensitive mode)
- **Missing fields**: Reports detailed error with available field names
- **Unsupported type combinations**: Clear error messages for invalid extractions
- **Case sensitivity**: Respects configured field name resolution strategy

## Code Generation
N/A - Factory creates expressions that support code generation.

## Examples
```scala
// Used internally during analysis
ExtractValue(structExpr, Literal("fieldName"), resolver)

// Test if extraction is possible
ExtractValue.isExtractable(
  attribute = col,
  nestedFields = Seq("address", "street"), 
  extractorKey = Some(Literal("apt")),
  resolver = resolver
)
```

## See Also
- All concrete ExtractValue implementations
- Catalyst analyzer resolution rules
- Field name resolution strategies