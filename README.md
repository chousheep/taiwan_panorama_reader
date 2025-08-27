# Taiwan Panorama Reader

**Taiwan Panorama Reader** is a Python tool that fetches and reads **Taiwan Panorama** articles in multiple languages. It is intended as a side project for language learning, which automatically detects available translations, parses tabbed article structures, and lets you read content in two modes:

- **Full-article mode** — prints the complete article per language.
- **Paragraph-by-paragraph mode** — interleaves matching paragraphs across multiple languages.

## Features
- Multi-language support: `zh`, `en`, `ja`, `vi`, `th`, `id` (depends on the languages offered by the original webpage)
- Two reading modes:
  - **Full-article** → outputs the full article per language.
  - **Paragraph-by-paragraph** → interleaves paragraphs across languages (when paragraphs match).
- Cleans up unwanted elements like scripts, styles, and image captions.

## Supported Languages
| Code | Label            |
| ---- | ---------------- |
| zh   | 繁體中文             |
| en   | English          |
| ja   | 日本語              |
| vi   | Tiếng Việt       |
| th   | ภาษาไทย          |
| id   | Bahasa Indonesia |

## Example
Let's say a user just chose zh and en as output langauges for a given article link, 

### Full-article mode: 

```
===== 繁體中文 =====
Taiwan Panorama 是中華民國官方的文化刊物，創刊於 1976 年...

（繁體中文全文）

===== English =====
Taiwan Panorama is an official cultural magazine of the Republic of China, founded in 1976...

(Full English Story)
```

### Paragraph-by-paragraph mode:

```
Taiwan Panorama 是中華民國官方的文化刊物，創刊於 1976 年...
Taiwan Panorama is an official cultural magazine of the Republic of China, founded in 1976...

Taiwan Panorama 是中華民國官方的文化刊物，創刊於 1976 年...
Taiwan Panorama is an official cultural magazine of the Republic of China, founded in 1976...

(Interleaved zh-en paragraphs)
```

## Installation
Clone the repository:

```
git clone https://github.com/chousheep/taiwan_panorama_reader.git
cd taiwan_panorama_reader
```

## Dependencies
### Using uv (recommended)
```
uv sync
```
Then start the program by running
```
uv run main.py
```
### Using pip 
```
source .venv/bin/activate
```
```
pip install -r requirements.txt
```
```
python3 main.py
```

## Disclaimer
This project is for educational purposes only.
By using this tool, you acknowledge and agree that:
* You are solely responsible for complying with the Taiwan Panorama Terms of Use.
* You authorize this program to send automated requests on your behalf.

## License
This project is licensed under the MIT License.
See the LICENSE file for details.

