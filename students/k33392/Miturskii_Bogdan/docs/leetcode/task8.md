## Задание №8

Дан корень бинарного дерева, вернуть порядок in-order обхода значений его узлов.

### Решение:

Для решения задачи in-order обхода бинарного дерева (левый узел, корень, правый узел) будем использовать рекурсивный подход.

```typescript
/* Класс предоставлен литкодом 
class TreeNode {
  val: number;
  left: TreeNode | null;
  right: TreeNode | null;
  constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {
    this.val = val === undefined ? 0 : val;
    this.left = left === undefined ? null : left;
    this.right = right === undefined ? null : right;
  }
} */

function inorderTraversal(root: TreeNode | null): number[] {
  const result: number[] = [];

  const traverse = (node: TreeNode | null) => {
    if (node !== null) {
      traverse(node.left);
      result.push(node.val);
      traverse(node.right);
    }
  };

  traverse(root);
  return result;
}
```
