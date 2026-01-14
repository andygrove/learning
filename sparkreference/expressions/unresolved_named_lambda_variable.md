# Higher Order Functions Reference

## Overview

Higher order functions are Spark SQL expressions that take lambda functions as parameters and apply them to complex data structures like arrays and maps. They enable functional programming patterns for transforming, filtering, and aggregating collection data types within SQL expressions.

---

# UnresolvedNamedLambdaVariable

## Overview
A placeholder for lambda variables during the parsing phase that prevents premature resolution of lambda functions. This is an internal expression used during SQL analysis before lambda variables are properly bound to their corresponding lambda functions.

## Syntax
```sql
-- Internal representation only, not directly used in SQL
lambda 'variable_name
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| nameParts | Seq[String] | The qualified name parts of the lambda variable |

## Return Type
This is an unresolved expression that throws `UnresolvedException` for all type-related operations.

## Supported Data Types
Not applicable - this is a placeholder expression that must be resolved before evaluation.

## Algorithm
- Acts as a placeholder during parsing phase
- Prevents unexpected resolution of lambda functions
- Must be resolved to `NamedLambdaVariable` before execution
- Throws `UnresolvedException` for any evaluation attempts

## Partitioning Behavior
Not applicable - expression is resolved before execution.

## Edge Cases
- Always marked as unresolved (`resolved = false`)
- All data type and evaluation methods throw `UnresolvedException`
- Uses atomic counter to generate unique variable names

## Code Generation
Not applicable - must be resolved before code generation phase.

## Examples
```scala
// Internal usage during parsing - not exposed to users
val unresolvedVar = UnresolvedNamedLambdaVariable(Seq("x"))
```

## See Also
- `NamedLambdaVariable`
- `LambdaFunction`

---

# NamedLambdaVariable

## Overview
A resolved lambda variable that represents a parameter in a lambda function. It holds a reference to a value that is set during lambda function evaluation and provides type information for the bound variable.

## Syntax
```sql
-- Used within lambda expressions
x -> x + 1  -- 'x' becomes a NamedLambdaVariable
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| name | String | The variable name |
| dataType | DataType | The data type of the variable |
| nullable | Boolean | Whether the variable can be null |
| exprId | ExprId | Unique expression identifier |
| value | AtomicReference[Any] | Thread-safe value holder |

## Return Type
Returns the data type specified in the variable definition.

## Supported Data Types
Can represent any Spark SQL data type based on the lambda function context.

## Algorithm
- Stores current value in atomic reference for thread safety
- Evaluation returns the currently set value
- Value is set by the containing higher-order function
- Maintains expression ID for reference tracking

## Partitioning Behavior
Does not affect partitioning - variables are local to lambda function scope.

## Edge Cases
- Value can be null if the variable is nullable
- Must be properly initialized by higher-order function
- Falls back to interpreted evaluation (CodegenFallback)

## Code Generation
Uses CodegenFallback - does not generate optimized code.

## Examples
```scala
// Internal representation - created during lambda binding
val variable = NamedLambdaVariable("x", IntegerType, nullable = false)
```

## See Also
- `LambdaFunction`
- `HigherOrderFunction`

---

# LambdaFunction

## Overview
Represents a lambda function with its body expression and parameter variables. Lambda functions are used as arguments to higher-order functions to define custom transformation logic on collection elements.

## Syntax
```sql
-- Single parameter lambda
x -> x + 1

-- Multiple parameter lambda  
(x, y) -> x + y

-- Lambda with complex expression
x -> CASE WHEN x > 0 THEN x * 2 ELSE 0 END
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| function | Expression | The lambda body expression |
| arguments | Seq[NamedExpression] | Lambda parameter variables |
| hidden | Boolean | Whether lambda is hidden for internal use |

## Return Type
Returns the same data type as the lambda body expression.

## Supported Data Types
Body expression can return any Spark SQL data type.

## Algorithm
- Contains the lambda body expression and parameter variables
- Parameters are bound during higher-order function analysis
- Evaluation delegates to the body expression
- References are tracked to prevent variable scope issues

## Partitioning Behavior
Does not directly affect partitioning - behavior depends on containing higher-order function.

## Edge Cases
- Must be bound before evaluation (all arguments resolved)
- References are filtered to exclude lambda parameters
- Identity lambda function available as `LambdaFunction.identity`

## Code Generation
Uses CodegenFallback - does not generate optimized code.

## Examples
```sql
-- Used within higher-order functions
SELECT transform(array(1,2,3), x -> x * 2);
SELECT filter(array(1,2,3,4), x -> x % 2 = 0);
```

## See Also
- `HigherOrderFunction`
- `NamedLambdaVariable`

---

# ArrayTransform

## Overview
Transforms elements in an array by applying a lambda function to each element, similar to a functional map operation. Supports both single-parameter and two-parameter lambda functions (element and index).

## Syntax
```sql
transform(array_expr, lambda_function)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| argument | Expression | Input array expression |
| function | Expression | Lambda function to apply |

