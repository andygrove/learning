# RaiseError

## Overview
The `RaiseError` expression is used for debugging purposes to throw custom exceptions during query execution. It allows users to specify an error class and associated parameters, defaulting to `USER_RAISED_EXCEPTION` when only a message is provided.

## Syntax
```sql
raise_error(error_message)
raise_error(error_class, error_parameters_map)
```

```scala
// DataFrame API
col("column").selectExpr("raise_error('Custom error message')")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| errorClass | StringType | The error class identifier to be thrown |
| errorParms | MapType(StringType, StringType) | A map containing error parameters with string keys and values |
| dataType | DataType | The return data type (typically NullType) |

## Return Type
The expression is configured with a `DataType` parameter but never actually returns a value since it always throws an exception. The return type is typically `NullType`.

## Supported Data Types

- **errorClass**: String types with collation support (including trim collation)
- **errorParms**: Map type with string keys and string values (both supporting collation)

## Algorithm

- Evaluates the errorClass expression to get the error identifier as UTF8String
- Evaluates the errorParms expression to get the parameter map as MapData
- Calls the raiseError utility method with the evaluated parameters
- Throws the constructed exception, preventing normal expression evaluation
- In code generation, wraps the throw statement in `if (true)` to avoid unreachable code compilation errors

## Partitioning Behavior
Since this expression always throws an exception during evaluation, it does not affect partitioning behavior. The query execution will terminate when this expression is evaluated, regardless of partitioning strategy.

## Edge Cases

- **Null handling**: The expression is marked as nullable but never returns null since it always throws
- **Legacy mode**: When `LEGACY_RAISE_ERROR_WITHOUT_ERROR_CLASS` is enabled, uses `_LEGACY_ERROR_USER_RAISED_EXCEPTION` as the default error class
- **Foldability**: Explicitly marked as non-foldable to prevent constant folding optimization
- **Single argument constructor**: Automatically wraps string messages in the standard error format with errorMessage parameter

## Code Generation
This expression supports Tungsten code generation. It generates code that evaluates both child expressions and then throws the exception using `QueryExecutionErrors.raiseError()`. The generated code uses an `if (true)` wrapper to avoid compiler warnings about unreachable code.

## Examples
```sql
-- Raise error with simple message
SELECT raise_error('Something went wrong');

-- Raise error with custom error class and parameters  
SELECT raise_error('CUSTOM_ERROR_CLASS', map('param1', 'value1', 'param2', 'value2'));
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Simple error message
df.select(expr("raise_error('Validation failed')"))

// Custom error with parameters
df.select(expr("raise_error('VALIDATION_ERROR', map('field', 'user_id', 'value', '123'))"))
```

## See Also

- Error handling expressions
- Debugging utilities
- `QueryExecutionErrors` utility class
- SQL configuration `LEGACY_RAISE_ERROR_WITHOUT_ERROR_CLASS`