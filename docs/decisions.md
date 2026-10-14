# Design decisions

[Project](../README.md) · [Architecture](architecture.md) · [Code tour](code-tour.md)

## Represent formulas structurally

The TypeScript parser converts authored formulas into AST nodes. Backend compilation and dependency handling are separate responsibilities. [Inspect the source](../evidence/E08.md).

## Make dependency cycles explicit

The compiler includes deterministic Tarjan strongly connected components for the dependency graph. The offline sample exercises the separate temporal evaluator. [Inspect the source](../evidence/E09.md).

## Separate authored and computed state

The budget grid keeps drafts, committed cells, computed values and preview sequence state apart, including protection against stale previews. [Inspect the source](../evidence/E10.md).

## Reuse the backend through an adapter

Sheets reads bounded workbook context and performs deterministic readbacks. Calculation and model execution remain in the backend. [Inspect the source](../evidence/E19.md).

