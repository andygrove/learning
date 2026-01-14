# CSV Expressions Reference

## CsvToStructs

### Overview
The `CsvToStructs` expression converts a CSV input string to a structured data type with a specified schema. It parses CSV-formatted text and returns a struct value containing the parsed fields according to the provided schema definition.

### Syntax
```sql
from_csv(csvStr, schema[, options])
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `csvStr` | String (with collation support) | The CSV-formatted input string to parse |
| `schema` | StructType | The target schema defining the structure and types of output fields |
| `options` | Map[String, String] (optional) | CSV parsing options (e.g., delimiter, timestampFormat) |
| `timeZoneId` | String (optional) | Time zone for timestamp parsing |
| `requiredSchema` | StructType (optional) | Subset of fields to extract from the full schema |

### Return Type
Returns a `StructType` with nullable fields based on the provided schema. The nullability is forced to avoid data corruption when CSV fields are missing.

### Supported Data Types
- Input: String types with collation support (including trim collation)
- Output: Any data types supported by CSV parsing (primitives, nested structures, timestamps, etc.)

### Algorithm
- Validates input is a non-null string with supported collation
- Creates a nullable version of the user-provided schema to handle missing fields
- Uses `CsvToStructsEvaluator` to parse the CSV string according to schema and options
- Applies time zone conversion for timestamp fields if specified
- Returns structured data or null if parsing fails

### Partitioning Behavior
- **Preserves partitioning**: This is a row-level transformation that doesn't require data movement
- **No shuffle required**: Each row is processed independently
- Can be pushed down to individual partitions for parallel execution

### Edge Cases
- **Null input**: Returns null (null intolerant behavior)
- **Empty CSV string**: Returns struct with null/default values for all fields
- **Missing fields**: Missing CSV fields are set to null in the output struct
- **Malformed CSV**: May populate corrupt record column or return null based on configuration
- **Schema mismatch**: Type conversion errors handled according to CSV parsing options

### Code Generation
Supports Tungsten code generation. The expression generates optimized Java code that:
- References a cached `CsvToStructsEvaluator` instance
- Performs direct method calls without reflection
- Handles null checking efficiently in generated code

### Examples
```sql
-- Basic CSV parsing
SELECT from_csv('1, 0.8', 'a INT, b DOUBLE');
-- Result: {"a":1,"b":0.8}

-- With timestamp formatting options
SELECT from_csv('26/08/2015', 'time Timestamp', map('timestampFormat', 'dd/MM/yyyy'));
-- Result: {"time":2015-08-26 00:00:00}
```

```scala
// DataFrame API usage
import org.apache.spark.sql.types._
val schema = StructType(Seq(
  StructField("a", IntegerType),
  StructField("b", DoubleType)
))
df.select(from_csv(col("csv_col"), lit(schema.toDDL)))
```

---

## SchemaOfCsv

### Overview
The `SchemaOfCsv` expression infers the schema of a CSV string by analyzing its structure and data types. It returns a DDL-formatted string describing the inferred schema structure.

### Syntax
```sql
schema_of_csv(csv[, options])
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `csv` | String | The CSV string to analyze for schema inference |
| `options` | Map[String, String] (optional) | CSV parsing options affecting schema inference |

### Return Type
Returns a `StringType` containing the schema in DDL format (e.g., "STRUCT<_c0: INT, _c1: STRING>").

### Supported Data Types
- Input: Must be `StringType` (exact type match required)
- Output: String representation of inferred schema

### Algorithm
- Validates input is a foldable (constant) non-null string expression
- Uses `SchemaOfCsvEvaluator` to analyze CSV structure and infer field types
- Generates default column names (_c0, _c1, etc.) when headers are not present
- Returns DDL-formatted schema string

### Partitioning Behavior
- **Not applicable**: This expression requires constant/foldable input and is typically evaluated at planning time
- Implemented as `RuntimeReplaceable` with `Invoke` for actual execution

### Edge Cases
- **Null input**: Compilation error - null input not allowed
- **Non-foldable input**: Compilation error - requires constant expression
- **Non-string input**: Type mismatch error
- **Empty CSV**: Infers minimal schema structure
- **Complex nested data**: Infers based on CSV's flat structure limitations

### Code Generation
Implemented as `RuntimeReplaceable` that generates an `Invoke` expression calling the evaluator's `evaluate` method. The actual schema inference happens through method invocation rather than generated code.

### Examples
```sql
-- Basic schema inference
SELECT schema_of_csv('1,abc');
-- Result: STRUCT<_c0: INT, _c1: STRING>

-- With options
SELECT schema_of_csv('1.5,"hello"', map('header', 'false'));
-- Result: STRUCT<_c0: DOUBLE, _c1: STRING>
```

```scala
// DataFrame API usage  
df.select(schema_of_csv(lit("1,abc,true")))
```

---

## StructsToCsv

### Overview
The `StructsToCsv` expression converts structured data (StructType) to a CSV-formatted string representation. It serializes struct fields into a delimited text format according to specified CSV formatting options.

### Syntax
```sql
to_csv(expr[, options])
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `expr` | StructType | The struct value to convert to CSV format |
| `options` | Map[String, String] (optional) | CSV formatting options (delimiter, timestampFormat, etc.) |
| `timeZoneId` | String (optional) | Time zone for timestamp formatting |

### Return Type
Returns a `StringType` containing the CSV-formatted representation of the input struct.

### Supported Data Types
- Input: `StructType` with fields of supported data types
- Supported field types: All primitive types, arrays, maps, nested structs, UDTs
- Unsupported: `VariantType`
- Recursive validation ensures all nested types are supported

### Algorithm
- Validates input is a StructType with all supported field data types
- Creates `UnivocityGenerator` for CSV serialization with specified options
- Converts InternalRow representation to CSV string format
- Applies time zone formatting for timestamp fields
- Returns UTF8String result

### Partitioning Behavior
- **Preserves partitioning**: Row-level transformation with no data movement required
- **No shuffle needed**: Each struct is converted independently
- Supports parallel execution across partitions

### Edge Cases
- **Null input**: Returns null (null intolerant)
- **Null fields**: Serialized according to CSV null representation options
- **Nested structures**: Flattened or serialized based on CSV format limitations
- **Special characters**: Escaped according to CSV quoting rules
- **Unsupported types**: Compilation error for VariantType or invalid nested types

### Code Generation
Supports Tungsten code generation with optimized performance:
- Caches converter function and generator instances
- Uses `nullSafeCodeGen` for efficient null handling
- Direct method invocation through cached references

### Examples
```sql
-- Basic struct to CSV
SELECT to_csv(named_struct('a', 1, 'b', 2));
-- Result: 1,2

-- With timestamp formatting
SELECT to_csv(
  named_struct('time', to_timestamp('2015-08-26', 'yyyy-MM-dd')), 
  map('timestampFormat', 'dd/MM/yyyy')
);
-- Result: 26/08/2015
```

```scala
// DataFrame API usage
df.select(to_csv(struct(col("field1"), col("field2"))))

// With options
df.select(to_csv(
  struct(col("timestamp_field")), 
  map("timestampFormat" -> "yyyy-MM-dd")
))
```

## See Also
- `from_json` / `to_json` - Similar functions for JSON format
- `get_json_object` - Extract values from JSON strings  
- CSV data source options for reading/writing CSV files
- `split` function for simple string splitting without schema