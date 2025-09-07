# 🏮 Taiwan Panorama Reader

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Taiwan Panorama](https://img.shields.io/badge/Source-Taiwan%20Panorama-red)](https://www.taiwan-panorama.com/)

A powerful Python command-line tool for reading **Taiwan Panorama** magazine articles in multiple languages. Perfect for language learners, researchers, and anyone interested in Taiwanese culture and multilingual content.

## 🌟 What is Taiwan Panorama?

[Taiwan Panorama](https://www.taiwan-panorama.com/) is the official cultural magazine of the Republic of China (Taiwan), published since 1976. It showcases Taiwan's rich culture, history, arts, cuisine, and contemporary life through high-quality articles available in multiple languages, making it an excellent resource for cultural exploration and language learning.

## ✨ Features

- 🌐 **Multi-language Support**: Automatically detects and processes articles in Chinese (Traditional), English, Japanese, Vietnamese, Thai, and Indonesian
- 📖 **Dual Reading Modes**: 
  - **Full-article mode** for complete immersion in each language
  - **Paragraph-by-paragraph mode** for side-by-side language comparison
- 🧹 **Clean Content Extraction**: Removes scripts, styles, ads, and other noise for distraction-free reading
- 🔍 **Smart Language Detection**: Automatically discovers available translations from any article URL
- 🎯 **Educational Focus**: Designed specifically for language learning and cultural exploration

## 🗣️ Supported Languages

| Code | Language         | Native Name      |
|------|------------------|------------------|
| `zh` | Chinese (Traditional) | 繁體中文       |
| `en` | English          | English          |
| `ja` | Japanese         | 日本語           |
| `vi` | Vietnamese       | Tiếng Việt       |
| `th` | Thai             | ภาษาไทย          |
| `id` | Indonesian       | Bahasa Indonesia |

## 🚀 Quick Start

### Prerequisites
- Python 3.13+ 
- Internet connection

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/chousheep/taiwan_panorama_reader.git
   cd taiwan_panorama_reader
   ```

2. **Install dependencies:**

   **Option A: Using uv (recommended)**
   ```bash
   uv sync
   ```

   **Option B: Using pip**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Usage

**With uv:**
```bash
uv run main.py
```

**With pip:**
```bash
python main.py
```

The tool will prompt you for:
1. A Taiwan Panorama article URL
2. Your preferred reading mode
3. Which languages you want to read

## 📚 Usage Examples

### Finding Articles
Visit [Taiwan Panorama](https://www.taiwan-panorama.com/) and copy any article URL, such as:
- `https://www.taiwan-panorama.com/en/Articles/Details?Guid=...`
- `https://www.taiwan-panorama.com/zh/Articles/Details?Guid=...`

### Example Output

**Full-article mode** (Chinese + English):
```
== 繁體中文 ==
台灣的夜市文化

夜市是台灣最具代表性的文化特色之一，從北到南都能找到各具特色的夜市...

== English ==
Taiwan's Night Market Culture

Night markets are one of Taiwan's most representative cultural features, with distinctive markets found from north to south...
```

**Paragraph-by-paragraph mode** (Chinese + English):
```
夜市是台灣最具代表性的文化特色之一，從北到南都能找到各具特色的夜市。
Night markets are one of Taiwan's most representative cultural features, with distinctive markets found from north to south.

每個夜市都有自己的招牌美食和獨特氛圍，成為觀光客必訪的景點。
Each night market has its own signature foods and unique atmosphere, making them must-visit destinations for tourists.
```

## 🛠️ Advanced Usage

### Batch Processing
The tool automatically detects all available language versions of an article. You can:
- Select specific languages: `zh en ja`
- Choose all available: Press Enter or type `all`

### Language Compatibility
For paragraph-by-paragraph mode, languages must have matching paragraph structures. The tool will automatically detect compatibility and suggest alternatives if needed.

## 🔧 Troubleshooting

### Common Issues

**"No language versions detected"**
- Ensure the URL is from taiwan-panorama.com
- Check that the article is properly published
- Verify your internet connection

**"Languages not compatible for paragraph-by-paragraph"**
- Some articles may have different structures across languages
- Try full-article mode instead
- This is normal for certain article types

**Connection timeout**
- Check your internet connection
- The site might be temporarily unavailable
- Try again in a few minutes

### Getting Help

If you encounter issues:
1. Check the [Taiwan Panorama website](https://www.taiwan-panorama.com/) is accessible
2. Verify you're using a valid article URL
3. Ensure your Python version is 3.13+

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs** by opening an issue
2. **Suggest features** for new functionality
3. **Submit pull requests** for improvements
4. **Improve documentation** and examples

### Development Setup
```bash
git clone https://github.com/chousheep/taiwan_panorama_reader.git
cd taiwan_panorama_reader
uv sync
uv run main.py
```

## 📋 Roadmap

- [ ] GUI interface
- [ ] Article export functionality (PDF, EPUB)
- [ ] Bookmark and reading history
- [ ] Audio pronunciation support
- [ ] Mobile app version
- [ ] Additional language support

## ⚖️ Legal & Ethics

This project is for **educational purposes only**. By using this tool, you acknowledge and agree that:

- ✅ You are solely responsible for complying with Taiwan Panorama's Terms of Use
- ✅ You authorize this program to send automated requests on your behalf
- ✅ This tool is intended for personal, educational, and research use
- ❌ Commercial use or redistribution of content is not permitted

Please respect the original content creators and Taiwan Panorama's intellectual property rights.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Taiwan Panorama Magazine for providing excellent multilingual content
- The open-source Python community for the amazing libraries used in this project
- Language learners and cultural enthusiasts who inspired this tool

---

**Made with ❤️ for language learners and Taiwan culture enthusiasts**

