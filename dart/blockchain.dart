import 'dart:convert';

class Block {
  Block({
    required this.index,
    required this.timestamp,
    required this.data,
    required this.previousHash,
  }) : hash = _calculateHash(index, timestamp, data, previousHash);

  final int index;
  final String timestamp;
  final String data;
  final String previousHash;
  final String hash;

  static String _calculateHash(
    int index,
    String timestamp,
    String data,
    String previousHash,
  ) {
    final content = jsonEncode([index, timestamp, data, previousHash]);
    var value = 0x811c9dc5;

    for (final byte in utf8.encode(content)) {
      value = ((value ^ byte) * 0x01000193) & 0xffffffff;
    }

    return value.toRadixString(16).padLeft(8, '0');
  }

  bool hasValidHash() =>
      hash == _calculateHash(index, timestamp, data, previousHash);
}

class Blockchain {
  Blockchain()
      : _blocks = [
          Block(
            index: 0,
            timestamp: DateTime.now().toUtc().toIso8601String(),
            data: 'Genesis block',
            previousHash: '0',
          ),
        ];

  final List<Block> _blocks;

  List<Block> get blocks => List.unmodifiable(_blocks);

  void addBlock(String data) {
    final previousBlock = _blocks.last;
    _blocks.add(
      Block(
        index: previousBlock.index + 1,
        timestamp: DateTime.now().toUtc().toIso8601String(),
        data: data,
        previousHash: previousBlock.hash,
      ),
    );
  }

  bool isValid() {
    for (var index = 0; index < _blocks.length; index++) {
      final block = _blocks[index];
      if (!block.hasValidHash()) return false;
      if (index > 0 && block.previousHash != _blocks[index - 1].hash) {
        return false;
      }
    }
    return true;
  }
}

void main() {
  final blockchain = Blockchain()
    ..addBlock('Alice sends 2 coins to Bob')
    ..addBlock('Bob sends 1 coin to Carol');

  for (final block in blockchain.blocks) {
    print(
      'Block ${block.index}: ${block.data}\n'
      '  Hash: ${block.hash}\n'
      '  Previous: ${block.previousHash}',
    );
  }

  print('Blockchain valid: ${blockchain.isValid()}');
}