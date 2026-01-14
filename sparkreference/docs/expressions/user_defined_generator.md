# UserDefinedGenerator

## Overview
A generator expression that produces multiple output rows using a user-provided lambda function. It converts Catalyst internal rows to Scala rows, applies the user function, and returns an iterable collection of internal rows for further processing.

## Syntax
```scala
// DataFrame API usage - typically used internally
UserDefinedGenerator(elementSchema, function, children)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| elementSchema | StructType | Schema definition for the output rows produced by the generator |
| function | Row => IterableOnce[InternalRow] | User-defined lambda function that takes a Row and returns an iterable collection of InternalRows |
| children | Seq[Expression] | Child expressions that provide input data to the generator function |

## Return Type
Returns `IterableOnce[InternalRow]` - a collection of internal rows that can be iterated over to produce multiple output rows from a single input row.

## Supported Data Types

- All Catalyst data types supported through child expressions
- Input types determined by the data types of child expressions  
- Output types must conform to the provided elementSchema
- Supports User Defined Types (UDT) through schema-based conversion

## Algorithm

- Lazily initializes converters on first evaluation call
- Creates an InterpretedProjection from child expressions to extract input values
- Builds a Catalyst-to-Scala converter based on child expression schemas and data types
- Projects input row through child expressions to get intermediate values
- Converts intermediate internal row to Scala Row using type converters
- Applies user-defined function to the converted Scala row
- Returns the iterable collection of InternalRows produced by the function

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve partitioning as it's a generator that can produce variable numbers of output rows
- May require shuffle depending on downstream operations that depend on generated data distribution
- Generator nature means output cardinality is unpredictable and depends on user function behavior

## Edge Cases

- Null handling depends on the user-defined function implementation - no built-in null safety
- Empty input behavior: if child expressions produce null/empty values, behavior depends on user function
- Lazy initialization means first evaluation may have higher latency due to converter setup
- Schema mismatch between elementSchema and actual function output can cause runtime failures
- Function exceptions are propagated up without additional error handling

## Code Generation
This expression uses `CodegenFallback` trait, meaning it does not support Tungsten code generation and always falls back to interpreted evaluation mode for safety and flexibility with user-defined functions.

## Examples
```scala
// Example DataFrame API usage - internal usage
import org.apache.spark.sql.types._
import org.apache.spark.sql.catalyst.InternalRow

val schema = StructType(Seq(
  StructField("value", IntegerType, false)
))

val generator = UserDefinedGenerator(
  elementSchema = schema,
  function = (row: Row) => {
    val input = row.getInt(0)
    (1 to input).map(i => InternalRow(i))
  },
  children = Seq(col("number"))
)
```

```sql
-- UserDefinedGenerator is typically not directly accessible in SQL
-- It's used internally by higher-level constructs like table-valued functions
```

## See Also

- Generator - Base trait for all generator expressions
- ExplodeBase - Built-in generator for array/map explosion  
- CodegenFallback - Trait for expressions that disable code generation
- InterpretedProjection - Row projection mechanism used internally