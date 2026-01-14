# Literal

## Overview
The `Literal` expression represents constant values in Spark SQL expressions. It wraps a value of any supported data type and provides type-safe evaluation during query execution. Literals are leaf expressions that always return the same constant value regardless of input data.

## Syntax
```sql
-- Literals are created implicitly in SQL
SELECT 42, 'hello', true, NULL
SELECT DATE '2023-01-01', TIMESTAMP '2023-01-01 12:00:00'
```

```scala
// DataFrame API - use lit() function
import org.apache.spark.sql.functions.lit
df.select(lit(42), lit("hello"), lit(true))

// Direct constructor (discouraged - use Literal.create() for type checking)
Literal(42, IntegerType)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| value | Any | The constant value to be wrapped (can be null) |
| dataType | DataType | The Spark SQL data type of the value |

## Return Type
Returns the same data type as specified in the `dataType` parameter. The return type is always known at compile time since literals represent constant values.

## Supported Data Types

- Primitive types: Boolean, Byte, Short, Integer, Long, Float, Double
- String and Binary types
- Temporal types: Date, Time, Timestamp, TimestampNTZ
- Interval types: CalendarInterval, DayTimeInterval, YearMonthInterval  
- Decimal types with arbitrary precision and scale
- Complex types: Array, Map, Struct
- Variant type for semi-structured data
- Null type

## Algorithm

- Validates the literal value against the specified data type during construction
- Returns the constant value directly without any computation during evaluation
- Implements specialized string formatting for different data types in `toString()`
- Generates optimized Java code for primitive types during code generation
- Uses reference objects for complex types to avoid repeated serialization

## Partitioning Behavior
Literal expressions do not affect partitioning behavior since they:

- Do not require data movement or shuffling
- Are evaluated independently of input data distribution  
- Can be computed on any partition without coordination
- Are often used in predicate pushdown optimizations

## Edge Cases

- **Null handling**: Returns `true` for `nullable` when value is `null`, handles null values correctly in `equals()` and `hashCode()`
- **NaN values**: Special handling for Float/Double NaN values in equality comparison and code generation
- **Binary data**: Uses hex encoding for string representation and proper array comparison for equality
- **ArrayBasedMapData**: Implements deterministic hashCode by combining key and value array hash codes
- **Infinity values**: Properly handles positive/negative infinity for floating-point types in SQL generation

## Code Generation
Supports full code generation (Tungsten) with optimizations:

- Primitive types generate inline Java literals (`42`, `true`, `3.14D`)
- Special constants use Java constants (`Float.NaN`, `Double.POSITIVE_INFINITY`)
- Complex objects use cached reference objects via `ctx.addReferenceObj()`
- Null literals generate optimized null-checking code

## Examples
```sql
-- Numeric literals
SELECT 42, 3.14D, 123.45BD, 100Y, 1000S, 1000000L

-- String and binary literals  
SELECT 'hello world', X'48656C6C6F'

-- Temporal literals
SELECT DATE '2023-01-01', TIME '12:30:45', TIMESTAMP '2023-01-01 12:30:45'

-- Special values
SELECT CAST('NaN' AS DOUBLE), CAST('Infinity' AS FLOAT)

-- Complex types
SELECT ARRAY(1, 2, 3), MAP('key1', 'value1', 'key2', 'value2')
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(
  lit(42).as("int_literal"),
  lit("hello").as("string_literal"), 
  lit(true).as("bool_literal"),
  lit(null).as("null_literal")
)

// Temporal literals
df.select(
  lit(java.sql.Date.valueOf("2023-01-01")).as("date_literal"),
  lit(java.sql.Timestamp.valueOf("2023-01-01 12:30:45")).as("timestamp_literal")
)
```

## See Also

- `Column.lit()` - DataFrame API function for creating literals
- `Literal.create()` - Factory method with type validation
- `Cast` - Expression for converting between data types
- `LeafExpression` - Base class for expressions without child expressions