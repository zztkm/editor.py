# editor.py

## Motivation

Inspired by this article, I decided to implement a text editor: [Challenging projects every programmer should try - Austin Z. Henley](https://austinhenley.com/blog/challengingprojects.html)

## Piece Table Overview

> In computing, a piece table is a data structure typically used to represent a text document while it is edited in a text editor. Initially a reference (or 'span') to the whole of the original file is created, which represents the as yet unchanged file. Subsequent inserts and deletes replace a span by combinations of one, two, or three references to sections of either the original document or to a buffer holding inserted text.[1]
> Typically the text of the original document is held in one immutable block, and the text of each subsequent insert is stored in new immutable blocks. Because even deleted text is still included in the piece table, this makes multi-level or unlimited undo easier to implement with a piece table than with alternative data structures such as a gap buffer.
> This data structure was invented by J Strother Moore.[2]


> コンピュータでは、ピーステーブルは、通常、テキストエディターで編集中のテキスト文書を表現するために使用されるデータ構造です。最初は、元のファイル全体への参照（または「スパン」）が作成され、まだ変更されていないファイルを表します。その後、挿入や削除を行うと、スパンは、元の文書または挿入されたテキストを保持するバッファのいずれかのセクションへの1、2、または3つの参照の組み合わせに置き換えられます[1]。
> 通常、元の文書のテキストは 1 つの不変ブロックに保持され、それ以降の挿入のテキストはそれぞれ新しい不変ブロックに格納されます。削除されたテキストもピーステーブルに含まれるため、ギャップバッファなどの代替データ構造よりもピーステーブルの方が、複数レベルまたは無制限のアンドゥを簡単に実装することができます。
> このデータ構造はJ Strother Mooreによって考案された[2]。: 日本語訳 DeepL

from wiki

## Development

init
```shell
poetry install
```

run tests
```shell
poetry run tox
```

install dev version editor:
```shell
poetry install
```

run dev version editor (e.g. print version):
```shell
poetry run editor-py --version
```

## Further reading:

- [Text Editor: Data Structures – averylaird.com](https://www.averylaird.com/programming/the%20text%20editor/2017/09/30/the-piece-table/)
- [二分木 - Wikipedia](https://ja.wikipedia.org/wiki/%E4%BA%8C%E5%88%86%E6%9C%A8)
- Gap Buffer
    - https://en.wikipedia.org/wiki/Gap_buffer
    - [dixtel/gapbuffer: Text editor with gap buffer implementation](https://github.com/dixtel/gapbuffer)
- Piece table
    - https://en.wikipedia.org/wiki/Piece_table
    - [テキストエディタで使われがちなデータ構造 Piece Table の概要と実装 - A Memorandum](https://blog1.mammb.com/entry/2022/09/07/224202#Piece-Table-method)
    - https://github.com/saiguy3/piece_table
	- https://github.com/veler/Csharp-Piece-Table-Implementation/blob/master/CsharpPieceTableImplementation/TextPieceTable.cs
