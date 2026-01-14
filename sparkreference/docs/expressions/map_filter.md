# MapFilter

## Overview
MapFilter is a higher-order function that filters map entries based on a lambda predicate function. It applies the provided lambda function to each key-value pair in the input map and returns a new map containing only the entries where the predicate evaluates to true.

## Syntax
```sql
map_filter(map_expression, lambda_function)
```

```scala
// DataFrame API usage
map_filter(col("map_column"), (k, v) => k > v)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| map_expression | MapType | The input map to be filtered |
| lambda_function | Lambda | A function that takes two parameters (key, value) and returns a boolean |

## Return Type
Returns a MapType with the same key and value types as the input map, containing only the entries that satisfy the predicate condition.

## Supported Data Types

- Input map can have keys and values of any supported Spark SQL data type
- The lambda function must return a boolean expression
- Key and value types are preserved in the output map

## Algorithm

- Iterates through each key-value pair in the input map
- Applies the lambda function to each pair, passing key as first argument and value as second argument  
- Evaluates the lambda function result as a boolean predicate
- Includes the key-value pair in the result map only if the predicate returns true
- Constructs and returns a new map with the filtered entries

## Partitioning Behavior
How this expression affects partitioning:

- Preserves existing partitioning since it operates row-by-row
- Does not require shuffle operations
- Can be applied as a projection without repartitioning

## Edge Cases

- If input map is null, returns null
- If lambda function returns null for a key-value pair, that pair is excluded (treated as false)
- Empty input map returns empty map of the same type
- Lambda function exceptions will cause the entire expression to fail
- Maintains original key and value data types in filtered result

## Code Generation
This expression supports Catalyst code generation (Tungsten) for optimized runtime performance when the lambda function can be code-generated.

## Examples
```sql
-- Filter map entries where key is greater than value
SELECT map_filter(map(1, 0, 2, 2, 3, -1), (k, v) -> k > v);
-- Returns: {1:0, 3:-1}

-- Filter string map by key length
SELECT map_filter(map('a', 'apple', 'bb', 'banana'), (k, v) -> length(k) > 1);
-- Returns: {'bb':'banana'}
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(map_filter(col("data_map"), (k, v) => k > v))

// Filter nested map column
df.withColumn("filtered_map", 
  map_filter(col("original_map"), (key, value) => key.isNotNull && value > 0))
```

## See Also

- `map_zip_with` - applies a function to corresponding pairs from two maps
- `transform_keys` - transforms map keys using a lambda function  
- `transform_values` - transforms map values using a lambda function
- `filter` - filters array elements using a predicate function