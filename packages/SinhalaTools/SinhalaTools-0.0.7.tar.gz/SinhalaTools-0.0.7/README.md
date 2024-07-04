# Sinhala Tools

A Python package to help with various Sinhala language processing tasks.

## Features

- Convert Sinhala text to Roman characters (Singlish) and vice versa.

- Translate text and files between Sinhala and other languages using Google Translate.

- Use Google Input Tools to convert text to Sinhala.

- Find possible Sinhala matches for Singlish input.

## Installation

Install the package via pip:

```bash
pip install SinhalaTools
```

# Usage

### Convert Sinhala to Roman

```python
from SinhalaTools import sinhala_to_roman

sinhala_text = "සිංහල"
result = sinhala_to_roman(sinhala_text )
print(result)
```

### Convert Roman to Sinhala

```python
from SinhalaTools import roman_to_sinhala

roman_text = "siṃhala"
sinhala_text = roman_to_sinhala(roman_text)
print(sinhala_text)
```

### Convert Using Google Input Tools

```python
from SinhalaTools import inputTools

text = "sinhala"
result = inputTools(text)
print(result)
```

### Finding Possible Matches

```python
from SinhalaTools import possible_matches

input_str = "sinhala"
matches = possible_matches(input_str)
print(matches)
```

### Translate a Text String

```python
from SinhalaTools import translate

text = "Hello, how are you?"
translated_text = translate(text, source_language='en', target_language='si')
print(translated_text)
```

### Translate a File

```python
from SinhalaTools import translate_file

file = "sample.txt"
translated_text = translate_file(file, source_language='en', target_language='si')
print(translated_text)
```

## Contact

For any inquiries or issues, please contact [tharindu.20@cse.mrt.ac.lk](tharindu.20@cse.mrt.ac.lk).
