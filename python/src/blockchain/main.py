
import json
from dataclasses import dataclass
from datetime import datetime, timezone


def _calculate_hash(
    index: int,
    timestamp: str,
    data: str,
    previous_hash: str,
) -> str:
    content = json.dumps(
        [index, timestamp, data, previous_hash],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    value = 0x811C9DC5

    for byte in content:
        value = ((value ^ byte) * 0x01000193) & 0xFFFFFFFF

    return f"{value:08x}"


def _timestamp_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


@dataclass(frozen=True)
class Block:
    index: int
    timestamp: str
    data: str
    previous_hash: str
    hash: str

    @classmethod
    def create(
        cls,
        index: int,
        timestamp: str,
        data: str,
        previous_hash: str,
    ) -> "Block":
        block_hash = _calculate_hash(index, timestamp, data, previous_hash)
        return cls(index, timestamp, data, previous_hash, block_hash)

    def has_valid_hash(self) -> bool:
        return self.hash == _calculate_hash(
            self.index,
            self.timestamp,
            self.data,
            self.previous_hash,
        )


class Blockchain:
    def __init__(self) -> None:
        self._blocks = [
            Block.create(0, _timestamp_now(), "Genesis block", "0")
        ]

    @property
    def blocks(self) -> tuple[Block, ...]:
        return tuple(self._blocks)

    def add_block(self, data: str) -> None:
        previous_block = self._blocks[-1]
        block = Block.create(
            previous_block.index + 1,
            _timestamp_now(),
            data,
            previous_block.hash,
        )
        self._blocks.append(block)

    def is_valid(self) -> bool:
        for index, block in enumerate(self._blocks):
            if not block.has_valid_hash():
                return False
            if index > 0 and block.previous_hash != self._blocks[index - 1].hash:
                return False
        return True


def main() -> None:
    blockchain = Blockchain()
    blockchain.add_block("Alice sends 2 coins to Bob")
    blockchain.add_block("Bob sends 1 coin to Carol")

    for block in blockchain.blocks:
        print(
            f"Block {block.index}: {block.data}\n"
            f"  Hash: {block.hash}\n"
            f"  Previous: {block.previous_hash}"
        )

    print(f"Blockchain valid: {str(blockchain.is_valid()).lower()}")


if __name__ == "__main__":
    main()