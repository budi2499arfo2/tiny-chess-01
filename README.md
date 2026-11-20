# tiny-chess-01

Chess engine for make.fun competition tiny-chess-01.

## Technical approach

4 KB Python chess engine using:
- 0x88 board representation
- Alpha-beta search with depth 3
- Material evaluation
- Direct attack detection (no make/unmake for king moves)

Compressed with lzma + base64 to fit within 4096 bytes.
