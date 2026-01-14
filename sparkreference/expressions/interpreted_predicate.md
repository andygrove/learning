# Spark Catalyst Predicate Expressions Reference

## InterpretedPredicate

### Overview
`InterpretedPredicate` is a concrete implementation of `BasePredicate` that evaluates expressions in interpreted mode rather than using code generation. It serves as a fallback mechanism when code generation is not available or disabled, providing a reliable way to evaluate boolean predicates using expression tree traversal.

### Syntax
```scala
// Internal usage - not directly accessible via SQL or DataFrame API
InterpretedPredicate(expression: Expression)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expression | Expression | The boolean expression to be evaluated in interpreted mode |

### Return Type
Returns `Boolean` values when evaluating predicates against input rows.

### Supported Data Types
Supports any expression that evaluates to `BooleanType`, including:
- Boolean literals and operations
- Comparison operations on numeric, string, date/timestamp types
- Complex predicates (AND, OR, NOT combinations)
- IN clauses and subqueries

### Algorithm
- Prepares expressions for evaluation with optional subexpression elimination
- Sets runtime input row context when subexpression elimination is enabled
- Evaluates the expression tree through recursive traversal
- Casts result to Boolean type for predicate evaluation
- Initializes expression state for partition-specific execution

### Partitioning Behavior
- Preserves partitioning as it only evaluates predicates without data movement
- Does not require shuffle operations
- Partition initialization is handled through `initializeExprs` method

### Edge Cases
- Null handling follows standard three-valued logic (true/false/null)
- Subexpression elimination can be enabled/disabled via `SQLConf.subexpressionEliminationEnabled`
- Falls back gracefully when code generation fails or is unavailable

### Code Generation
This expression explicitly **does not** use code generation - it's the interpreted fallback for when Tungsten code generation is not available or suitable.

### Examples
```scala
// Internal Catalyst usage example
val predicate = InterpretedPredicate(GreaterThan(col("age"), Literal(18)))
val result = predicate.eval(inputRow) // Returns Boolean
```

### See Also
- `GeneratePredicate` (code-generated counterpart)
- `BasePredicate` (base abstraction)
- `Predicate` (trait for boolean expressions)

---

## Not

### Overview
`Not` is a unary logical operator that performs boolean negation, implementing standard three-valued logic. It returns the logical inverse of its child expression, handling null values according to SQL semantics where NOT NULL evaluates to NULL.

### Syntax
```sql
NOT expression
```

```scala
// DataFrame API
col("column").unary_!
not(col("column"))
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | Boolean expression to negate |

### Return Type
`BooleanType`

### Supported Data Types
- Input: `BooleanType` only
- Uses implicit casting to convert compatible types

### Algorithm
- Validates input is boolean type through `ImplicitCastInputTypes`
- Applies boolean negation using `!` operator
- Preserves null values (NOT NULL = NULL)
- Optimizes during canonicalization by flipping comparison operators
- Generates efficient code using simple boolean negation

### Partitioning Behavior
- Preserves partitioning (no data movement required)
- Does not require shuffle operations
- Can be pushed down as a filter predicate

### Edge Cases
- `NOT NULL` returns `NULL` (three-valued logic)
- `NOT TRUE` returns `FALSE`
- `NOT FALSE` returns `TRUE`
- Canonicalization converts `NOT >` to `<=`, `NOT <` to `>=`, etc.

### Code Generation
Supports efficient code generation with simple boolean negation: `!($input)`

### Examples
```sql
SELECT NOT true;        -- false
SELECT NOT false;       -- true
SELECT NOT NULL;        -- NULL
SELECT * FROM table WHERE NOT (age > 65);
```

```scala
df.filter(not(col("active")))
df.select(col("flag").unary_!)
```

### See Also
- `And`, `Or` (other logical operators)
- `BinaryComparison` (expressions commonly negated)

---

## In

### Overview
`In` evaluates whether a value expression matches any value in a list of expressions. It implements SQL's IN predicate with three-valued logic, returning true if the value matches any list element, false if no matches and no nulls, or null if no matches but nulls are present.

