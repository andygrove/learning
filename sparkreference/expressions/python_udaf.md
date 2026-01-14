# PythonUDAF

## Overview
PythonUDAF represents a serialized Python lambda function for aggregation operations. This is a special expression that requires a dedicated physical operator for execution instead of using the standard Aggregate operator, enabling Python-based user-defined aggregate functions in Spark SQL.

## Syntax
```sql
-- SQL syntax (when registered)
python_udaf_name([DISTINCT] column1, column2, ...)
```

```scala
// DataFrame API usage
// Must be registered through PySpark API first
df.groupBy("group_col").agg(python_udaf_function(col("input_col")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| name | String | The name of the Python UDF function |
| func | PythonFunction | The serialized Python function implementation |
| dataType | DataType | The return data type of the aggregation |
| children | Seq[Expression] | Input expressions/columns to the aggregate function |
| udfDeterministic | Boolean | Whether the UDF produces deterministic results |
| evalType | Int | Evaluation type (defaults to SQL_GROUPED_AGG_PANDAS_UDF) |
| resultId | ExprId | Unique identifier for the expression result |

## Return Type
The return type is specified by the `dataType` parameter and can be any Spark SQL DataType supported by the Python function implementation.

## Supported Data Types
- All Spark SQL DataTypes are potentially supported depending on the Python function implementation
- Input types are determined by the `children` expressions
- Return type must be serializable between Python and Spark SQL
- Complex types (Arrays, Maps, Structs) supported through Arrow serialization

## Algorithm
- Serializes Python aggregate function for distributed execution
- Requires special physical operator (not standard Aggregate operator)
- Uses Pandas UDF evaluation by default (SQL_GROUPED_AGG_PANDAS_UDF)
- Leverages Arrow for efficient data transfer between JVM and Python
- Executes aggregation logic in Python worker processes

## Partitioning Behavior
How this expression affects partitioning:
- Preserves existing partitioning scheme
- May require shuffle for grouping operations (same as regular aggregates)
- Execution depends on the physical operator implementation
- Does not inherently change partition distribution

## Edge Cases
- **Null handling**: Behavior depends on Python function implementation
- **Empty input**: Returns result based on Python function's empty group handling
- **Deterministic flag**: Non-deterministic UDFs may produce different results across executions
- **Serialization failures**: Python function must be serializable across cluster nodes
- **Memory pressure**: Large intermediate states in Python workers can cause OOM

## Code Generation
This expression does **not** support Tungsten code generation. It falls back to interpreted mode because:
- Inherits from `UnevaluableAggregateFunc` 
- Requires Python interpreter execution
- Uses special physical operator for evaluation
- Cannot be compiled to Java bytecode due to Python dependency

## Examples
```sql
-- SQL usage (after registering UDAF in PySpark)
SELECT 
  category,
  my_python_udaf(DISTINCT value_col) as aggregated_result
FROM my_table 
GROUP BY category
```

```scala
// Scala DataFrame API (function must be created via PySpark)
import org.apache.spark.sql.functions._

// Assuming python_udaf was registered from PySpark
df.groupBy("category")
  .agg(expr("my_python_udaf(value_col)").as("result"))
```

## See Also
- `AggregateFunction` - Base interface for aggregate functions
- `PythonUDF` - Regular Python UDF (non-aggregate)
- `UnevaluableAggregateFunc` - Parent class for aggregates requiring special operators
- `PythonFunction` - Container for serialized Python functions