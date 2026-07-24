# Pedagogy Research Notes

These notes explain the original teaching grammar encoded in `AGENTS.md`.
They are a design record, not source material for copying narration, artwork,
code, or rendered media.

## Carlo's Math context

[正哥愛數學](https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/) is built
for students preparing for selective science and gifted-class assessments and
for teachers studying problem solving. Its archive-plus-topic structure makes
two needs visible:

- each lesson must retain its original exam context and exact solution source;
- the same problem may also belong to one or more reusable mathematical topics.

The production model therefore stores one provider asset once, preserves all
archive/topic relationships, and makes one deliberate lesson per identifiable
problem-solution unit. A topic page organizes discovery; it does not justify
duplicating a finished deck.

## 3Blue1Brown explanatory patterns

The following official pages were reviewed as examples of explanatory order:

- [About](https://www.3blue1brown.com/about/) describes a focus on discovery,
  visualization, and the circumstances that make an idea feel natural.
- [Essence of calculus](https://www.3blue1brown.com/lessons/essence-of-calculus/)
  motivates a general method through concrete changing quantities.
- [The hardest problem on the hardest test](https://www.3blue1brown.com/lessons/hardest-problem/)
  varies a point while fixed structure stays visible, then turns an observed
  regularity into an argument.
- [Sphere area](https://www.3blue1brown.com/lessons/sphere-area/) moves between
  a whole object, one representative piece, and the reconstructed whole.
- [Derivatives of trig functions](https://www.3blue1brown.com/lessons/derivatives-trig-functions/)
  uses motion diagnostically, then freezes the picture for a local proof.
- [Dandelin spheres](https://www.3blue1brown.com/lessons/dandelin-spheres/)
  makes a hidden invariant visible before using it algebraically.
- [Windmills](https://www.3blue1brown.com/lessons/windmills/) treats deliberate
  exploration and invariant-finding as part of the proof experience.

Across those examples, the transferable pattern is not a visual brand. It is
an order of attention:

1. pose a concrete question;
2. vary one meaningful object and freeze the rest;
3. compare deliberately chosen examples, including a boundary case;
4. pause before naming the pattern;
5. reveal the invariant or constraint that explains it;
6. isolate one representative piece;
7. introduce algebra only after the visible relationship earns it; and
8. return the local result to the original whole.

This repository implements that grammar with original diagrams, wording, code,
timing, colors, and lesson-specific arguments. It does not imitate 3Blue1Brown
scene composition or incorporate its expressive assets.

## Consequences for review

A polished animation still fails review when it reveals the completed locus,
formula, or theorem before the viewer has a question that needs it. Motion is
evidence only when the chosen states distinguish hypotheses, boundaries, or
invariants. A visual coincidence is not a proof: symmetry needs a
constraint-preserving map, counting needs an exhaustive boundary argument,
and an area decomposition needs visible ownership of every added or subtracted
term.
