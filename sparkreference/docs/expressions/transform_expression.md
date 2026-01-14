# TransformExpression

## Overview
`TransformExpression` is a Spark Catalyst expression that represents partition transform functions used in partitioned tables. It wraps a `BoundFunction` and provides compatibility checking between transform expressions to enable optimizations like storage-partitioned joins.

## Syntax
This expression is primarily used internally by Spark for partition transforms and is not directly accessible through SQL or DataFrame API. It represents transforms like:
```sql
-- Examples of underlying transforms this expression represents
bucket(32, column)
year(date_column)
month(date_column)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| function | BoundFunction | The transform function itself used for compatibility decisions |
| children | Seq[Expression] | Child expressions that provide input values |
| numBucketsOpt | Option[Int] | Number of buckets for bucket transforms, None for other transforms |

## Return Type
The return type is determined by the underlying `BoundFunction.resultType()`. The expression is always nullable regardless of input nullability.

## Supported Data Types
Supported data types depend on the underlying `BoundFunction`:

- Bucket transforms: typically numeric and string types
- Date/time transforms (year, month, day, hour): timestamp and date types
- Identity transforms: any data type

## Algorithm
The expression evaluation follows these steps:

- Attempts to resolve the function as a `ScalarFunction` using `V2ExpressionUtils`
- For bucket transforms, prepends the number of buckets as a literal argument
- Evaluates the resolved scalar function against the input row
- Throws `QueryExecutionError` if the function cannot be resolved or evaluated
- Falls back to interpreted mode as code generation is not supported

## Partitioning Behavior
This expression is specifically designed for partitioning operations:

- Preserves partitioning when used in partition schemes
- Enables storage-partitioned joins when compatible transforms are detected
- Compatible transforms can avoid shuffle operations in join scenarios
- Function compatibility is determined through `ReducibleFunction` relationships

## Edge Cases

- **Null handling**: Expression is always nullable and returns null for null inputs
- **Function resolution failure**: Throws `QueryExecutionError` if the underlying function cannot be resolved
- **Incompatible functions**: Non-reducible functions are never considered compatible
- **Bucket mismatch**: Bucket transforms with different bucket counts are incompatible unless reducible
- **Code generation**: Always falls back to interpreted mode, throws error if code generation is attempted

## Code Generation
This expression does not support Tungsten code generation and always throws a `QueryExecutionError` when `doGenCode` is called. All evaluation is performed in interpreted mode through the resolved scalar function.

## Examples
```scala
// Internal usage - not directly accessible via public APIs
// Represents partition transforms in table definitions

// Bucket transform with 32 buckets
TransformExpression(
  bucketFunction, 
  Seq(col("user_id")), 
  Some(32)
)

// Year transform for date partitioning
TransformExpression(
  yearFunction, 
  Seq(col("created_date")), 
  None
)
```

## See Also

- `BoundFunction` - The underlying function interface
- `ReducibleFunction` - Interface for compatible transform functions
- `ScalarFunction` - Scalar function implementations used for evaluation
- `V2ExpressionUtils` - Utility for resolving scalar functions
- Storage-partitioned joins optimization