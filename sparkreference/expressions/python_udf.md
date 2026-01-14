# PythonUDF

## Overview
PythonUDF represents a serialized Python lambda function that can be executed within Spark SQL expressions. It serves as a bridge between Spark's Catalyst optimizer and Python user-defined functions, requiring dedicated physical operators for execution and cannot be pushed down to data sources.

## Syntax
```sql
-- SQL syntax (registered UDF)
SELECT my_python_udf(column1, column2) FROM table

-- DataFrame API
import pyspark.sql.functions as F
df.select(F.udf(python_function, return_type)(*columns))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| name | String | Name of the Python function |
| func | PythonFunction | Serialized Python function containing code and environment |
| dataType | DataType | Expected return data type of the function |
| children | Seq[Expression] | Input expressions/columns to pass to the function |
| evalType | Int | Evaluation type from PythonEvalType (batched, Arrow, Pandas, etc.) |
| udfDeterministic | Boolean | Whether the UDF is deterministic for optimization |
| resultId | ExprId | Unique identifier for this expression instance |

## Return Type
Returns the specified `dataType` parameter. The expression is always nullable regardless of the specified data type.

## Supported Data Types
- **Input**: All Spark SQL data types including primitives, arrays, structs, and maps
- **Output**: All Spark SQL data types 
- **Special handling**: User-defined types (UDTs) may fallback from Arrow to regular batched evaluation
- **Arrow compatibility**: Most types support Arrow format except UDTs when `pythonUDFArrowFallbackOnUDT` is enabled

## Algorithm
- Serializes Python function code and environment into `PythonFunction` object
- Batches input rows according to the specified `evalType` (regular batching, Arrow, or Pandas)
- Executes Python function in separate Python worker processes
- Deserializes results back to Catalyst internal representation
- Supports multiple evaluation strategies: SQL_BATCHED_UDF, SQL_ARROW_BATCHED_UDF, SQL_SCALAR_PANDAS_UDF, etc.
- Automatically falls back from Arrow to regular batching for UDTs when configured

## Partitioning Behavior
- **Preserves partitioning**: Yes, PythonUDF operations maintain existing data partitioning
- **Requires shuffle**: No, evaluation happens locally on each partition
- **Execution**: Requires dedicated physical operators (ArrowEvalPythonExec, BatchEvalPythonExec) rather than columnar processing
- **Barrier execution**: May use barrier mode for certain evaluation types to ensure process synchronization

## Edge Cases
- **Null handling**: Always returns nullable results; null handling depends on Python function implementation
- **Empty partitions**: Handled gracefully, Python workers receive empty batches
- **UDT fallback**: Automatically switches from Arrow to batched evaluation for User-Defined Types
- **Deterministic behavior**: Overall determinism depends on both `udfDeterministic` flag and determinism of child expressions
- **Error propagation**: Python exceptions are captured and re-raised as Spark exceptions

## Code Generation
This expression does **not** support code generation (Tungsten). It extends `Unevaluable` trait, meaning:
- No `eval()` method implementation
- No `doGenCode()` method implementation  
- Always requires interpretation through dedicated Python execution operators
- Cannot be used in generated code paths

## Examples
```sql
-- Register and use Python UDF
CREATE OR REPLACE TEMPORARY VIEW my_table AS SELECT 1 as id, 'hello' as text;
-- (Python UDF registration happens in Python/PySpark layer)
SELECT my_python_udf(id, text) FROM my_table;
```

```scala
// DataFrame API usage (typically from PySpark)
import org.apache.spark.sql.functions._
import org.apache.spark.api.python.PythonFunction

// This is typically created internally by PySpark
val pythonUDF = PythonUDF(
  name = "my_function",
  func = pythonFunction, // PythonFunction object
  dataType = StringType,
  children = Seq(col("input_column")),
  evalType = PythonEvalType.SQL_BATCHED_UDF,
  udfDeterministic = true
)
```

## See Also
- **PythonUDAF**: Python user-defined aggregate functions
- **PythonUDTF**: Python user-defined table functions  
- **PythonFuncExpression**: Base trait for all Python function expressions
- **ArrowEvalPythonExec**: Physical operator for Arrow-based Python UDF execution
- **BatchEvalPythonExec**: Physical operator for regular batched Python UDF execution