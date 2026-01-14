# VectorInnerProduct

## Overview

The `VectorInnerProduct` expression computes the inner (dot) product of two float vectors represented as arrays. This is a runtime replaceable expression that delegates the actual computation to `VectorFunctionImplUtils.vectorInnerProduct` method for optimized vector operations.

## Syntax

```sql
vector_inner_product(array1, array2)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("vector_inner_product(vector1, vector2)"))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| left | Array[Float] | The first float vector/array |
| right | Array[Float] | The second float vector/array |

## Return Type

`FloatType` - Returns a single float value representing the inner product of the two input vectors.

## Supported Data Types

This expression only supports:

- Input: `ArrayType(FloatType, _)` for both arguments
- Output: `FloatType`

Any other input data types will result in a `DataTypeMismatch` error with the `UNEXPECTED_INPUT_TYPE` error subclass.

## Algorithm

The expression evaluation follows these steps:

- Validates that both input expressions are arrays of float type
- Delegates to `VectorFunctionImplUtils.vectorInnerProduct` via `StaticInvoke`
- The static method computes the dot product: Σ(left[i] * right[i]) for all valid indices
- Returns the computed scalar result as a float value
- Includes the pretty name "vector_inner_product" for error reporting context

## Partitioning Behavior

This expression has neutral partitioning behavior:

- Preserves existing partitioning as it operates row-wise on individual records
- Does not require shuffle operations since computation is local to each row
- Can be pushed down and executed in parallel across partitions

## Edge Cases

- **Null handling**: Behavior depends on the underlying `VectorFunctionImplUtils.vectorInnerProduct` implementation
- **Mismatched array lengths**: Error handling delegated to the runtime implementation
- **Empty arrays**: Likely returns 0.0, but depends on the utility method implementation
- **NaN/Infinity values**: Standard IEEE 754 floating-point arithmetic rules apply
- **Type validation**: Strict type checking - only `Array[Float]` accepted for both inputs

## Code Generation

This expression uses `StaticInvoke` for code generation, which:

- Generates efficient bytecode that directly calls the static utility method
- Supports Tungsten code generation for optimized execution
- Avoids interpreted expression evaluation overhead
- Provides better performance for vector operations

## Examples

```sql
-- Calculate inner product of two feature vectors
SELECT vector_inner_product(
  array(1.0, 2.0, 3.0), 
  array(4.0, 5.0, 6.0)
) AS dot_product;
-- Result: 32.0 (1*4 + 2*5 + 3*6)

-- Use with table columns
SELECT id, vector_inner_product(features1, features2) as similarity
FROM vectors_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.createDataFrame(Seq(
  (Array(1.0f, 2.0f, 3.0f), Array(4.0f, 5.0f, 6.0f)),
  (Array(1.0f, 0.0f), Array(0.0f, 1.0f))
)).toDF("vec1", "vec2")

df.select(expr("vector_inner_product(vec1, vec2)").as("dot_product")).show()
```

## See Also

- Vector similarity functions
- Array aggregation functions  
- Mathematical expressions for arrays
- `VectorFunctionImplUtils` utility class