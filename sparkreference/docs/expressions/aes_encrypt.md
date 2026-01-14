# AesEncrypt

## Overview

The `AesEncrypt` expression provides AES (Advanced Encryption Standard) encryption functionality in Spark SQL. It encrypts binary input data using a specified key, encryption mode, padding scheme, initialization vector (IV), and optional additional authenticated data (AAD). This expression is implemented as a runtime replaceable that delegates to native implementation methods for performance.

## Syntax

```sql
aes_encrypt(input, key [, mode [, padding [, iv [, aad]]]])
```

```scala
// DataFrame API
import org.apache.spark.sql.catalyst.expressions.AesEncrypt
AesEncrypt(inputExpr, keyExpr, modeExpr, paddingExpr, ivExpr, aadExpr)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| input | BinaryType | The binary data to encrypt |
| key | BinaryType | The encryption key as binary data |
| mode | StringType | The encryption mode (defaults to "GCM") |
| padding | StringType | The padding scheme (defaults to "DEFAULT") |
| iv | BinaryType | The initialization vector (defaults to empty) |
| aad | BinaryType | Additional authenticated data for GCM mode (defaults to empty) |

## Return Type

Returns `BinaryType` - the encrypted data as a binary array.

## Supported Data Types

- **Input data**: Binary type only
- **Key**: Binary type only  
- **Mode**: String type with collation support (trim collation supported)
- **Padding**: String type with collation support (trim collation supported)
- **IV**: Binary type only
- **AAD**: Binary type only

## Algorithm

- Accepts up to 6 parameters with automatic default value assignment for optional parameters
- Delegates actual encryption to `ExpressionImplUtils.aesEncrypt` static method via `StaticInvoke`
- Supports multiple constructor overloads for convenience (2-6 parameters)
- Uses implicit type casting to coerce inputs to expected types
- Implements runtime replacement pattern for efficient native code execution

## Partitioning Behavior

This expression preserves partitioning behavior:

- Does not require data shuffling across partitions
- Can be applied per-row independently within each partition  
- Does not affect the partitioning scheme of the underlying dataset

## Edge Cases

- **Null inputs**: Follows standard Spark null propagation - any null input produces null output
- **Empty AAD**: When AAD parameter is omitted, defaults to empty binary literal
- **Empty IV**: When IV parameter is omitted, defaults to empty binary literal  
- **Invalid key sizes**: Behavior depends on underlying AES implementation in ExpressionImplUtils
- **Mode/padding combinations**: Some mode and padding combinations may not be supported

## Code Generation

This expression uses runtime replacement with `StaticInvoke`, which supports:

- Full code generation (Tungsten) when possible
- Falls back to interpreted mode for complex scenarios
- Leverages native implementation through `ExpressionImplUtils` for optimal performance

## Examples

```sql
-- Basic encryption with default GCM mode
SELECT base64(aes_encrypt('Spark', 'abcdefghijklmnop12345678ABCDEFGH'));

-- Full specification with all parameters
SELECT base64(aes_encrypt(
  'Spark', 
  'abcdefghijklmnop12345678ABCDEFGH', 
  'GCM', 
  'DEFAULT', 
  unhex('000000000000000000000000'), 
  'This is an AAD mixed into the input'
));
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(base64(expr("aes_encrypt(data, key, 'GCM', 'DEFAULT', iv, aad)")))

// Using expression directly
import org.apache.spark.sql.catalyst.expressions._
val encrypted = AesEncrypt(col("data").expr, col("key").expr)
```

## See Also

- `AesDecrypt` - corresponding decryption function
- `base64/unbase64` - commonly used for encoding encrypted binary output
- `unhex/hex` - for converting hexadecimal strings to binary data