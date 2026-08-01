#!/usr/bin/env python3
"""Reject unstable glyph animation and concurrent cross-fades in lesson scenes."""

from __future__ import annotations

import ast
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

TEXT_CONSTRUCTORS = {
    "Code",
    "DecimalNumber",
    "Integer",
    "MarkupText",
    "MathTable",
    "MathTex",
    "Matrix",
    "Paragraph",
    "Table",
    "Tex",
    "Text",
    "Variable",
    "label",
}
TEXT_MORPHS = {
    "ReplacementTransform",
    "TransformFromCopy",
    "TransformMatchingShapes",
    "TransformMatchingTex",
}


def _call_name(node: ast.AST) -> str | None:
    if not isinstance(node, ast.Call):
        return None
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def _is_self_play(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "play"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "self"
    )


def _fade_targets(node: ast.AST, animation_name: str) -> set[str]:
    """Return named targets for one concurrent fade animation type."""
    if isinstance(node, ast.Call) and _call_name(node) == "Succession":
        return set()

    targets: set[str] = set()
    if isinstance(node, ast.Call):
        name = _call_name(node)
        if name == animation_name and node.args:
            for child in ast.walk(node.args[0]):
                if isinstance(child, ast.Name):
                    targets.add(child.id)
            return targets
        for argument in node.args:
            targets.update(_fade_targets(argument, animation_name))
        for keyword in node.keywords:
            targets.update(_fade_targets(keyword.value, animation_name))
        return targets

    for child in ast.iter_child_nodes(node):
        targets.update(_fade_targets(child, animation_name))
    return targets


class _Positions:
    """Small union-find for objects explicitly moved to the same anchor."""

    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, item: str) -> str:
        self.parent.setdefault(item, item)
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, left: str, right: str) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


def _move_to_anchor(call: ast.Call) -> ast.AST | None:
    if (
        isinstance(call.func, ast.Attribute)
        and call.func.attr == "move_to"
        and call.args
    ):
        return call.args[0]
    return None


def _record_position(positions: _Positions, name: str, anchor: ast.AST) -> None:
    if isinstance(anchor, ast.Name):
        positions.union(name, anchor.id)
        return
    positions.union(name, "@" + ast.dump(anchor, include_attributes=False))


def _explicit_positions(tree: ast.AST) -> _Positions:
    positions = _Positions()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            anchor = _move_to_anchor(node.value)
            if anchor is not None:
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        _record_position(positions, target.id, anchor)
        if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
            continue
        anchor = _move_to_anchor(node.value)
        owner = node.value.func.value if isinstance(node.value.func, ast.Attribute) else None
        if anchor is not None and isinstance(owner, ast.Name):
            _record_position(positions, owner.id, anchor)
    return positions


