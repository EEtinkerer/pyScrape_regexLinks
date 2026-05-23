
# linkregex

`linkregex` converts sample URLs into generalized Python regex patterns.

Useful when scraping pages with BeautifulSoup and you want to find links similar to one or more known examples.

---

## Features

- Converts sample URLs into reusable regex patterns
- Supports multiple URLs
- Supports input files
- Optional output file support
- Windows or Unix line ending selection
- Skip-on-error or stop-on-error behavior

---

## Example

```bash
python linkregex.py -u "https://example.com/products/widget-123.html"
```

Output:

```python
r'https?://example\.com/[\w-]+/[\w-]+\.\w+'
```

---

## Multiple URLs

```bash
python linkregex.py   -u "https://example.com/products/widget-123.html"   -u "https://example.com/blog/post-name"
```

---

## Input File

```bash
python linkregex.py -i urls.txt -o patterns.txt --unix
```

---

## Options

| Option | Description |
|---|---|
| `-u`, `--url` | Add a URL directly |
| `-i`, `--input` | Read URLs from a file |
| `-o`, `--output` | Write output to a file |
| `--win` | Use Windows CRLF line endings |
| `--unix` | Use Unix LF line endings |
| `--skiponerror` | Skip bad inputs |
| `--stoponerror` | Stop on first error |

---

## GitHub Setup

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
```

Then create a GitHub repository and run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/linkregex.git
git push -u origin main
```

---

## License

MIT
