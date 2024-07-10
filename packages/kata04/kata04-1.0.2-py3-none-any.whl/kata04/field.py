class Field:
    def __init__(self, rows, cols, matrix_lines):
        self.rows = rows
        self.cols = cols
        self.matrix_lines = matrix_lines
    
    def convert_to_string(self):
        converted_matrix = ""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix_lines[i][j] == '*':
                    converted_matrix += '*'
                else:
                    count = self.count_adjacent_mines(i, j)
                    converted_matrix += str(count)
            converted_matrix += '\n'
        return converted_matrix
    
    def count_adjacent_mines(self, row, col):
        count = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = row + di, col + dj
                if 0 <= ni < self.rows and 0 <= nj < self.cols and self.matrix_lines[ni][nj] == '*':
                    count += 1
        return count
