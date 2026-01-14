# InterpretedPredicate

## Overview
InterpretedPredicate is a Catalyst expression evaluator that wraps a boolean expression and evaluates it in interpreted mode (non-code-generated). It extends BasePredicate and is primarily used for filtering operations where the predicate expression needs to be evaluated row by row to return a boolean result.

## Syntax
```scala
// Internal Catalyst usage - not directly exposed to SQL/DataFrame API
InterpretedPredicate(expression: Expression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expression | Expression | The boolean expression to be evaluated against input rows |

## Return Type
Boolean - returns true if the predicate condition is satisfied, false otherwise.

## Supported Data Types
InterpretedPredicate itself doesn't restrict data types - it depends on the wrapped expression. The wrapped expression must evaluate to a Boolean type, but can operate on:

- All primitive types (numeric, string, boolean)
- Complex types (arrays, maps, structs)  
- Date and timestamp types
- Any data type supported by the underlying expression

## Algorithm

- Prepares the wrapped expression during initialization with optional subexpression elimination
- On evaluation, sets the input row in the runtime context if subexpression elimination is enabled
- Delegates the actual evaluation to the wrapped expression's eval method
- Casts the result to Boolean type before returning

## Partitioning Behavior
InterpretedPredicate evaluation behavior:

- Preserves existing partitioning as it only evaluates expressions row-wise
- Does not require shuffle operations
- Can be pushed down to individual partitions for local evaluation
- Commonly used in filter operations that can be applied per-partition

## Edge Cases

- Null handling depends entirely on the wrapped expression's null semantics
- If the wrapped expression returns null, casting to Boolean may throw ClassCastException
- Empty input behavior is handled at the operator level, not within the predicate itself
- Subexpression elimination state is managed per-partition through initialization

## Code Generation
This expression explicitly uses interpreted evaluation mode and does not support Tungsten code generation. It falls back to the eval() method for row-by-row interpretation. Code generation would typically use GeneratedPredicate instead of InterpretedPredicate.

## Examples
```scala
// Internal Catalyst usage example
val expr = EqualTo(col("age"), Literal(25))
val predicate = InterpretedPredicate(expr)
val result = predicate.eval(inputRow) // Returns Boolean
```

```scala
// Conceptual DataFrame operation that might use InterpretedPredicate internally
df.filter($"age" === 25) // May use InterpretedPredicate for the equality expression
```

## See Also

- BasePredicate - Parent abstract class
- GeneratedPredicate - Code-generated alternative
- ExpressionsEvaluator - Base evaluation interface
- SQLConf.subexpressionEliminationEnabled - Configuration flag for optimization