from paquetekata04.field import Field

class ConverterService:
    @staticmethod
    def validate_matrix_format(lines):
        # Check if there are at least two lines (header and at least one row)
        if len(lines) < 2:
            return False
        
        # Check header format
        header = lines[0].strip()
        if not header:
            return False
        
        try:
            rows, cols = map(int, header.split())
        except ValueError:
            return False
        
        # Check if the number of rows matches the header
        if len(lines[1:]) != rows:
            return False
        
        # Check if each row has exactly 'cols' characters
        for line in lines[1:]:
            if len(line.strip()) != cols:
                return False
        
        return True

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
            
            try:
                rows, cols = map(int, header.split())
            except ValueError:
                continue
            
            if rows == 0 and cols == 0:
                break
            
            if index + rows > len(lines):
                # Inconsistent number of rows
                continue
            
            array_matrix = lines[index:index + rows]
            index += rows
            
            if not ConverterService.validate_matrix_format([header] + array_matrix):
                # Invalid matrix format, skip
                continue
            
            field = Field(rows, cols, array_matrix)
            converted_matrix += f"Field #{matrix_num}:\n"
            converted_matrix += field.convert_to_string()
            matrix_num += 1
        
        return converted_matrix
