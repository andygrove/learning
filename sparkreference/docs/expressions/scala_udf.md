# ScalaUDF

## Overview
ScalaUDF is a Spark Catalyst expression that wraps user-defined Scala functions for execution within SQL queries and DataFrame operations. It handles type conversion between Scala data types and Catalyst's internal representation, supporting up to 22 function parameters with automatic serialization and deserialization of complex types.

## Syntax
```scala
// DataFrame API usage
import org.apache.spark.sql.functions.udf

val myUDF = udf((x: Int, y: String) => s"$x-$y")
df.select(myUDF(col("id"), col("name")))

// Registration for SQL usage
spark.udf.register("my_udf", myUDF)
```

```sql
-- SQL usage
SELECT my_udf(id, name) FROM table
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| function | AnyRef | The user-defined Scala function to execute |
| dataType | DataType | The expected return data type of the function |
| children | Seq[Expression] | Input expressions that will be passed as function arguments |
| inputEncoders | Seq[Option[ExpressionEncoder[_]]] | Optional encoders for type conversion of inputs |
| outputEncoder | Option[ExpressionEncoder[_]] | Optional encoder for type conversion of output |
| udfName | Option[String] | User-specified name for the UDF |
| nullable | Boolean | Whether the UDF can return null values (default: true) |
| udfDeterministic | Boolean | Whether the UDF is deterministic (default: true) |

## Return Type
Returns the data type specified by the `dataType` parameter, which can be any Catalyst data type including primitives, complex types (arrays, maps, structs), and user-defined types.

## Supported Data Types

- All primitive types (Int, Long, Double, Float, Boolean, String, etc.)
- Complex types (Array, Map, Struct)
- Option types for nullable values
- Case classes and custom Scala types (with appropriate encoders)
- Any type (falls back to CatalystTypeConverters)

## Algorithm

- Evaluates all child expressions to obtain input values
- Applies type converters to transform Catalyst internal format to Scala types
- Invokes the user-defined function with converted arguments
- Converts the function result back to Catalyst internal format using output converter
- Handles null values according to primitive type rules and nullable flag

## Partitioning Behavior
ScalaUDFs are stateful expressions that do not affect data partitioning directly:

- Preserves existing partitioning when used in select operations
- Does not require shuffle operations by itself
- Can be used safely across partition boundaries

## Edge Cases

- **Null handling**: Primitive Scala types receive null checks; boxed types and case classes handle nulls through encoders
- **Type mismatches**: Runtime exceptions occur if function signature doesn't match provided arguments
- **Encoder limitations**: Falls back to CatalystTypeConverters for unsupported types or missing encoders
- **Function arity**: Supports 0-22 parameters; uses pattern matching for optimal code generation
- **Exception handling**: Wraps user function exceptions with detailed error context including function name and types

## Code Generation
ScalaUDF supports full code generation (Tungsten) with optimized paths:

- Generates specialized code based on number of function parameters (0-22)
- Uses lazy evaluation for type converters to minimize overhead
- Optimizes primitive type handling by avoiding unnecessary boxing
- Falls back to interpreted mode only for unsupported type combinations

## Examples
```sql
-- Register and use a simple UDF
SELECT upper_concat(first_name, last_name) FROM users;

-- UDF with multiple parameters and types
SELECT calculate_score(age, salary, CAST(is_manager AS INT)) FROM employees;
```

```scala
// Simple string transformation UDF
val upperConcat = udf((first: String, last: String) => 
  s"${first.toUpperCase} ${last.toUpperCase}")
df.select(upperConcat(col("first_name"), col("last_name")))

// Complex type UDF with case class
case class Score(value: Double, grade: String)
val calculateScore = udf((age: Int, salary: Double, isManager: Boolean) => 
  Score(age * 0.1 + salary * 0.001, if (isManager) "A" else "B"))
df.select(calculateScore(col("age"), col("salary"), col("is_manager")))

// Nullable UDF handling
val safeDiv = udf((a: Option[Double], b: Option[Double]) => 
  for (x <- a; y <- b if y != 0) yield x / y)
df.select(safeDiv(col("numerator"), col("denominator")))
```

## See Also

- JavaUDF - Java-based user-defined functions
- HiveGenericUDF - Hive UDF integration  
- UserDefinedFunction - High-level UDF wrapper API
- ExpressionEncoder - Type encoding for complex Scala types