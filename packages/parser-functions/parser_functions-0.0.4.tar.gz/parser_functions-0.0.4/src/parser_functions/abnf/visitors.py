from dataclasses import dataclass, field
from typing import Dict, List

from parser_functions.abnf.ast import (
    AlternationNode,
    ConcatenationNode,
    DeferNode,
    GroupNode,
    OptionNode,
    RepititionNode,
    RuleListNode,
    RuleNameNode,
    RuleNode,
)


@dataclass
class DeferVisitor:
    """Visitor that climbs the AST injecting DeferNode to prevent reference loops."""

    path: List[str] = field(default_factory=list)
    rules: Dict[str, RuleNode] = field(default_factory=dict)

    def _append(self, name):
        self.path.append(name)

    def _pop(self):
        self.path.pop()

    def visit_rule_list_node(self, node: RuleListNode):
        for rule in node.rules:
            self.rules[rule.name_node.name] = rule
        for rule in node.rules:
            self.path = []
            rule.accept(self)

    def visit_rule_node(self, node: RuleNode):
        self._append(node.name_node.name)
        if r := node.rhs.accept(self):
            node.rhs = r
        self._pop()

    def visit_alternation_node(self, node: AlternationNode):
        path = self.path.copy()
        for i, child in enumerate(node.nodes):
            if r := child.accept(self):
                node.nodes[i] = r
            self.path = path.copy()

    def visit_concatenation_node(self, node: ConcatenationNode):
        path = self.path.copy()
        for i, child in enumerate(node.nodes):
            if r := child.accept(self):
                node.nodes[i] = r
            child.accept(self)
            self.path = path.copy()

    def visit_repitition_node(self, node: RepititionNode):
        if r := node.target.accept(self):
            node.target = r

    def visit_option_node(self, node: OptionNode):
        if r := node.target.accept(self):
            node.target = r

    def visit_group_node(self, node: GroupNode):
        if r := node.target.accept(self):
            node.target = r

    def visit_rule_name_node(self, node: RuleNameNode):
        if node.name not in self.path:
            match rule := self.rules.get(node.name):
                case None:
                    return
                case _:
                    rule.accept(self)
        else:
            return DeferNode(node)

    def __getattr__(self, name):
        return self.fallback_visit

    def fallback_visit(self, node):
        pass
