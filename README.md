# Simple Blockchain

An educational repository for learning how blockchain works and implementing its core concepts in different programming languages.

## Contents

| Language | Status | Example |
| --- | --- | --- |
| Dart | Basic blockchain example available | [dart/blockchain.dart](dart/blockchain.dart) |
| Python | Basic blockchain example available | [python/src/blockchain/main.py](python/src/blockchain/main.py) |
| Go | Basic blockchain example available | [go/main.go](go/main.go) |

## Run the Dart Example

Install the [Dart SDK](https://dart.dev/get-dart), then run this command from the repository root:

```sh
dart run dart/blockchain.dart
```

The example creates a chain of blocks, links each block to the previous one, and validates the chain's integrity.

## Run the Python Example

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run this command from the repository root:

```sh
cd python && uv run blockchain
```

The Python example follows the same structure and validation steps as the Dart and Go examples.

## Run the Go Example

Install [Go](https://go.dev/doc/install), then run this command from the repository root:

```sh
cd go && go run .
```

The Go example follows the same structure and validation steps as the Dart example.

## Learning Roadmap

- Block and chain structure
- Hashing and integrity validation
- Transactions and consensus mechanisms
- Networking between nodes

## Disclaimer

This project is for learning purposes only. The examples use a simplified FNV-1a hash function that is not suitable for real-world applications or data security.