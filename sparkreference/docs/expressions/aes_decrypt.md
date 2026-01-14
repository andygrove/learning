# AesDecrypt

## Overview
The `AesDecrypt` expression provides AES (Advanced Encryption Standard) decryption functionality for encrypted binary data. It supports multiple AES modes including GCM (Galois/Counter Mode) with optional Additional Authenticated Data (AAD) for authenticated encryption scenarios.

## Syntax
```sql
AES_DECRYPT(input, key [, mode [, padding [, aad]]])
```

```scala
// DataFrame API
col("encrypted_data").aes_decrypt(col("key"), col("mode"), col("padding"), col("aad"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| input | Binary | The encrypted binary data to decrypt |
| key | Binary | The encryption key used for decryption |
| mode | String | The AES mode (default: "GCM") |
| padding | String | The padding scheme (default: "DEFAULT") |
| aad | Binary | Additional Authenticated Data for authenticated modes (default: empty) |

## Return Type
Returns `BinaryType` - the decrypted data as a binary array.

## Supported Data Types

- **input**: Binary data only
- **key**: Binary data only  
- **mode**: String with collation support (supports trim collation)
- **padding**: String with collation support (supports trim collation)
- **aad**: Binary data only

## Algorithm

- Validates input parameters and converts them to appropriate formats
- Extracts the AES encryption mode from the mode parameter (defaults to GCM)
- Configures the padding scheme based on the padding parameter
- Initializes the AES cipher with the provided key and parameters
- For authenticated modes like GCM, incorporates the Additional Authenticated Data
- Performs the decryption operation and returns the plaintext binary data

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffling as it operates row-by-row
- Can be executed independently on each partition
- Maintains the same partitioning scheme as the input data

## Edge Cases

- **Null input**: Returns null if any required parameter (input, key) is null
- **Invalid key length**: Throws exception for keys that don't match AES requirements (128, 192, or 256 bits)
- **Corrupted ciphertext**: Returns null or throws exception for malformed encrypted data
- **Authentication failure**: For authenticated modes, returns null if AAD doesn't match or authentication tag is invalid
- **Empty AAD**: Treated as valid input (empty byte array) for modes that support AAD
- **Unsupported mode/padding**: Throws exception for invalid combinations

## Code Generation
This expression uses `RuntimeReplaceable` with `StaticInvoke`, which means:

- Falls back to interpreted mode rather than generating optimized code
- Delegates execution to `ExpressionImplUtils.aesDecrypt` method
- Does not benefit from Tungsten code generation optimizations

## Examples
```sql
-- Basic AES decryption with default GCM mode
SELECT AES_DECRYPT(unbase64('AAAAAAAAAAAAAAAAQiYi+sTLm7KD9UcZ2nlRdYDe/PX4'), 
                   'abcdefghijklmnop12345678ABCDEFGH');

-- AES decryption with specific mode, padding and AAD
SELECT AES_DECRYPT(unbase64('AAAAAAAAAAAAAAAAQiYi+sTLm7KD9UcZ2nlRdYDe/PX4'), 
                   'abcdefghijklmnop12345678ABCDEFGH', 
                   'GCM', 
                   'DEFAULT', 
                   'This is an AAD mixed into the input');
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(
  aes_decrypt(
    col("encrypted_data"),
    col("encryption_key"),
    lit("GCM"),
    lit("DEFAULT"),
    col("additional_auth_data")
  ).alias("decrypted_data")
)
```

## See Also

- `AesEncrypt` - Corresponding AES encryption function
- `Base64` / `UnBase64` - For encoding/decoding binary data to/from strings
- `Sha2` - For generating cryptographic hashes