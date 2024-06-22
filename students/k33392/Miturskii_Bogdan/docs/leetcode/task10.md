## Задание №10

Даны два целочисленных массива preorder и inorder, где preorder — это порядок обхода дерева в прямом порядке, а inorder — это порядок обхода дерева в симметричном порядке. Постройте и верните бинарное дерево.

### Решение:

Для решения задачи построения бинарного дерева из порядков обхода preorder и inorder используем рекурсивный подход:

- Первый элемент в preorder всегда является корнем.
- Найдем этот корень в inorder, чтобы определить левое и правое поддеревья.
- Рекурсивно построим левое и правое поддеревья.

```typescript
/* class TreeNode {
    val: number;
    left: TreeNode | null;
    right: TreeNode | null;
    constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {
        this.val = (val === undefined ? 0 : val);
        this.left = (left === undefined ? null : left);
        this.right = (right === undefined ? null : right);
    }
} */

function buildTree(preorder: number[], inorder: number[]): TreeNode | null {
  if (!preorder.length || !inorder.length) {
    return null;
  }

  const rootVal = preorder[0];
  const root = new TreeNode(rootVal);
  const rootIndex = inorder.indexOf(rootVal);

  root.left = buildTree(
    preorder.slice(1, rootIndex + 1),
    inorder.slice(0, rootIndex)
  );
  root.right = buildTree(
    preorder.slice(rootIndex + 1),
    inorder.slice(rootIndex + 1)
  );

  return root;
}
```