## Return Type
`ArrayType` with element type matching the lambda function return type.

## Supported Data Types
- Input: Any `ArrayType`
- Lambda can return any data type

## Algorithm
- Iterates through each array element
- Sets lambda variable to current element value
- Optionally sets index variable if lambda has two parameters  
- Evaluates lambda function for each element
- Copies result values to new array

## Partitioning Behavior
- Preserves input partitioning
- No shuffle required
- Element-wise transformation

## Edge Cases
- Null input array returns null
- Null elements are passed to lambda function
- Result array size matches input array size
- Index parameter (if used) starts from 0

## Code Generation
Uses CodegenFallback - interpreted evaluation only.

## Examples
```sql
-- Single parameter - transform elements
SELECT transform(array(1, 2, 3), x -> x + 1);
-- Result: [2, 3, 4]

-- Two parameters - element and index
SELECT transform(array(1, 2, 3), (x, i) -> x + i);
-- Result: [1, 3, 5]
```

```scala
// DataFrame API
df.select(transform(col("array_col"), x => x + 1))
```

## See Also
- `ArrayFilter`
- `ArrayAggregate`

---

# ArraySort

## Overview
Sorts elements in an array using either natural ordering (for orderable types) or a custom comparator lambda function. Null elements are placed at the end of the result array.

## Syntax
```sql
array_sort(array_expr)
array_sort(array_expr, comparator_lambda)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| argument | Expression | Input array expression |
| function | Expression | Optional comparator lambda function |
| allowNullComparisonResult | Boolean | Whether to allow null comparator results |

## Return Type
Same `ArrayType` as input array.

## Supported Data Types
- Input: Any `ArrayType` with orderable element type (if no comparator)
- Comparator lambda must return `IntegerType`

## Algorithm
- Uses Java Arrays.sort() with custom comparator
- Default comparator handles null values (nulls last)
- Custom comparator receives two elements as parameters
- Comparator returns negative/zero/positive for less/equal/greater
- NaN values are greater than non-NaN for float/double types

## Partitioning Behavior
- Preserves input partitioning  
- No shuffle required
- In-place sorting operation

## Edge Cases
- Null input array returns null
- Null elements sorted to end by default comparator
- Comparator returning null throws error (unless legacy flag set)
- Empty arrays return empty arrays

## Code Generation
Uses CodegenFallback - interpreted evaluation only.

## Examples
```sql
-- Default ascending sort
SELECT array_sort(array('b', 'd', null, 'c', 'a'));
-- Result: ["a", "b", "c", "d", null]

-- Custom comparator - ascending
SELECT array_sort(array(5, 6, 1), (left, right) -> 
  case when left < right then -1 
       when left > right then 1 
       else 0 end);
-- Result: [1, 5, 6]

-- Custom comparator - descending  
SELECT array_sort(array('bc', 'ab', 'dc'), (left, right) ->
  case when left < right then 1
       when left > right then -1
       else 0 end);
-- Result: ["dc", "bc", "ab"]
```

## See Also
- `ArrayTransform`
- Default comparator logic in `ArraySort.comparator`

---

# MapFilter

## Overview
Filters entries in a map by applying a predicate lambda function to each key-value pair. Only entries where the predicate returns true are included in the result map.

## Syntax
```sql
map_filter(map_expr, predicate_lambda)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| argument | Expression | Input map expression |
| function | Expression | Predicate lambda function |

## Return Type
Same `MapType` as input map.

## Supported Data Types
- Input: Any `MapType`
- Lambda function must return `BooleanType`

## Algorithm
- Iterates through each map entry (key-value pair)
- Sets lambda variables to current key and value
- Evaluates predicate lambda function
- Includes entry in result if predicate returns true
- Builds result map from filtered entries

## Partitioning Behavior
- Preserves input partitioning
- No shuffle required  
- Entry-wise filtering operation

## Edge Cases
- Null input map returns null
- Null keys/values are passed to lambda function
- Empty result if no entries match predicate
- Predicate returning null treated as false

## Code Generation
Uses CodegenFallback - interpreted evaluation only.

## Examples
```sql
-- Filter entries where key > value
SELECT map_filter(map(1, 0, 2, 2, 3, -1), (k, v) -> k > v);
-- Result: {1:0, 3:-1}

-- Filter entries with non-null values
SELECT map_filter(map('a', 1, 'b', null, 'c', 3), (k, v) -> v IS NOT NULL);
-- Result: {'a':1, 'c':3}
```

