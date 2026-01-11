# -*- coding: utf-8 -*-

from expression import Variable, Implication, Negation, implies, expr_or, expr_and
from proof import Proof, ProofBuilder
from Deduction import DeductionEngine


def proveIdentity(x) -> Proof:
    builder = ProofBuilder()

    s1 = builder.axiom1(x, implies(x, x))
    s2 = builder.axiom2(x, implies(x, x), x)
    s3 = builder.mp(s1, s2)
    s4 = builder.axiom1(x, x)
    builder.mp(s4, s3)

    return builder.build()


def proveExplosion(notA, a, b) -> Proof:
    builder = ProofBuilder()

    hNotA = builder.hypothesis(notA)
    hA = builder.hypothesis(a)

    notB = Negation(b)

    s1 = builder.axiom1(notA, notB)
    s2 = builder.mp(hNotA, s1)

    s3 = builder.axiom1(a, notB)
    s4 = builder.mp(hA, s3)

    s5 = builder.axiom3(a, b)
    s6 = builder.mp(s2, s5)
    builder.mp(s4, s6)

    return builder.build()


def proveDNE(a) -> Proof:
    builder = ProofBuilder()

    notNotA = Negation(Negation(a))
    notA = Negation(a)

    h = builder.hypothesis(notNotA)
    a3 = builder.axiom3(notA, a)

    a1 = builder.axiom1(notNotA, notA)
    s1 = builder.mp(h, a1)

    idProof = proveIdentity(notA)
    s2 = builder.append(idProof)

    mp1 = builder.mp(s1, a3)
    builder.mp(s2, mp1)

    return DeductionEngine.deduce(builder.build(), notNotA)


def proveContraposition(a, b) -> Proof:
    builder = ProofBuilder()

    aImpliesB = implies(a, b)
    notB = Negation(b)

    h1 = builder.hypothesis(aImpliesB)
    h2 = builder.hypothesis(notB)

    notNotA = Negation(Negation(a))

    line1 = builder.axiom1(notB, notNotA)
    part1 = builder.mp(h2, line1)

    dneProof = proveDNE(a)
    dneLine = builder.append(dneProof)

    part2 = builder.apply_syl(dneLine, h1)

    ax3 = builder.axiom3(b, Negation(a))

    stepFinal1 = builder.mp(part1, ax3)
    builder.mp(part2, stepFinal1)

    d1 = DeductionEngine.deduce(builder.build(), notB)
    return DeductionEngine.deduce(d1, aImpliesB)


def proveA11(a) -> Proof:
    return proveIdentity(Negation(a))


def proveA8(a, b) -> Proof:
    builder = ProofBuilder()
    notA = Negation(a)

    builder.axiom1(b, notA)
    return builder.build()


def proveA10(a, b) -> Proof:
    notA = Negation(a)

    baseProof = proveExplosion(notA, a, b)
    d1 = DeductionEngine.deduce(baseProof, a)
    d2 = DeductionEngine.deduce(d1, notA)

    return d2


def proveA7(a, b) -> Proof:
    notA = Negation(a)

    baseProof = proveExplosion(notA, a, b)
    d1 = DeductionEngine.deduce(baseProof, notA)
    d2 = DeductionEngine.deduce(d1, a)

    return d2


def proveA4(a, b) -> Proof:
    builder = ProofBuilder()

    aAndB = expr_and(a, b)
    h = builder.hypothesis(aAndB)

    c = implies(a, Negation(b))

    proofA10 = proveA10(a, Negation(b))
    s1 = builder.append(proofA10)

    a1 = builder.axiom1(aAndB, Negation(a))
    s2 = builder.mp(h, a1)

    a3 = builder.axiom3(c, a)

    mp1 = builder.mp(s2, a3)
    builder.mp(s1, mp1)

    return DeductionEngine.deduce(builder.build(), aAndB)


def proveA5(a, b) -> Proof:
    builder = ProofBuilder()

    aAndB = expr_and(a, b)
    h = builder.hypothesis(aAndB)

    c = implies(a, Negation(b))

    a1 = builder.axiom1(aAndB, Negation(b))
    s1 = builder.mp(h, a1)

    s2 = builder.axiom1(Negation(b), a)

    a3 = builder.axiom3(c, b)

    mp1 = builder.mp(s1, a3)
    builder.mp(s2, mp1)

    return DeductionEngine.deduce(builder.build(), aAndB)


def proveA6(a, b) -> Proof:
    builder = ProofBuilder()

    notB = Negation(b)
    f = implies(a, notB)
    target = Negation(f)

    hA = builder.hypothesis(a)
    hB = builder.hypothesis(b)

    a3 = builder.axiom3(b, target)
    notNotF = Negation(Negation(f))

    a1 = builder.axiom1(b, notNotF)
    branch1 = builder.mp(hB, a1)

    dneProof = proveDNE(f)
    dne = builder.append(dneProof)

    a2 = builder.axiom2(notNotF, a, notB)
    mp2 = builder.mp(dne, a2)

    a1A = builder.axiom1(a, notNotF)
    notNotFImpliesA = builder.mp(hA, a1A)

    branch2 = builder.mp(notNotFImpliesA, mp2)

    s1 = builder.mp(branch2, a3)
    builder.mp(branch1, s1)

    d1 = DeductionEngine.deduce(builder.build(), b)
    return DeductionEngine.deduce(d1, a)


def proveA9(a, b, c) -> Proof:
    builder = ProofBuilder()

    aImpliesC = implies(a, c)
    bImpliesC = implies(b, c)
    aOrB = expr_or(a, b)

    h1 = builder.hypothesis(aImpliesC)
    h2 = builder.hypothesis(bImpliesC)
    h3 = builder.hypothesis(aOrB)

    notAImpliesC = builder.apply_syl(h3, h2)

    notA = Negation(a)

    contra1 = proveContraposition(a, c)
    contraLine1 = builder.append(contra1)
    notCImpliesNotA = builder.mp(h1, contraLine1)

    contra2 = proveContraposition(notA, c)
    contraLine2 = builder.append(contra2)
    notCImpliesNotNotA = builder.mp(notAImpliesC, contraLine2)

    dneProof = proveDNE(a)
    dneLine = builder.append(dneProof)

    notCImpliesA = builder.apply_syl(notCImpliesNotNotA, dneLine)

    lineA3 = builder.axiom3(a, c)

    mp1 = builder.mp(notCImpliesNotA, lineA3)
    builder.mp(notCImpliesA, mp1)

    d1 = DeductionEngine.deduce(builder.build(), aOrB)
    d2 = DeductionEngine.deduce(d1, bImpliesC)
    return DeductionEngine.deduce(d2, aImpliesC)