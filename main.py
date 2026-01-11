from pathlib import Path


def main() -> None:
    a = v("A")
    b = v("B")
    c = v("C")

    print("\n=== Доказательство A11: A ∨ ¬A ===")
    proofA11 = proveA11(a)
    proofA11.print()

    print("\n=== Доказательство A8: B -> (A ∨ B) ===")
    proofA8 = proveA8(a, b)
    proofA8.print()

    print("\n=== Доказательство A10: ¬A -> (A -> B) ===")
    proofA10 = proveA10(a, b)
    proofA10.print()

    print("\n=== Доказательство A7: A -> (¬A -> B) ===")
    proofA7 = proveA7(a, b)
    proofA7.print()

    print("\n=== Доказательство A4: ¬(A -> ¬B) -> A ===")
    proofA4 = proveA4(a, b)
    proofA4.print()

    print("\n=== Доказательство A5: ¬(A -> ¬B) -> B ===")
    proofA5 = proveA5(a, b)
    proofA5.print()

    print("\n=== Доказательство A6: A -> (B -> ¬(A -> ¬B)) ===")
    proofA6 = proveA6(a, b)
    proofA6.print()

    print("\n=== Доказательство A9: (A -> C) -> ((B -> C) -> ((¬A -> B) -> C)) ===")
    proofA9 = proveA9(a, b, c)

    out_path = Path("proof_a9.txt")
    with out_path.open("w", encoding="utf-8") as out:
        for step in proofA9.steps:
            out.write(f"{step}\n")

    print("Доказательство A9 сохранено в файл (24k+ строк)")


if __name__ == "__main__":
    main()