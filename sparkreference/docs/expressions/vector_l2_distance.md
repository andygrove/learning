# VectorL2Distance

## Overview
The `VectorL2Distance` expression computes the L2 (Euclidean) distance between two float vector arrays. This is a runtime-replaceable expression that delegates the actual computation to the `VectorFunctionImplUtils.vectorL2Distance` method through static invocation.

## Syntax
```sql
vector_l2_distance(array1, array2)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Array[Float] | The first float array vector |
| right | Array[Float] | The second float array vector |

## Return Type
`FloatType` - Returns a single float value representing the L2 distance between the two input vectors.

## Supported Data Types
This expression only supports:

- Input arrays must be of type `ArrayType(FloatType, _)` for both left and right expressions
- No other numeric types (Double, Integer, etc.) are supported
- Both arrays must contain float elements

## Algorithm
The expression uses a runtime replacement pattern for evaluation:

- Validates that both input expressions are float arrays during type checking
- Delegates actual computation to `VectorFunctionImplUtils.vectorL2Distance` via `StaticInvoke`
- Passes the left array, right array, and expression name ("vector_l2_distance") as parameters
- The underlying implementation computes the Euclidean distance between the two vectors

## Partitioning Behavior
This expression has neutral partitioning behavior:

- Preserves existing partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be evaluated independently on each partition

## Edge Cases

- **Null handling**: Behavior depends on the underlying `VectorFunctionImplUtils.vectorL2Distance` implementation
- **Array length mismatch**: Runtime behavior is determined by the static invocation target
- **Empty arrays**: Handling is delegated to the underlying utility method
- **Type validation**: Strict type checking ensures only float arrays are accepted, with specific error messages for mismatched types

## Code Generation
This expression uses runtime replacement rather than direct code generation:

- Implements `RuntimeReplaceable` interface
- Replaces itself with a `StaticInvoke` expression during query planning
- The `StaticInvoke` expression may support code generation depending on Spark's capabilities for static method calls

## Examples
```sql
-- Calculate L2 distance between two float vectors
SELECT vector_l2_distance(array(1.0, 2.0, 3.0), array(4.0, 5.0, 6.0)) as distance;

-- Use in WHERE clause for similarity search
SELECT id, features 
FROM vectors_table 
WHERE vector_l2_distance(features, array(1.0, 0.0, 1.0)) < 2.0;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("vector_l2_distance(vector1, vector2)").as("distance"))

// With column references
df.withColumn("similarity", 
  expr("vector_l2_distance(features, reference_vector)"))
```

## See Also

- Other vector distance functions in the `vector_funcs` group
- `VectorFunctionImplUtils` class for underlying implementation details
- `StaticInvoke` expression for runtime replacement pattern