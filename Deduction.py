from proof import *
from main import *
from expression import *
from proofs import *


class DeductionEngine:
    # ax1: A -> (B -> A)
    @staticmethod
    def ax1(a, b):
        return a.implies(b.implies(a))

    # ax2: (A -> (B -> C)) -> ((A -> B) -> (A -> C))
    @staticmethod
    def ax2(a, b, c):
        return (a.implies(b.implies(c))).implies((a.implies(b)).implies(a.implies(c)))

    # Применение теоремы о дедукции
    @staticmethod
    def deduce(original_proof, hypothesis_a):
        builder = ProofBuilder()

        # Старый номер строки -> Новый номер строки, где доказано (A -> Di)
        line_mapping = {}

        for step in original_proof.steps:
            current_formula = step.expression

            # Случай 1: Это сама гипотеза A
            if current_formula == hypothesis_a:
                s1 = builder.add(
                    DeductionEngine.ax1(hypothesis_a, hypothesis_a.implies(hypothesis_a)),
                    AxiomType("1"),
                )
                s2 = builder.add(
                    DeductionEngine.ax2(hypothesis_a, hypothesis_a.implies(hypothesis_a), hypothesis_a),
                    AxiomType("2"),
                )
                s3 = builder.add(
                    (hypothesis_a.implies(hypothesis_a.implies(hypothesis_a))).implies(
                        hypothesis_a.implies(hypothesis_a)
                    ),
                    MpType(s1, s2),
                )
                s4 = builder.add(DeductionEngine.ax1(hypothesis_a, hypothesis_a), AxiomType("1"))
                result_idx = builder.add(hypothesis_a.implies(hypothesis_a), MpType(s4, s3))
                line_mapping[step.index] = result_idx

            # Случай 2: Аксиома или другая гипотеза
            elif not isinstance(step.justification, MpType):
                s1 = builder.add(current_formula, step.justification)
                s2 = builder.add(DeductionEngine.ax1(current_formula, hypothesis_a), AxiomType("1"))
                result_idx = builder.add(hypothesis_a.implies(current_formula), MpType(s1, s2))
                line_mapping[step.index] = result_idx

            # Случай 3: Modus Ponens
            else:
                mp = step.justification
                line_j = mp.lineDef
                line_k = mp.lineImpl

                mapped_j = line_mapping[line_j]
                mapped_k = line_mapping[line_k]

                dj = original_proof.steps[line_j - 1].expression

                axiom2_expr = DeductionEngine.ax2(hypothesis_a, dj, current_formula)
                s1 = builder.add(axiom2_expr, AxiomType("2"))

                intermediate_expr = (hypothesis_a.implies(dj)).implies(hypothesis_a.implies(current_formula))
                s2 = builder.add(intermediate_expr, MpType(mapped_k, s1))

                result_idx = builder.add(hypothesis_a.implies(current_formula), MpType(mapped_j, s2))
                line_mapping[step.index] = result_idx

        return builder.build()