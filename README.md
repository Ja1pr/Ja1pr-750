# Ja1pr-750
full version released

Ja1pr750 is a high-performance, object-oriented symmetric stream cipher. It is designed to demonstrate modern cryptographic principles through a unique combination of dynamic state rotation and bitwise propagation.

[!CAUTION]
CRYPTOGRAPHIC DISCLAIMER: This cipher is an experimental project for educational purposes. It has not undergone formal cryptanalysis. Do not use it for securing sensitive, high-stakes, or production-level data.

 Technical Architecture
The cipher operates through a multi-layered security pipeline:

Entropy Injection (Salt): Every encryption starts with a cryptographically secure random salt generated via the secrets library.

Avalanche Propagation: A bitwise XOR forward-propagation layer ensures that changing a single bit in the plaintext affects every subsequent byte.

Dynamic S-Box Rotation: The internal alphabet state is not static. It performs complex rotations and character swaps based on key-driven indices for every processed character.

Base16 Binary Expansion: Final output is mapped through a custom 4-bit nibble expansion into a user-defined suppression alphabet.
