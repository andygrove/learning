# ApplyFunctionExpression

## Overview
`ApplyFunctionExpression` is a Catalyst expression that wraps and evaluates user-defined scalar functions that implement the `ScalarFunction` interface. It serves as a bridge between Spark's external function API and the internal Catalyst expression evaluation system, allowing custom scalar functions to be seamlessly integrated into SQL queries and DataFrame operations.

## Syntax
```sql
-- SQL syntax depends on the registered function name
SELECT custom_function(col1, col2, ...) FROM table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.connector.catalog.functions.ScalarFunction
df.select(expr("custom_function(col1, col2)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `function` | `ScalarFunction[_]` | The user-defined scalar function instance to be applied |
| `children` | `Seq[Expression]` | The input expressions that will be evaluated and passed to the scalar function |

## Return Type
The return type is determined dynamically by calling `function.resultType()` on the wrapped `ScalarFunction` instance. The actual data type depends on the specific implementation of the user-defined function.

## Supported Data Types
Input data types are determined by the wrapped `ScalarFunction`'s `inputTypes()` method. The expression supports any data types that:
- Are specified by the function's input type requirements via `function.inputTypes()`
- Can be implicitly cast to the required types (due to `ImplicitCastInputTypes` trait)
- Are compatible with Spark's internal data type system

## Algorithm
- Creates a reused `SpecificInternalRow` based on the function's input types for efficient memory usage
- During evaluation, iterates through all child expressions and evaluates them against the input row
- Populates the reused internal row with the evaluated child expression results
- Delegates to the wrapped `ScalarFunction.produceResult()` method to compute the final result
- Returns the function's computed result directly

## Partitioning Behavior
- **Preserves partitioning**: This expression does not affect data partitioning as it operates row-by-row
- **No shuffle required**: Evaluation is performed locally on each partition without requiring data movement
- Partitioning behavior ultimately depends on how the expression is used within larger query plans

## Edge Cases
- **Null handling**: Nullability is determined by `function.isResultNullable()` - the wrapped function controls null behavior
- **Empty input**: Behavior depends on the specific `ScalarFunction` implementation when no arguments are provided
- **Type mismatches**: Relies on implicit casting; incompatible types will cause runtime failures
- **Non-deterministic functions**: Determinism is computed as the logical AND of function determinism and all children's determinism

## Code Generation
This expression extends `CodegenFallback`, meaning it **does not support** Tungsten code generation. All evaluation falls back to interpreted mode using the `eval()` method, which may result in slower performance compared to code-generated expressions.

## Examples
```sql
-- Assuming a registered UDF named 'my_custom_function'
SELECT my_custom_function(age, name) FROM users;
SELECT id, my_custom_function(salary * 1.1) FROM employees;
```

```scala
// Example with DataFrame API
import org.apache.spark.sql.functions.expr
df.select(expr("my_custom_function(col1, col2)"))

// Direct usage in expression tree (internal API)
val customFunc: ScalarFunction[String] = // ... implementation
val expression = ApplyFunctionExpression(
  function = customFunc,
  children = Seq(col("input1").expr, col("input2").expr)
)
```

## See Also
- `ScalarFunction` - The interface that wrapped functions must implement
- `UserDefinedExpression` - Parent trait for user-defined expressions
- `ImplicitCastInputTypes` - Trait providing automatic type casting behavior
- `CodegenFallback` - Trait for expressions that don't support code generation