# PythonUDF

## Overview
PythonUDF represents a serialized version of a Python lambda function within Spark's Catalyst expression tree. This is a special expression that requires a dedicated physical operator for execution and cannot be pushed down to data sources due to its Python runtime dependency.

## Syntax
```python
# Register a Python UDF
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType

my_udf = udf(lambda x: x * 2, IntegerType())
df.select(my_udf(df.column_name))
```

```scala
// Scala DataFrame API (using registered Python UDF)
df.selectExpr("my_python_udf(column_name)")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| name | String | The name identifier of the Python UDF |
| func | PythonFunction | The serialized Python function object containing the lambda logic |
| dataType | DataType | The Spark SQL data type that the UDF returns |
| children | Seq[Expression] | Input expressions that serve as arguments to the Python function |
| evalType | Int | Evaluation type identifier specifying how the UDF should be executed |
| udfDeterministic | Boolean | Flag indicating whether the UDF produces consistent results for the same inputs |
| resultId | ExprId | Unique expression identifier for the result (defaults to new generated ID) |

## Return Type
Returns the data type specified by the `dataType` parameter. Can be any Spark SQL data type including primitive types (IntegerType, StringType, etc.) or complex types (ArrayType, StructType, MapType).

## Supported Data Types
- **Input**: All Spark SQL data types are supported as inputs to Python UDFs
- **Output**: All Spark SQL data types that can be serialized between JVM and Python
- **Limitations**: Complex nested types may have serialization overhead

## Algorithm
- Serializes input expressions from JVM to Python-compatible format
- Transfers data to Python worker processes via inter-process communication
- Executes the Python lambda function on the deserialized data
- Serializes Python function results back to JVM Spark SQL data types
- Returns results as part of the Catalyst expression evaluation pipeline

## Partitioning Behavior
- **Preserves partitioning**: Yes, PythonUDF operations maintain existing data partitioning
- **Requires shuffle**: No, evaluation happens within existing partitions
- **Execution**: Requires spawning Python worker processes on each executor
- **Isolation**: Each partition's data is processed independently in separate Python processes

## Edge Cases
- **Null handling**: Null values are passed through to Python; null handling depends on the Python function implementation
- **Empty input**: Empty partitions skip Python process creation for efficiency
- **Python exceptions**: Runtime errors in Python functions propagate as Spark task failures
- **Memory pressure**: Large Python objects may cause memory issues due to JVM-Python serialization overhead
- **Deterministic flag**: Non-deterministic UDFs may produce different results across multiple evaluations

## Code Generation
PythonUDF extends `Unevaluable`, meaning it **does not support** Tungsten code generation. The expression requires interpreted execution through the dedicated Python evaluation framework, as it needs to interface with external Python processes rather than generate JVM bytecode.

## Examples
```python
# Example Python UDF registration and usage
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType

spark = SparkSession.builder.appName("PythonUDF").getOrCreate()

# Define and register UDF
def format_name(first, last):
    return f"{last}, {first}".upper()

format_udf = udf(format_name, StringType())

# Usage
df = spark.createDataFrame([("John", "Doe"), ("Jane", "Smith")], ["first", "last"])
result = df.select(format_udf(col("first"), col("last")).alias("formatted_name"))
```

```sql
-- SQL usage after registering UDF
CREATE OR REPLACE TEMPORARY VIEW people AS 
SELECT * FROM VALUES ("John", "Doe"), ("Jane", "Smith") AS t(first, last);

-- Register the UDF in SQL context first, then use
SELECT format_name_udf(first, last) as formatted_name FROM people;
```

## See Also
- `PythonFuncExpression` - Base trait for Python function expressions
- `ScalaUDF` - Scala equivalent for user-defined functions
- `Unevaluable` - Trait for expressions requiring special physical operators
- Physical operators: `ArrowEvalPythonExec`, `BatchEvalPythonExec`