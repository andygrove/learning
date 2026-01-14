# TransformValues

## Overview
The `TransformValues` expression applies a lambda function to each value in a map while preserving the original keys. This higher-order function transforms map values according to the provided lambda expression, creating a new map with the same keys but modified values.

## Syntax
```sql
transform_values(map_expr, lambda_function)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| map_expr | MapType | The input map whose values will be transformed |
| lambda_function | LambdaFunction | A lambda function that takes (key, value) parameters and returns the transformed value |

## Return Type
Returns a `MapType` with the same key type as the input map, but potentially different value type based on the lambda function's return type.

## Supported Data Types

- Input map can have any valid MapType with supported key and value types
- Lambda function can return any supported Spark SQL data type
- Keys must be of a type that supports map operations (non-null, hashable types)

## Algorithm

- Iterates through each key-value pair in the input map
- Applies the lambda function to each (key, value) pair
- Preserves the original keys in their exact form
- Collects transformed values and constructs a new map
- Maintains the original map's structure and ordering properties

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be executed locally on each partition

## Edge Cases

- Null input map returns null
- Empty map returns empty map with same type signature
- If lambda function returns null for any value, that key-value pair will have null as the value
- Lambda function exceptions will propagate and cause query failure
- Duplicate keys are handled according to standard map semantics

## Code Generation
This expression supports Spark's Tungsten code generation for optimized execution when the lambda function and map operations can be compiled to efficient Java bytecode.

## Examples
```sql
-- Transform values by adding key to value
SELECT transform_values(map_from_arrays(array(1, 2, 3), array(1, 2, 3)), (k, v) -> k + v);
-- Result: {1:2, 2:4, 3:6}

-- Transform string values to uppercase
SELECT transform_values(map('a', 'hello', 'b', 'world'), (k, v) -> upper(v));
-- Result: {'a':'HELLO', 'b':'WORLD'}
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(transform_values(col("map_column"), (k, v) => k + v))

// Using SQL expression
df.selectExpr("transform_values(map_column, (k, v) -> k + v)")
```

## See Also

- `transform_keys` - transforms map keys instead of values
- `map_from_arrays` - creates maps from key and value arrays
- `map_filter` - filters map entries based on conditions
- `aggregate` - general aggregation with lambda functions