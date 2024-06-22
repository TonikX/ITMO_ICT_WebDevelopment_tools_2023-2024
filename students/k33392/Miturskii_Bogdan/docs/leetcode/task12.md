## Задание №12

Дан корень бинарного дерева поиска и целое число k. Необходимо вернуть k-е наименьшее значение (с 1-индексацией) среди всех значений узлов в дереве.

### Решение:

Для решения задачи нахождения k-го наименьшего значения в бинарном дереве поиска используем обход in-order, так как при таком обходе значения узлов в бинарном дереве поиска будут отсортированы в порядке возрастания.

```typescript
/*
class TreeNode {
    val: number;
    left: TreeNode | null;
    right: TreeNode | null;
    constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {
        this.val = (val === undefined ? 0 : val);
        this.left = (left === undefined ? null : left);
        this.right = (right === undefined ? null : right);
    }
}
*/

function kthSmallest(root: TreeNode | null, k: number): number {
  let stack: TreeNode[] = [];
  let current = root;
  let count = 0;

  while (stack.length > 0 || current !== null) {
    while (current !== null) {
      stack.push(current);
      current = current.left;
    }

    current = stack.pop()!;
    count++;
    if (count === k) {
      return current.val;
    }

    current = current.right;
  }
}
```