class _TextOrigins:
    """Conservatively identify expressions that contain rendered glyphs."""

    def __init__(self, tree: ast.AST) -> None:
        self.assignments: dict[str, list[ast.AST]] = {}
        self.returns: dict[str, list[ast.AST]] = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    self._record_target(target, node.value)
            elif isinstance(node, ast.AnnAssign) and node.value is not None:
                self._record_target(node.target, node.value)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.returns[node.name] = [
                    child.value
                    for child in ast.walk(node)
                    if isinstance(child, ast.Return) and child.value is not None
                ]

    def _record_target(self, target: ast.AST, value: ast.AST) -> None:
        if isinstance(target, ast.Name):
            self.assignments.setdefault(target.id, []).append(value)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for element in target.elts:
                self._record_target(element, value)

    def has_text(
        self,
        node: ast.AST,
        *,
        seen_names: frozenset[str] = frozenset(),
        seen_methods: frozenset[str] = frozenset(),
    ) -> bool:
        if isinstance(node, ast.Name):
            if node.id in seen_names:
                return False
            return any(
                self.has_text(
                    value,
                    seen_names=seen_names | {node.id},
                    seen_methods=seen_methods,
                )
                for value in self.assignments.get(node.id, [])
            )
        if isinstance(node, ast.Subscript):
            return self._subscript_has_text(
                node,
                seen_names=seen_names,
                seen_methods=seen_methods,
            )
        if isinstance(node, ast.Starred):
            return self.has_text(
                node.value,
                seen_names=seen_names,
                seen_methods=seen_methods,
            )
        if isinstance(node, ast.Call):
            name = _call_name(node)
            if name in TEXT_CONSTRUCTORS:
                return True
            if name in self.returns and name not in seen_methods:
                if any(
                    self.has_text(
                        value,
                        seen_names=seen_names,
                        seen_methods=seen_methods | {name},
                    )
                    for value in self.returns[name]
                ):
                    return True
            # Fluent calls such as MathTex(...).scale(...) retain the receiver's type.
            if isinstance(node.func, ast.Attribute) and self.has_text(
                node.func.value,
                seen_names=seen_names,
                seen_methods=seen_methods,
            ):
                return True
            if name in {"Group", "VGroup", "VDict", "always_redraw"}:
                return any(
                    self.has_text(
                        child,
                        seen_names=seen_names,
                        seen_methods=seen_methods,
                    )
                    for child in [*node.args, *(item.value for item in node.keywords)]
                )
            return False
        if isinstance(node, ast.Lambda):
            return self.has_text(
                node.body,
                seen_names=seen_names,
                seen_methods=seen_methods,
            )
        if isinstance(node, ast.Dict):
            children = [*node.keys, *node.values]
        elif isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            children = list(node.elts)
        elif isinstance(node, ast.IfExp):
            children = [node.body, node.orelse]
        else:
            return False
        return any(
            child is not None
            and self.has_text(
                child,
                seen_names=seen_names,
                seen_methods=seen_methods,
            )
            for child in children
        )

    def _subscript_has_text(
        self,
        node: ast.Subscript,
        *,
        seen_names: frozenset[str],
        seen_methods: frozenset[str],
    ) -> bool:
        """Resolve obvious indexed text without tainting every mixed helper group."""
        values = self._indexed_values(node.value, node.slice, seen_names=seen_names)
        if values is not None:
            return any(
                self.has_text(
                    value,
                    seen_names=seen_names,
                    seen_methods=seen_methods,
                )
                for value in values
            )
        return self._is_text_object(
            node.value,
            seen_names=seen_names,
            seen_methods=seen_methods,
        )

    def _indexed_values(
        self,
        value: ast.AST,
        index: ast.AST,
        *,
        seen_names: frozenset[str],
    ) -> list[ast.AST] | None:
        if isinstance(value, ast.Name):
            if value.id in seen_names:
                return None
            candidates: list[ast.AST] = []
            resolved = False
            for assignment in self.assignments.get(value.id, []):
                nested = self._indexed_values(
                    assignment,
                    index,
                    seen_names=seen_names | {value.id},
                )
                if nested is not None:
                    candidates.extend(nested)
                    resolved = True
            return candidates if resolved else None
        if isinstance(value, ast.Call) and _call_name(value) in {"Group", "VGroup"}:
            if isinstance(index, ast.Constant) and isinstance(index.value, int):
                try:
                    return [value.args[index.value]]
                except IndexError:
                    return []
            return list(value.args)
        if isinstance(value, (ast.List, ast.Tuple)):
            if isinstance(index, ast.Constant) and isinstance(index.value, int):
                try:
                    return [value.elts[index.value]]
                except IndexError:
                    return []
            return list(value.elts)
        if isinstance(value, ast.Dict) and isinstance(index, ast.Constant):
            return [
                item
                for key, item in zip(value.keys, value.values, strict=True)
                if isinstance(key, ast.Constant) and key.value == index.value
            ]
        return None

    def _is_text_object(
        self,
        node: ast.AST,
        *,
        seen_names: frozenset[str],
        seen_methods: frozenset[str],
    ) -> bool:
        if isinstance(node, ast.Name):
            if node.id in seen_names:
                return False
            return any(
                self._is_text_object(
                    value,
                    seen_names=seen_names | {node.id},
                    seen_methods=seen_methods,
                )
                for value in self.assignments.get(node.id, [])
            )
        if isinstance(node, ast.Call):
            name = _call_name(node)
            if name in TEXT_CONSTRUCTORS:
                return True
            if isinstance(node.func, ast.Attribute):
                return self._is_text_object(
                    node.func.value,
                    seen_names=seen_names,
                    seen_methods=seen_methods,
                )
        return False

    def text_signatures(
        self,
        node: ast.AST,
        *,
        seen_names: frozenset[str] = frozenset(),
    ) -> set[str]:
        """Return comparable text origins for plain Transform() calls."""
        if isinstance(node, ast.Name):
            if node.id in seen_names:
                return set()
            signatures: set[str] = set()
            for value in self.assignments.get(node.id, []):
                signatures.update(
                    self.text_signatures(value, seen_names=seen_names | {node.id})
                )
            return signatures
        if isinstance(node, ast.Subscript):
            base = self.text_signatures(node.value, seen_names=seen_names)
            if not base:
                return set()
            return {
                f"{signature}[{ast.dump(node.slice, include_attributes=False)}]"
                for signature in base
            }
        if not isinstance(node, ast.Call):
            return set()
        name = _call_name(node)
        if name in TEXT_CONSTRUCTORS:
            content = ",".join(
                ast.dump(argument, include_attributes=False) for argument in node.args
            )
            return {f"{name}({content})"}
        if isinstance(node.func, ast.Attribute):
            receiver = self.text_signatures(node.func.value, seen_names=seen_names)
            if receiver:
                return receiver
        if name in self.returns and any(self.has_text(value) for value in self.returns[name]):
            return {f"helper:{name}"}
        return set()


