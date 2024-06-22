## Задание №9

Дан корень бинарного дерева, вернуть зигзагообразный обход уровней значений его узлов (т.е. сначала слева направо, затем справа налево для следующего уровня и чередовать между ними).

### Решение:

Для решения задачи зигзагообразного обхода бинарного дерева будем использовать обход в ширину с очередью и переменной для отслеживания направления обхода.

```typescript
/* class TreeNode {
  val: number;
  left: TreeNode | null;
  right: TreeNode | null;
  constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {
    this.val = val === undefined ? 0 : val;
    this.left = left === undefined ? null : left;
    this.right = right === undefined ? null : right;
  }
} */

function zigzagLevelOrder(root: TreeNode | null): number[][] {
  if (root === null) return [];

  const result: number[][] = [];
  const queue: TreeNode[] = [root];
  let leftToRight = true;

  while (queue.length > 0) {
    const levelSize = queue.length;
    const currentLevel: number[] = [];

    for (let i = 0; i < levelSize; i++) {
      const node = queue.shift();

      if (node) {
        if (leftToRight) {
          currentLevel.push(node.val);
        } else {
          currentLevel.unshift(node.val);
        }

        if (node.left) queue.push(node.left);
        if (node.right) queue.push(node.right);
      }
    }

    result.push(currentLevel);
    leftToRight = !leftToRight;
  }

  return result;
}
```
