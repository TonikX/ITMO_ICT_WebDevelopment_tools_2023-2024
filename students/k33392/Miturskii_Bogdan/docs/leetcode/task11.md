## Задание №11

Дано идеальное бинарное дерево, где все листья находятся на одном уровне, и каждый родитель имеет двух детей. Необходимо заполнить каждый указатель next, чтобы он указывал на следующий правый узел. Если следующего правого узла нет, указатель next должен быть установлен в NULL.

Изначально все указатели next установлены в NULL.

### Решение:

Для решения задачи заполнения указателей next в идеальном бинарном дереве будем использовать обход в ширину с использованием очереди. Проходим по каждому уровню дерева, заполняя указатели next для каждого узла. Возвращаем корень дерева с заполненными указателями next.

```typescript
/* class Node {
    val: number;
    left: Node | null;
    right: Node | null;
    next: Node | null;
    constructor(val?: number, left?: Node | null, right?: Node | null, next?: Node | null) {
        this.val = (val === undefined ? 0 : val);
        this.left = (left === undefined ? null : left);
        this.right = (right === undefined ? null : right);
        this.next = (next === undefined ? null : next);
    }
} */

function connect(root: Node | null): Node | null {
  if (root === null) {
    return null;
  }

  let queue: (Node | null)[] = [root];

  while (queue.length > 0) {
    let size = queue.length;
    let prev: Node | null = null;

    for (let i = 0; i < size; i++) {
      let node = queue.shift()!;

      if (prev !== null) {
        prev.next = node;
      }
      prev = node;

      if (node.left !== null) queue.push(node.left);
      if (node.right !== null) queue.push(node.right);
    }
  }

  return root;
}
```
