# VectorCosineSimilarity

## Overview
The `VectorCosineSimilarity` expression computes the cosine similarity between two float arrays (vectors). This expression is implemented as a `RuntimeReplaceable` that delegates to the `VectorFunctionImplUtils.vectorCosineSimilarity` method at runtime.

## Syntax
```sql
vector_cosine_similarity(array1, array2)
```

```scala
// DataFrame API
col("vector1").function("vector_cosine_similarity", col("vector2"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | `array<float>` | The first vector (array of float values) |
| right | `array<float>` | The second vector (array of float values) |

## Return Type
`float` - Returns a float value representing the cosine similarity between the two input vectors.

## Supported Data Types

- Input: `array<float>` only
- Both left and right expressions must be arrays of float type
- No automatic type coercion is performed

## Algorithm

- Validates that both inputs are arrays of float type during analysis phase
- Delegates actual computation to `VectorFunctionImplUtils.vectorCosineSimilarity` at runtime
- Uses `StaticInvoke` to call the external implementation method
- Passes the expression's pretty name as an additional parameter for error reporting
- Type checking occurs before code generation, ensuring type safety

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffling
- Can be computed independently on each partition
- Row-level operation that doesn't affect data distribution

## Edge Cases

- **Type mismatch**: Throws `DataTypeMismatch` error with `UNEXPECTED_INPUT_TYPE` subclass if inputs are not `array<float>`
- **Null handling**: Null behavior is handled by the underlying `VectorFunctionImplUtils` implementation
- **Array length mismatch**: Error handling depends on the runtime implementation
- **Empty arrays**: Behavior determined by the runtime utility method
- **Zero vectors**: May result in undefined cosine similarity (division by zero in magnitude calculation)

## Code Generation
This expression uses runtime replacement pattern:

- Does not generate inline code during Catalyst code generation
- Uses `StaticInvoke` to call pre-compiled Java method
- Falls back to interpreted execution through method invocation
- The actual computation is handled by `VectorFunctionImplUtils.vectorCosineSimilarity`

## Examples
```sql
-- Calculate cosine similarity between two feature vectors
SELECT vector_cosine_similarity(
  array(1.0, 2.0, 3.0), 
  array(4.0, 5.0, 6.0)
) AS similarity;

-- Use with table columns
SELECT id, vector_cosine_similarity(features1, features2) AS sim
FROM vectors_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(
  expr("vector_cosine_similarity(vector_col1, vector_col2)").alias("similarity")
)

// With literal arrays
df.select(
  expr("vector_cosine_similarity(array(1.0f, 2.0f), array(3.0f, 4.0f))")
)
```

## See Also

- Other vector functions in the `vector_funcs` group
- `ArrayType` expressions for array manipulation
- `StaticInvoke` for understanding runtime replacement patterns
- `VectorFunctionImplUtils` for the actual implementation details