## See Also
- `ArrayFilter`
- `TransformKeys`
- `TransformValues`

---

# ArrayFilter

## Overview
Filters elements in an array using a predicate lambda function. Supports both single-parameter (element only) and two-parameter (element and index) lambda functions.

## Syntax
```sql
filter(array_expr, predicate_lambda)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| argument | Expression | Input array expression |
| function | Expression | Predicate lambda function |

## Return Type
Same `ArrayType` as input array.

## Supported Data Types
- Input: Any `ArrayType`
- Lambda function must return `BooleanType`

## Algorithm
- Iterates through each array element with index
- Sets element variable to current element value
- Optionally sets index variable if lambda has two parameters
- Evaluates predicate lambda function
- Includes element in result if predicate returns true
- Uses mutable ArrayBuffer for efficient result building

## Partitioning Behavior
- Preserves input partitioning
- No shuffle required
- Element-wise filtering operation

## Edge Cases
- Null input array returns null
- Null elements are passed to lambda function
- Result array may be shorter than input
- Index parameter (if used) reflects original array positions

## Code Generation
Uses CodegenFallback - interpreted evaluation only.

## Examples
```sql
-- Filter odd numbers
SELECT filter(array(1, 2, 3), x -> x % 2 == 1);
-- Result: [1, 3]

-- Filter with index - elements greater than their index
SELECT filter(array(0, 2, 3), (x, i) -> x > i);
-- Result: [2, 3]

-- Filter non-null elements
SELECT filter(array(0, null, 2, 3, null), x -> x IS NOT NULL);
-- Result: [0, 2, 3]
```

## See Also
- `ArrayTransform`
- `ArrayExists`
- `ArrayForAll`

---

# ArrayExists

## Overview
Tests whether a predicate holds for one or more elements in an array. Returns true if at least one element satisfies the predicate, with configurable three-valued logic handling.

## Syntax
```sql
exists(array_expr, predicate_lambda)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| argument | Expression | Input array expression |
| function | Expression | Predicate lambda function |
| followThreeValuedLogic | Boolean | Whether to follow SQL three-valued logic |

## Return Type
`BooleanType` (nullable based on configuration)

## Supported Data Types
- Input: Any `ArrayType`
- Lambda function must return `BooleanType`

## Algorithm
- Iterates through array elements until predicate returns true
- Short-circuits on first true result
- Tracks null predicate results for three-valued logic
- Returns true if any element satisfies predicate
- Returns null if no true found but null encountered (if three-valued logic enabled)

## Partitioning Behavior
- Preserves input partitioning
- No shuffle required
- Short-circuiting evaluation

## Edge Cases
- Null input array returns null
- Empty array returns false
- Three-valued logic: true > null > false precedence
- Legacy mode ignores null predicate results

## Code Generation
Uses CodegenFallback - interpreted evaluation only.

## Examples
```sql
-- Check if any even numbers exist
SELECT exists(array(1, 2, 3), x -> x % 2 == 0);
-- Result: true

-- Check for impossible condition
SELECT exists(array(1, 2, 3), x -> x % 2 == 10);
-- Result: false

-- Three-valued logic with nulls
SELECT exists(array(1, null, 3), x -> x % 2 == 0);
-- Result: NULL (with three-valued logic)

-- Check for null elements
SELECT exists(array(0, null, 2, 3, null), x -> x IS NULL);
-- Result: true
```

## See Also
- `ArrayForAll`
- `ArrayFilter`

---

# ArrayForAll

## Overview
Tests whether a predicate holds for all elements in an array. Returns true only if every element satisfies the predicate, following three-valued logic for null handling.

## Syntax
```sql
forall(array_expr, predicate_lambda)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| argument | Expression | Input array expression |
| function | Expression | Predicate lambda function |

## Return Type
`BooleanType` (nullable)

## Supported Data Types
- Input: Any `ArrayType`
- Lambda function must return `BooleanType`

## Algorithm
- Iterates through array elements until predicate returns false
- Short-circuits on first false result
- Tracks null predicate results
- Returns false if any element fails predicate
- Returns null if all non-null satisfy but nulls encountered
- Returns true only if all elements satisfy predicate

## Partitioning Behavior
- Preserves input partitioning
- No shuffle required
- Short-circuiting evaluation

## Edge Cases
- Null input array returns null
- Empty array returns true (vacuous truth)
- Null predicate results affect final outcome
- Three-valued logic: false > null > true precedence

## Code Generation
Uses CodegenFallback - interpreted evaluation only.

## Examples
```sql
-- Check if all numbers are even
SELECT forall(array(1, 2, 3), x -> x % 2 == 0);
-- Result: false

-- Check if all even numbers are even
SELECT forall(array(2, 4, 8), x -> x % 2 == 0);