def transition_issues(source: str) -> list[tuple[int, str]]:
    """Return line-numbered transition problems found in one scene source."""
    tree = ast.parse(source)
    issues: list[tuple[int, str]] = []
    positions = _explicit_positions(tree)
    text_origins = _TextOrigins(tree)

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        animation_name = _call_name(node)
        if animation_name == "Write":
            issues.append(
                (
                    node.lineno,
                    "Write() draws glyph strokes; reveal completed text with FadeIn()",
                )
            )
        if animation_name in {"TransformMatchingShapes", "TransformMatchingTex"}:
            issues.append(
                (
                    node.lineno,
                    f"{animation_name}() reshapes glyphs; replace text in a settled "
                    "sequence",
                )
            )
        elif animation_name in TEXT_MORPHS and any(
            text_origins.has_text(argument) for argument in node.args[:2]
        ):
            issues.append(
                (
                    node.lineno,
                    f"{animation_name}() morphs a text-bearing object; move the same "
                    "object or use settled FadeOut()/FadeIn() phases",
                )
            )
        elif animation_name == "Transform" and len(node.args) >= 2:
            source_signatures = text_origins.text_signatures(node.args[0])
            target_signatures = text_origins.text_signatures(node.args[1])
            if source_signatures and target_signatures and not (
                source_signatures & target_signatures
            ):
                issues.append(
                    (
                        node.lineno,
                        "Transform() changes glyph content; replace text in a settled "
                        "sequence",
                    )
                )
        if not _is_self_play(node):
            continue
        outgoing: set[str] = set()
        incoming: set[str] = set()
        for argument in node.args:
            outgoing.update(_fade_targets(argument, "FadeOut"))
            incoming.update(_fade_targets(argument, "FadeIn"))
        outgoing_roots = {positions.find(name) for name in outgoing}
        incoming_roots = {positions.find(name) for name in incoming}
        if outgoing_roots & incoming_roots:
            issues.append(
                (
                    node.lineno,
                    "objects at the same anchor fade out and in concurrently; sequence "
                    "the clearance with Succession()",
                )
            )

    return sorted(set(issues))


def main() -> int:
    failures = 0
    checked = 0
    for metadata_path in sorted(ROOT.glob("lessons/*/*/lesson.toml")):
        with metadata_path.open("rb") as handle:
            lesson = tomllib.load(handle)
        scene_path = ROOT / lesson.get("scene_file", "")
        if not scene_path.is_file():
            continue
        checked += 1
        try:
            issues = transition_issues(scene_path.read_text(encoding="utf-8"))
        except SyntaxError as error:
            issues = [(error.lineno or 1, f"scene syntax error: {error.msg}")]
        for line_number, message in issues:
            failures += 1
            print(
                f"ERROR: {lesson['id']}: {scene_path}:{line_number}: {message}",
                file=sys.stderr,
            )

    if failures:
        print(f"Slide transition checks failed: {failures} issue(s) across {checked} scenes.")
        return 1
    print(f"Slide transition checks passed: {checked} scenes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
