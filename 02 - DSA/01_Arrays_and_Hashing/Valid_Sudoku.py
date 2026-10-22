class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        matrix = [set() for _ in range(9)]
        for row in range(9):
            for col in range(9):
                num = board[row][col]
                key = (row // 3) * 3 + (col // 3)
                if num == ".": continue
                if (
                    num in rows[row] or
                    num in cols[col] or
                    num in matrix[key]
                ): return False
                rows[row].add(num)
                cols[col].add(num)
                matrix[key].add(num)
        return True