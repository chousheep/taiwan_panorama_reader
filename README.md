# Taiwan Panorama Reader
This tool allows you to fetch and display articles from Taiwan Panorama in multiple languages. It supports two modes of reading: full-article mode and paragraph-by-paragraph mode.

## Features
- **Multi-language Support**: Handles articles in languages such as Traditional Chinese, English, Japanese, Vietnamese, Thai, and Indonesian.
- **Customizable Output**: Choose between full-article or interleaved paragraph-by-paragraph display.

**Supported Languages** (depends on languages found in the aritcle)
    | Language          | Code  |
    |-------------------|-------|
    | 繁體中文 | zh |
    | English           | en    |
    | 日本語          | ja    |
    | Tiếng Việt        | vi    |
    | ภาษาไทย            | th    |
    | Bahasa Indonesia        | id    |

## Implementation
### Using uv (recommended)
1. Syncing dependencies
    ```
    uv sync
    ```
2. Run the script:
    ```
    uv run main.py
    ```

### Using pip
1. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
2. Activating venv
    ```
    source .venv/bin/activate
    ```
3. Run the script:
    ```
    pytho3 main.py
    ```

## Disclaimer
By using this tool, you agree to comply with Taiwan Panorama's Terms of Use and authorize the program to send automated requests on your behalf.

## Notes
- Ensure the input URL is a valid Taiwan Panorama article link.
- The tool may not work if the website structure changes or if the article is unavailable.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
