# BitwiseGet

## Overview
The `BitwiseGet` expression extracts a specific bit from an integral value at a given position. It performs a bitwise right shift operation followed by a bitwise AND to isolate the bit at the specified position, returning 1 if the bit is set or 0 if it is not.

## Syntax
```sql
bit_get(value, position)
```

```scala
// DataFrame API usage
df.select(bit_get(col("value"), col("position")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `value` | IntegralType (Byte, Short, Integer, Long) | The integral value from which to extract the bit |
| `position` | IntegerType | The zero-based bit position to extract (0 is the least significant bit) |

## Return Type
Returns `ByteType` - always returns either 0 or 1 as a byte value.

## Supported Data Types
- **Input value**: All integral types (ByteType, ShortType, IntegerType, LongType)
- **Input position**: IntegerType only
- **Output**: ByteType (0 or 1)

## Algorithm
- Validates that the position is within the valid range for the input data type's bit size
- Converts the target value to a long for consistent bit manipulation
- Performs a right shift operation (`>>`) by the specified position
- Applies a bitwise AND operation with 1 to isolate the least significant bit
- Converts the result to a byte (0 or 1)

## Partitioning Behavior
- **Preserves partitioning**: Yes, this is a row-level transformation that does not require data movement
- **Requires shuffle**: No, the operation is performed independently on each row
- **Deterministic**: Yes, produces consistent results for the same inputs

## Edge Cases
- **Null handling**: Returns null if either input argument is null (`nullIntolerant = true`)
- **Invalid position**: Throws an exception if position is outside the valid bit range for the data type
- **Negative position**: Invalid, will cause position validation to fail
- **Position bounds**: Must be within [0, bitSize) where bitSize varies by data type:
  - Byte: 0-7
  - Short: 0-15  
  - Integer: 0-31
  - Long: 0-63

## Code Generation
Supports Tungsten code generation through the `doGenCode` method. The generated code includes:
- Null-safe evaluation using `nullSafeCodeGen`
- Inline position validation via `BitwiseGetUtil.checkPosition`
- Direct bit manipulation without method calls for optimal performance

## Examples
```sql
-- Extract the 2nd bit (0-indexed) from the value 11 (binary: 1011)
SELECT bit_get(11, 2);
-- Result: 0 (the bit at position 2 is 0)

-- Extract the 0th bit from the value 11
SELECT bit_get(11, 0);
-- Result: 1 (the least significant bit is 1)

-- Extract the 3rd bit from the value 11
SELECT bit_get(11, 3);
-- Result: 1 (the most significant bit is 1)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Extract specific bits from a column
df.select(bit_get(col("flags"), lit(0)).as("lsb"))
  .select(bit_get(col("status_code"), col("bit_position")))

// Working with different integral types
df.select(bit_get(col("byte_col").cast("byte"), lit(7)))
  .select(bit_get(col("long_col").cast("long"), lit(63)))
```

## See Also
- **BitwiseAnd**: Bitwise AND operation between two values
- **BitwiseOr**: Bitwise OR operation between two values
- **BitwiseXor**: Bitwise XOR operation between two values
- **ShiftLeft**: Left bit shift operation
- **ShiftRight**: Right bit shift operation