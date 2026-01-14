# LambdaFunction

## Overview
LambdaFunction represents a lambda function expression along with its arguments in Spark Catalyst expressions. It encapsulates a function expression and its bound variables, enabling higher-order functions to process expressions with local variable scoping. Lambda functions can be marked as hidden for internal bookkeeping within higher-order functions when processing independent expressions.

## Syntax
```sql
-- Used internally within higher-order functions like transform, filter, etc.
transform(array_col, x -> x + 1)
filter(array_col, x -> x > 0)
```

```scala
// DataFrame API - used internally, not directly instantiated by users
LambdaFunction(function, arguments, hidden)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| function | Expression | The expression that represents the lambda function body |
| arguments | Seq[NamedExpression] | The lambda function parameters/variables |
| hidden | Boolean | Whether the lambda function is hidden for internal bookkeeping (default: false) |

## Return Type
The return type matches the data type of the underlying function expression. The LambdaFunction itself acts as a wrapper and returns whatever data type its function expression produces.

## Supported Data Types
LambdaFunction supports all data types since it acts as a wrapper around the underlying function expression. The supported data types depend entirely on what the wrapped function expression can handle.

## Algorithm

- Wraps a function expression along with its parameter definitions to create scoped variable binding
- Evaluates by directly delegating to the underlying function expression's eval method
- Manages variable scoping by filtering out lambda argument references from the function's reference set
- Tracks binding state by checking if all lambda arguments are resolved
- Uses CodegenFallback, meaning it falls back to interpreted evaluation mode

## Partitioning Behavior
LambdaFunction itself does not directly affect partitioning behavior:

- Partitioning impact depends on the higher-order function that contains the lambda
- The lambda function wrapper preserves whatever partitioning behavior the underlying function expression has
- No shuffle is introduced by the LambdaFunction wrapper itself

## Edge Cases

- Null handling behavior is delegated to the underlying function expression
- When not resolved, falls back to default reference calculation behavior
- Variable scope isolation: lambda arguments are excluded from external references when resolved
- Hidden lambdas are used for internal processing without exposing lambda semantics to users
- Binding validation ensures all arguments are resolved before the lambda is considered bound

## Code Generation
This expression uses CodegenFallback, which means it does not support Tungsten code generation and always falls back to interpreted evaluation mode for safety and simplicity.

## Examples
```sql
-- Lambda functions are used internally in higher-order functions
SELECT transform(array(1, 2, 3), x -> x * 2) as doubled;
SELECT filter(array(1, 2, 3, 4), x -> x % 2 = 0) as evens;
SELECT aggregate(array(1, 2, 3), 0, (acc, x) -> acc + x) as sum;
```

```scala
// Internal representation (not directly used by end users)
import org.apache.spark.sql.catalyst.expressions._
import org.apache.spark.sql.types._

// Example internal structure for transform(array, x -> x + 1)
val lambdaVar = UnresolvedNamedLambdaVariable(Seq("x"))
val addExpr = Add(lambdaVar, Literal(1))
val lambda = LambdaFunction(addExpr, Seq(lambdaVar), hidden = false)
```

## See Also

- HigherOrderFunction - Base class for functions that use lambda expressions
- ArrayTransform - Uses lambda functions to transform array elements  
- ArrayFilter - Uses lambda functions to filter array elements
- MapFilter - Uses lambda functions to filter map entries
- NamedExpression - Interface implemented by lambda function arguments