### Syntax
```sql
expr IN (value1, value2, ...)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| value | Expression | The expression to test for membership |
| list | Seq[Expression] | List of expressions to check against |

### Return Type
`BooleanType`

### Supported Data Types
- All expressions must have the same data type (with structural equality)
- Supports orderable types (numeric, string, date/timestamp, arrays, structs)
- Does not support map types

### Algorithm
- Validates all expressions have compatible data types
- Short-circuits to false for empty lists (configurable legacy behavior)
- Evaluates value expression first
- Returns null immediately if value is null
- Iterates through list, comparing each element using ordering
- Returns true on first match, tracks null presence for final result
- Can be automatically optimized to `InSet` when all list values are literals

### Partitioning Behavior
- Preserves partitioning when used as filter predicate
- Eligible for predicate pushdown optimization
- Does not require data shuffling

### Edge Cases
- Empty IN list returns `false` (new behavior) or `null` if value is null (legacy)
- Null values in list contribute to null result when no match found
- NaN handling for floating-point types follows IEEE standards
- Legacy behavior controlled by `SQLConf.legacyNullInEmptyBehavior`

### Code Generation
Generates optimized code with early termination:
- Uses do-while loop structure for list evaluation
- Implements three-state result tracking (matched/not-matched/has-null)
- Splits large expressions across multiple functions to avoid 64KB method limit

### Examples
```sql
SELECT 1 IN (1, 2, 3);                    -- true
SELECT 1 IN (2, 3, 4);                    -- false  
SELECT 1 IN (2, 3, NULL);                 -- NULL
SELECT 'a' IN ('a', 'b', 'c');            -- true
SELECT struct(1,2) IN (struct(1,2), struct(3,4)); -- true
```

```scala
df.filter(col("status").isin("active", "pending"))
df.where(col("id").isin(1, 2, 3, 4, 5))
```

### See Also
- `InSet` (optimized version for literal values)
- `InSubquery` (for subquery expressions)
- `BinaryComparison` (related predicate expressions)

---

## InSet

### Overview
`InSet` is an optimized version of the IN predicate that uses hash-based lookup when all filter values are static literals. It provides O(1) average-case lookup performance compared to O(n) sequential scanning in the standard `In` expression, making it highly efficient for large value lists.

### Syntax
```sql
-- Automatically optimized from IN when all values are literals
expr IN (literal1, literal2, ...)
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The expression to test for membership |
| hset | Set[Any] | Precomputed hash set of literal values |

### Return Type
`BooleanType`

### Supported Data Types
- Same as `In` expression: orderable types excluding maps
- Special handling for string types with collation awareness
- Atomic types, null type, and complex types with interpreted ordering

### Algorithm
- Precomputes hash set from literal values during construction
- Uses specialized set implementations based on data type
- Implements O(1) hash-based lookup for membership testing
- Handles special cases for NaN values in floating-point types
- Optimizes code generation with switch statements for small integer sets
- Falls back to set-based lookup for larger or non-integer types

### Partitioning Behavior
- Preserves partitioning (filter-only operation)
- Highly efficient for predicate pushdown
- No shuffle operations required

### Edge Cases
- Empty set returns `false` (or follows legacy null behavior)
- Null value in input returns `null`
- NaN handling for float/double types with separate tracking
- String collation awareness through `CollationAwareSet`
- Switch statement optimization for integers ≤ configured threshold

### Code Generation
Multiple code generation strategies:
- **Switch statements**: For small integer sets (≤ `optimizerInSetSwitchThreshold`)
- **Hash set lookup**: For larger sets or non-integer types
- **Empty set**: Optimized constant false result

### Examples
```sql
-- These are automatically optimized to InSet
SELECT * FROM table WHERE id IN (1, 2, 3, 4, 5);
SELECT * FROM table WHERE status IN ('active', 'pending', 'inactive');
SELECT * FROM table WHERE price IN (9.99, 19.99, 29.99);
```

```scala
// DataFrame operations that become InSet
df.filter(col("category").isin("A", "B", "C"))
df.where(col("priority").isin(1, 2, 3))
```

### See Also
- `In` (general version for non-literal expressions)
- `CollationAwareSet` (for string collation handling)
- `SQLConf.optimizerInSetSwitchThreshold` (configuration)

---

## And

### Overview
`And` implements the logical AND operation following SQL's three-valued logic. It returns true only when both operands are true, false when either operand is false (regardless of the other's value), and null when the result is indeterminate due to null values.

### Syntax
```sql
expr1 AND expr2
```

