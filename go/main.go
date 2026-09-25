package main

import (
	"encoding/json"
	"fmt"
	"hash/fnv"
	"time"
)

type Block struct {
	Index        int
	Timestamp    string
	Data         string
	PreviousHash string
	Hash         string
}

func newBlock(index int, timestamp, data, previousHash string) Block {
	block := Block{
		Index:        index,
		Timestamp:    timestamp,
		Data:         data,
		PreviousHash: previousHash,
	}
	block.Hash = calculateHash(block)
	return block
}

func calculateHash(block Block) string {
	content, _ := json.Marshal([]any{
		block.Index,
		block.Timestamp,
		block.Data,
		block.PreviousHash,
	})

	hasher := fnv.New32a()
	_, _ = hasher.Write(content)
	return fmt.Sprintf("%08x", hasher.Sum32())
}

func (block Block) hasValidHash() bool {
	return block.Hash == calculateHash(block)
}

type Blockchain struct {
	blocks []Block
}

func newBlockchain() *Blockchain {
	genesis := newBlock(0, timestampNow(), "Genesis block", "0")
	return &Blockchain{blocks: []Block{genesis}}
}

func (blockchain *Blockchain) addBlock(data string) {
	previousBlock := blockchain.blocks[len(blockchain.blocks)-1]
	block := newBlock(
		previousBlock.Index+1,
		timestampNow(),
		data,
		previousBlock.Hash,
	)
	blockchain.blocks = append(blockchain.blocks, block)
}

func (blockchain *Blockchain) isValid() bool {
	for index, block := range blockchain.blocks {
		if !block.hasValidHash() {
			return false
		}
		if index > 0 && block.PreviousHash != blockchain.blocks[index-1].Hash {
			return false
		}
	}
	return true
}

func timestampNow() string {
	return time.Now().UTC().Format("2006-01-02T15:04:05.000Z")
}

func main() {
	blockchain := newBlockchain()
	blockchain.addBlock("Alice sends 2 coins to Bob")
	blockchain.addBlock("Bob sends 1 coin to Carol")

	for _, block := range blockchain.blocks {
		fmt.Printf(
			"Block %d: %s\n  Hash: %s\n  Previous: %s\n",
			block.Index,
			block.Data,
			block.Hash,
			block.PreviousHash,
		)
	}

	fmt.Printf("Blockchain valid: %t\n", blockchain.isValid())
}
