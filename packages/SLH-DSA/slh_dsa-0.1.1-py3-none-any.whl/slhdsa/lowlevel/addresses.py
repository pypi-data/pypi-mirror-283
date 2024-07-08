from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T", bound="Address")


@dataclass
class Address:
    layer: int
    tree: int
    typ: int

    def to_bytes(self) -> bytes:
        return self.layer.to_bytes(4, "big") + self.tree.to_bytes(12, "big") + self.typ.to_bytes(4, "big")

    def with_type(self, typ: type[T]) -> T:
        return typ(self.layer, self.tree, typ.typ)


@dataclass
class WOTSHashAddress(Address):
    typ: int = 0
    keypair: int = 0
    chain: int = 0
    hash: int = 0

    def to_bytes(self) -> bytes:
        return super().to_bytes() + self.keypair.to_bytes(4, "big") + self.chain.to_bytes(4, "big") + self.hash.to_bytes(4, "big")


@dataclass
class WOTSPKAddress(Address):
    typ: int = 1
    keypair: int = 0

    def to_bytes(self) -> bytes:
        return super().to_bytes() + self.keypair.to_bytes(4, "big") + b'\x00' * 8


@dataclass
class TreeAddress(Address):
    typ: int = 2
    height: int = 0
    index: int = 0

    def to_bytes(self) -> bytes:
        return super().to_bytes() + b'\x00' * 4 + self.height.to_bytes(4, "big") + self.index.to_bytes(4, "big")


@dataclass
class FORSTreeAddress(Address):
    typ: int = 3
    keypair: int = 0
    height: int = 0
    index: int = 0

    def to_bytes(self) -> bytes:
        return super().to_bytes() + self.keypair.to_bytes(4, "big") + self.height.to_bytes(4, "big") + self.index.to_bytes(4, "big")


@dataclass
class FORSRootsAddress(Address):
    typ: int = 4
    keypair: int = 0

    def to_bytes(self) -> bytes:
        return super().to_bytes() + self.keypair.to_bytes(4, "big") + b'\x00' * 8


@dataclass
class WOTSPrfAddress(Address):
    typ: int = 5
    keypair: int = 0
    chain: int = 0
    hash: int = 0

    def to_bytes(self) -> bytes:
        return super().to_bytes() + self.keypair.to_bytes(4, "big") + self.chain.to_bytes(4, "big") + self.hash.to_bytes(4, "big")


@dataclass
class FORSPrfAddress(Address):
    typ: int = 6
    keypair: int = 0
    height: int = 0
    index: int = 0

    def to_bytes(self) -> bytes:
        return super().to_bytes() + self.keypair.to_bytes(4, "big") + self.height.to_bytes(4, "big") + self.index.to_bytes(4, "big")
