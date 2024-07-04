import json

class AltairGraphComparer:
    """
    A class for comparing Altair chart objects based on their JSON representations.
    """

    @staticmethod
    def get_chart_json(chart) -> dict:
        """
        Converts an Altair chart or its JSON string representation to a Python dictionary.

        Args:
            chart (Union[str, AltairChart]): The Altair chart or its JSON string representation.

        Returns:
            dict: The JSON representation of the chart as a Python dictionary.
        """
        if isinstance(chart, str):
            return json.loads(chart)
        else:
            return json.loads(chart.to_json())
    
    @staticmethod
    def match(chart1, chart2) -> bool:
        """
        Compares two Altair charts for similarity based on their type and dataset values.

        Args:
            chart1 (Union[str, AltairChart]): The first Altair chart or its JSON string representation.
            chart2 (Union[str, AltairChart]): The second Altair chart or its JSON string representation.

        Returns:
            bool: True if the charts are similar based on their type and dataset values, False otherwise.
        """
        json1 = AltairGraphComparer.get_chart_json(chart1)
        json2 = AltairGraphComparer.get_chart_json(chart2)

        # Compare chart type ("mark" attribute)
        mark1 = json1.get('mark')
        mark2 = json2.get('mark')
        if mark1 != mark2:
            print(f"Chart type is different: {mark1} != {mark2}")
            return False

        # Get datasets values ignoring keys
        datasets1 = next(iter(json1.get('datasets', {}).values()), [])
        datasets2 = next(iter(json2.get('datasets', {}).values()), [])

        # Compare dataset values
        if datasets1 == datasets2:
            return True
        else:
            differences = []
            for idx, (item1, item2) in enumerate(zip(datasets1, datasets2)):
                for key in item1.keys() | item2.keys():
                    val1 = item1.get(key)
                    val2 = item2.get(key)
                    if val1 != val2:
                        differences.append(f"Dataset[{idx}].{key}: {val1} != {val2}")
            
            if differences:
                print("Differences in dataset values:")
                for diff in differences:
                    print(diff)
            return False