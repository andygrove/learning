# ScalaUDF

## Overview
`ScalaUDF` is a Catalyst expression that represents user-defined functions written in Scala. It wraps a Scala function and handles the conversion between Catalyst's internal data representation and Scala data types, enabling custom logic to be executed within Spark SQL queries and DataFrame operations.

## Syntax
```scala
// DataFrame API usage
import org.apache.spark.sql.functions.udf

val myUdf = udf((x: Int, y: String) => s"$y: $x")
df.select(myUdf($"col1", $"col2"))
```

```sql
-- SQL usage (after registration)
CREATE TEMPORARY FUNCTION my_function AS 'com.example.MyUDF';
SELECT my_function(col1, col2) FROM table;
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `function` | `AnyRef` | The user-defined Scala function to execute |
| `dataType` | `DataType` | Return type of the function |
| `children` | `Seq[Expression]` | Input expressions passed to the UDF |
| `inputEncoders` | `Seq[Option[ExpressionEncoder[_]]]` | Encoders for input parameters (for typed UDFs) |
| `outputEncoder` | `Option[ExpressionEncoder[_]]` | Encoder for return type (for typed UDFs) |
| `udfName` | `Option[String]` | User-specified name of the UDF |
| `nullable` | `Boolean` | Whether the UDF can return null (default: true) |
| `udfDeterministic` | `Boolean` | Whether the UDF is deterministic (default: true) |

## Return Type
Returns the data type specified by the `dataType` parameter. Can be any Spark SQL data type including primitive types, complex types (arrays, structs, maps), and user-defined types.

## Supported Data Types
- **Input Types**: All Spark SQL data types via `AnyDataType` or specific types when `inputEncoders` are provided
- **Output Types**: All Spark SQL data types supported by the return `dataType`
- **Primitive Types**: Handled with automatic null-checking for Scala primitives
- **Complex Types**: Supported through `ExpressionEncoder` for case classes, Options, and nested structures

## Algorithm
- Evaluates input expressions and converts from Catalyst internal format to Scala types using appropriate converters
- Executes the user-defined Scala function with converted inputs
- Converts the function result back to Catalyst internal format using `catalystConverter`
- Uses `CatalystTypeConverters` for untyped UDFs and primitive types, `ExpressionEncoder` for complex typed scenarios
- Supports up to 22 input parameters through generated pattern-matched evaluation functions

## Partitioning Behavior
- **Preserves Partitioning**: No, UDFs typically break partitioning guarantees since the optimizer cannot reason about custom logic
- **Requires Shuffle**: May require shuffle depending on the query context and other operations
- **Deterministic Impact**: Only deterministic UDFs can participate in certain optimizations like predicate pushdown

## Edge Cases
- **Null Handling**: For primitive Scala parameters, automatic null checking returns null if any primitive input is null; boxed types and `Option` allow manual null handling
- **Empty Input**: Zero-parameter UDFs are supported and evaluated once per row
- **Type Mismatches**: Runtime exceptions if function signature doesn't match provided arguments
- **Encoder Limitations**: Falls back to `CatalystTypeConverters` when `ExpressionEncoder` cannot handle certain types
- **Arity Limit**: Maximum of 22 parameters due to Scala's Function22 limit

## Code Generation
This expression **does not support** whole-stage code generation and falls back to interpreted mode. The `doGenCode` method is present but the implementation is truncated in the source, indicating limited or no codegen support. The stateful nature due to `ExpressionEncoder` usage also prevents effective code generation.

## Examples
```sql
-- Register and use a UDF in SQL
CREATE TEMPORARY FUNCTION double_it AS 'com.example.DoubleUDF';
SELECT double_it(value) FROM numbers;
```

```scala
// DataFrame API with typed UDF
import org.apache.spark.sql.functions.udf

// Simple UDF
val addOne = udf((x: Int) => x + 1)
df.select(addOne($"number"))

// Complex UDF with case class
case class Person(name: String, age: Int)
val extractName = udf((p: Person) => p.name)
df.select(extractName($"person_col"))

// Multi-parameter UDF
val concat = udf((s1: String, s2: String, sep: String) => s"$s1$sep$s2")
df.select(concat($"first", $"second", lit(",")))
```

## See Also
- `UserDefinedFunction` - Higher-level wrapper for UDFs in DataFrame API
- `Expression` - Base class for all Catalyst expressions  
- `CatalystTypeConverters` - Utilities for converting between Scala and Catalyst types
- `ExpressionEncoder` - Type-safe encoders for complex Scala types