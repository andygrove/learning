# BinaryPad

## Overview
BinaryPad is a runtime-replaceable expression that provides left padding (lpad) and right padding (rpad) functionality for binary data types. It serves as a wrapper that delegates the actual padding logic to native methods in the ByteArray class, supporting padding of binary strings with a specified pad value to reach a target length.

## Syntax
```sql
LPAD(binary_expr, length, pad_binary)
RPAD(binary_expr, length, pad_binary)
```

```scala
// DataFrame API usage would depend on the registered function name
col("binary_column").expr("lpad(binary_column, 10, pad_bytes)")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| str | BinaryType | The binary expression to be padded |
| len | IntegerType | Target length for the padded result |
| pad | BinaryType | Binary value used for padding |

## Return Type
BinaryType - Returns a binary array with the specified padding applied.

## Supported Data Types

- **Input**: BinaryType for string and pad arguments, IntegerType for length
- **Output**: BinaryType
- Implicit casting is supported for input types as this expression extends ImplicitCastInputTypes

## Algorithm

- Validates that funcName is either "lpad" or "rpad" through assertion
- Creates a StaticInvoke expression targeting the ByteArray class
- Delegates actual padding computation to native ByteArray.lpad() or ByteArray.rpad() methods
- Maintains input type constraints through the inputTypes override
- Uses runtime replacement pattern to substitute the expression during query planning

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require shuffle operations
- Can be applied per-partition independently
- Maintains data locality since it operates on individual rows

## Edge Cases

- **Null handling**: Returns null if any input argument is null (returnNullable = false in StaticInvoke, but null propagation handled by input validation)
- **Empty binary input**: Behavior depends on underlying ByteArray implementation
- **Zero or negative length**: Handled by the native ByteArray methods
- **Empty pad value**: May result in truncation or error depending on implementation
- **Length exceeding limits**: Subject to ByteArray implementation constraints

## Code Generation
This expression uses StaticInvoke for code generation, which enables Tungsten code generation by calling native methods directly rather than using interpreted evaluation mode.

## Examples
```sql
-- Left pad binary data to 8 bytes with zero bytes
SELECT LPAD(CAST('ABC' AS BINARY), 8, CAST('\x00' AS BINARY));

-- Right pad binary data to 10 bytes  
SELECT RPAD(binary_column, 10, CAST('XY' AS BINARY)) FROM table;
```

```scala
// DataFrame API usage (assuming registered functions)
import org.apache.spark.sql.functions._
df.select(expr("lpad(binary_col, 8, cast('\\x00' as binary))"))
df.select(expr("rpad(binary_col, 10, cast('pad' as binary))"))
```

## See Also

- StringLPad - String-based left padding equivalent
- StringRPad - String-based right padding equivalent  
- StaticInvoke - Runtime expression replacement mechanism
- RuntimeReplaceable - Base trait for expressions replaced at runtime