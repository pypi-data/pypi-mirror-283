import re

class NumericMatcher:
    """
    A class for matching numerical values extracted from strings to target numerical values.
    """

    def __init__(self):
        pass

    @staticmethod
    def normalize_numeric(input_str: str) -> list[float]:
        """
        Extracts and normalizes the numeric values from the input string.

        Args:
            input_str (str): The input string containing numeric values.

        Returns:
            list[float]: List of extracted and normalized numeric values. Returns an empty list if none are found.
        """
        normalized_values = []
        try:
            # Find all numeric parts from the input string
            numeric_parts = re.findall(r'[\d\.,]+', input_str)
            
            for numeric_part in numeric_parts:
                try:
                    # Replace commas and convert to float
                    numeric_value = float(numeric_part.replace(',', ''))
                    normalized_values.append(numeric_value)
                except ValueError:
                    pass
            
        except ValueError:
            pass
        
        return normalized_values

    def match(self, input_str: str, target: float) -> bool:
        """
        Checks if any of the extracted numeric values from the input string match the target value based on rounding rules.

        Args:
            input_str (str): The input string containing numeric values.
            target (float): The target numeric value to match.

        Returns:
            bool: True if any of the numeric values match the target value based on rounding rules, False otherwise.
        """
        # Normalize the numeric values from the input string
        numeric_values = self.normalize_numeric(input_str)
        
        # Check if there are any numeric values extracted
        if not numeric_values:
            return False
        
        # Iterate through each numeric value and check if it matches the target
        for numeric_value in numeric_values:
            if numeric_value < 1:
                # For numbers less than 1, match up to 2 decimal places
                if round(numeric_value, 2) == round(target, 2):
                    return True
            else:
                # Check if both numbers have decimal places
                if (numeric_value % 1 != 0) and (target % 1 != 0):
                    if round(numeric_value, 1) == round(target, 1):
                        return True
                # For numbers greater than or equal to 1, round and check if match
                elif round(numeric_value) == round(target):
                    return True
        
        return False
