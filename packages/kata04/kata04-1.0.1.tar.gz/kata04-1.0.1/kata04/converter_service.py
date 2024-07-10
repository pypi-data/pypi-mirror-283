from paquetekata04.field import Field

class ConverterService:
    @staticmethod
    def convertMatrix(matrix):
        lines = matrix.split("\n")
        converted_matrix = ""
        matrix_num = 1
        index = 0
        
        while index < len(lines):
            header = lines[index].strip()
            index += 1
            
            if not header:
                continue
            
            rows, cols = map(int, header.split())
            
            if rows == 0 and cols == 0:
                break
            
            array_matrix = []
            for _ in range(rows):
                if index < len(lines):
                    array_matrix.append(lines[index])
                    index += 1
            
            field = Field(rows, cols, array_matrix)
            converted_matrix += f"Field #{matrix_num}:\n"
            converted_matrix += field.convert_to_string()
            matrix_num += 1
        
        return converted_matrix
