# CallMethodViaReflection

## Overview
CallMethodViaReflection is a Spark Catalyst expression that enables calling static methods on Java classes via reflection from SQL queries. It provides a bridge between Spark SQL and arbitrary Java code by allowing dynamic method invocation with type conversion and error handling.

## Syntax
```sql
reflect(className, methodName, arg1, arg2, ...)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| className | String (foldable) | Fully qualified Java class name containing the static method |
| methodName | String (foldable) | Name of the static method to invoke |
| arg1, arg2, ... | Various supported types | Arguments to pass to the method (optional) |

## Return Type
Always returns `StringType` - the result of calling `String.valueOf()` on the method's return value.

## Supported Data Types
Input arguments support the following data types:

- BooleanType
- ByteType  
- ShortType
- IntegerType
- LongType
- FloatType
- DoubleType
- StringType (with collation support)

## Algorithm
The expression evaluation follows these steps:

- Validates that the specified class exists and can be loaded via reflection
- Locates the target static method matching the provided method name and argument types
- Converts Spark internal data types to appropriate Java objects (UTF8String to String)
- Invokes the method using Java reflection with the converted arguments
- Wraps the result using `String.valueOf()` and converts to UTF8String for return

## Partitioning Behavior
This expression has no impact on partitioning:

- Preserves existing partitioning as it operates row-by-row
- Does not require shuffle operations
- Marked as `Nondeterministic` which may affect certain optimizations

## Edge Cases

- **Null handling**: Returns null if any required argument is null or if method invocation fails (when `failOnError` is false)
- **Class loading**: Throws compilation error if the specified class cannot be found or loaded
- **Method resolution**: Throws compilation error if no matching static method is found for the given signature  
- **Type conversion**: Only UTF8String arguments are converted to Java String; other types are passed as-is
- **Exception handling**: Method invocation exceptions return null when `failOnError=false`, otherwise propagate

## Code Generation
This expression uses `CodegenFallback`, meaning it does not support Tungsten code generation and always falls back to interpreted evaluation mode for safety with reflection operations.

## Examples
```sql
-- Call UUID.fromString() method
SELECT reflect('java.util.UUID', 'fromString', 'a5cf6c42-0c85-418f-af6c-3e4e5b1328f2');
-- Returns: a5cf6c42-0c85-418f-af6c-3e4e5b1328f2

-- Call Math.max() with integer arguments  
SELECT reflect('java.lang.Math', 'max', 10, 20);
-- Returns: 20

-- Call System.getProperty() 
SELECT reflect('java.lang.System', 'getProperty', 'java.version');
-- Returns: current Java version string
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.expr

df.select(expr("reflect('java.lang.Math', 'abs', -42)").as("absolute_value"))

// Using column references
df.select(expr("reflect('java.lang.String', 'valueOf', some_column)").as("string_value"))
```

## See Also

- UDF (User Defined Functions) for type-safe custom logic
- Built-in mathematical functions for common operations
- `CallMethodViaReflection.typeMapping` for supported type conversions