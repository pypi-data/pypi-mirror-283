## Installation

To use this module, you need to have Python >=3.7 installed on your system. You can do this using pip:

Run 
```pip install llm-similarity-checker```


## Overview

This module is designed to handle various tasks related to sentence similarity, numeric extraction and comparison, and Altair graph comparison. The core functionality includes:

- Comparing sentences using transformer models and computing similarity scores.
- Extracting and matching numerical values within strings to target numerical values.
- Comparing two Altair graphs to determine their similarity.


### AnalysisMatcher

This class performs sentence comparison using state-of-the-art transformer models in natural language processing (NLP). Leveraging the Hugging Face transformers library, it tokenizes input sentences, extracts embeddings using a pre-trained model, and calculates similarity scores between sentences.

Example:
```python
from similarity_checker import AnalysisMatcher

reference = "This indicates a statistically significant difference in the average incomes of males and females in the dataset."

target1 = "We can conclude there is no statistically significant difference in the average incomes of males and females in this dataset."
target2 = "We can conclude there is statistically significant difference in the average incomes of males and females in this dataset."

# Initialize the AnalysisMatcher
matcher = AnalysisMatcher()

# Perform matching
result1_score, result1_match = matcher.match(reference, target1)
result2_score, result2_match = matcher.match(reference, target2)

# Print results
print(f"Match result for target 1: Score = {result1_score}, Match = {result1_match}")
print(f"Match result for target 2: Score = {result2_score}, Match = {result2_match}")
```

Output:
```bash
Match results for sentence1:
(0.24839641153812408, False)

Match results for sentence2:
(0.6842396259307861, True)
```


### NumericMatcher

This class focuses on extracting numerical values from strings and comparing them against target values. It uses regular expressions to locate and normalize numeric values from input strings, handling variations like comma separators.

Example:
```python
sentence = "The top 5 most preferred car brands in the UAE, based on the average proportion across cities, are:\n\n| brand         | avg_proportion   |\n|:--------------|:-----------------|\n| Nissan        | 0.159158         |\n| Toyota        | 0.0978399        |\n| Mercedes-Benz | 0.0843513        |\n| Honda         | 0.0776763        |\n| BMW           | 0.056902         |"

target1 = 0.159
target2 = 0

matcher = NumericMatcher()

result1_match = matcher.match(sentence, target1)
result2_match = matcher.match(sentence, target2)

print(f"Match result for target 1: Match = {result1_match}")
print(f"Match result for target 2: Match = {result2_match}")
```

Output:
```bash
Match result for target 1: Match = True
Match result for target 2: Match = False
```

### AltairGraphComparer

This class compares two Altair graphs to determine their similarity.

Example:
```python
chart1 = "{\"config\": {\"view\": {\"continuousWidth\": 400, \"continuousHeight\": 300}}, \"data\": {\"name\": \"data-679d61f96919a9b00678a3858e27aa15\"}, \"mark\": \"bar\", \"encoding\": {\"tooltip\": [{\"field\": \"month\", \"type\": \"nominal\"}, {\"field\": \"booking_duration\", \"type\": \"quantitative\"}], \"x\": {\"axis\": {\"labelAngle\": -45, \"title\": \"Month\"}, \"field\": \"month\", \"sort\": null, \"type\": \"nominal\"}, \"y\": {\"field\": \"booking_duration\", \"title\": \"Average Booking Duration (Days)\", \"type\": \"quantitative\"}}, \"selection\": {\"selector001\": {\"type\": \"interval\", \"bind\": \"scales\", \"encodings\": [\"x\", \"y\"]}}, \"title\": \"Average Booking Duration by Month\", \"$schema\": \"https://vega.github.io/schema/vega-lite/v4.17.0.json\", \"datasets\": {\"data-679d61f96919a9b00678a3858e27aa15\": [{\"month\": \"January\", \"booking_duration\": -778.581308411215, \"month_order\": 0}]}}"

chart2 = "{\"config\": {\"view\": {\"continuousWidth\": 400, \"continuousHeight\": 300}}, \"data\": {\"name\": \"data-71fd4bd6411150f723ef9e15bf55c9ea\"}, \"mark\": \"bar\", \"encoding\": {\"tooltip\": [{\"field\": \"month\", \"type\": \"nominal\"}, {\"field\": \"booking_duration\", \"type\": \"quantitative\"}], \"x\": {\"axis\": {\"labelAngle\": -45, \"title\": \"Month\"}, \"field\": \"month\", \"sort\": null, \"type\": \"nominal\"}, \"y\": {\"field\": \"booking_duration\", \"title\": \"Average Booking Duration (Days)\", \"type\": \"quantitative\"}}, \"selection\": {\"selector001\": {\"type\": \"interval\", \"bind\": \"scales\", \"encodings\": [\"x\", \"y\"]}}, \"title\": \"Average Booking Duration by Month\", \"$schema\": \"https://vega.github.io/schema/vega-lite/v4.17.0.json\", \"datasets\": {\"data-71fd4bd6411150f723ef9e15bf55c9ea\": [{\"month\": \"January\", \"booking_duration\": 1.8288770053475936, \"month_order\": 0}]}}"

matcher = AltairGraphComparer()
result_match = matcher.match(chart1, chart2)

print(f"Match result for target: Match = {result_match}")
```

Output:
```bash
Differences in dataset values:
Dataset[0].booking_duration: -778.581308411215 != 1.8288770053475936
Match result for target: Match = False
```