```scala
col("expr1") && col("expr2")
col("expr1").and(col("expr2"))
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | Left boolean operand |
| right | Expression | Right boolean operand |

### Return Type
`BooleanType`

### Supported Data Types
- Both operands must be `BooleanType`
- Supports implicit casting from compatible types

### Algorithm
- Short-circuit evaluation: if left operand is false, returns false immediately
- Evaluates right operand only if left operand is not false
- Implements three-valued logic truth table for null handling
- Canonicalizes operand order for optimization
- Generates optimized code with early termination

### Partitioning Behavior
- Preserves partitioning when used in filter predicates
- Supports predicate pushdown optimization
- No shuffle operations required

### Edge Cases
- `FALSE AND NULL` = `FALSE` (short-circuit)
- `NULL AND FALSE` = `FALSE` (short-circuit) 
- `TRUE AND NULL` = `NULL`
- `NULL AND NULL` = `NULL`
- `TRUE AND TRUE` = `TRUE`

### Code Generation
Generates efficient short-circuit evaluation:
- Non-nullable case: Simple conditional evaluation
- Nullable case: Complex logic handling all null combinations
- Optimizes for cases where operands are known to be non-null

### Examples
```sql
SELECT true AND false;           -- false
SELECT true AND NULL;            -- NULL  
SELECT false AND NULL;          -- false
SELECT * FROM users WHERE age > 18 AND status = 'active';
```

```scala
df.filter(col("age") > 18 && col("active") === true)
df.where(col("salary").isNotNull.and(col("salary") > 50000))
```

### See Also
- `Or` (logical OR operator)
- `Not` (logical negation)
- `PredicateHelper.splitConjunctivePredicates` (optimization utility)

---

## Or

### Overview
`Or` implements the logical OR operation following SQL's three-valued logic. It returns true when either operand is true (regardless of the other's value), false only when both operands are false, and null when the result is indeterminate due to null values.

### Syntax
```sql
expr1 OR expr2
```

```scala
col("expr1") || col("expr2")
col("expr1").or(col("expr2"))
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | Left boolean operand |
| right | Expression | Right boolean operand |

### Return Type
`BooleanType`

### Supported Data Types
- Both operands must be `BooleanType`
- Supports implicit casting from compatible types

### Algorithm
- Short-circuit evaluation: if left operand is true, returns true immediately
- Evaluates right operand only if left operand is not true
- Implements three-valued logic truth table for null handling
- Canonicalizes operand order for optimization
- Generates optimized code with early termination

### Partitioning Behavior
- Preserves partitioning when used in filter predicates
- May limit predicate pushdown opportunities (OR conditions are harder to optimize)
- No shuffle operations required

### Edge Cases
- `TRUE OR NULL` = `TRUE` (short-circuit)
- `NULL OR TRUE` = `TRUE` (short-circuit)
- `FALSE OR NULL` = `NULL`
- `NULL OR NULL` = `NULL`
- `FALSE OR FALSE` = `FALSE`

### Code Generation
Generates efficient short-circuit evaluation:
- Non-nullable case: Simple conditional evaluation
- Nullable case: Complex logic handling all null combinations
- Optimizes for cases where operands are known to be non-null

### Examples
```sql
SELECT true OR false;            -- true
SELECT false OR NULL;           -- NULL
SELECT true OR NULL;            -- true
SELECT * FROM users WHERE age < 18 OR age > 65;
```

```scala
df.filter(col("priority") === "high" || col("urgent") === true)
df.where(col("discount").isNull.or(col("discount") > 0.1))
```

### See Also
- `And` (logical AND operator)
- `Not` (logical negation)
- `PredicateHelper.splitDisjunctivePredicates` (optimization utility)

---

## EqualTo

### Overview
`EqualTo` implements the standard SQL equality comparison operator using three-valued logic. It returns true when both operands are equal and non-null, false when they are unequal and non-null, and null when either operand is null.

### Syntax
```sql
expr1 = expr2
```

```scala
col("expr1") === col("expr2")
```

### Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | Left operand for comparison |
| right | Expression | Right operand for comparison |

### Return Type
`BooleanType`

### Supported Data Types
- Orderable types: numeric, string, date/timestamp, boolean
- Complex types (arrays, structs) with orderable field types
- Both operands must have structurally equivalent data types
- Does not support map types

### Algorithm
- Validates operands have compatible and orderable data types
- Uses null-intolerant evaluation (null inputs produce null output)
- Delegates to type-specific equality comparison via `Ordering.equiv`
- Canonicalizes operand order based on hash codes for optimization
- Generates efficient comparison code based on data type

### Partitioning Behavior
- Preserves partitioning when used in filter predicates
- Excellent for predicate pushdown optimization
- Supports partition pruning when comparing partition columns
- No shuffle operations required

### Edge Cases
- `NULL = anything` returns `NULL` (three-valued logic)
- String comparisons respect collation settings
- Floating-point NaN values follow IEEE standards
- Complex type comparisons are recursive (field-by-field)

### Code Generation
Optimized code generation strategies:
- Primitive types: Direct comparison operators (`==`)
- Non-primitive types: Generated comparison functions
- Special handling for floating-point and boolean types

### Examples
```sql
SELECT 2 = 2;                    -- true
SELECT 1 = '1';                  -- true (with casting)
SELECT true = NULL;              -- NULL
SELECT array(1,2) = array(1,2);  -- true
```

```scala
df.filter(col("status") === "active")
df.where(col("id") === col("parent_id"))
df.select(col("name") === col("alias"))
```

### See Also
- `EqualNullSafe` (null-safe equality)
- `BinaryComparison`