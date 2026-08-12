import re
import sys

def array_to_md_table(block: str) -> str:
    # вырезаем \begin{array}{...} и \end{array}
    block = re.sub(r"\\begin\{array\}\{[^}]*\}", "", block)
    block = re.sub(r"\\end\{array\}", "", block)
    block = re.sub(r"\\hline", "", block)

    # делим по строкам LaTeX-таблицы
    rows = [r.strip() for r in block.split(r"\\") if r.strip()]
    if not rows:
        return block

    # парсим строки по &
    parsed = [[c.strip() for c in row.split("&")] for row in rows]

    # выравниваем длины строк по максимуму
    max_cols = max(len(r) for r in parsed)
    for r in parsed:
        while len(r) < max_cols:
            r.append("")

    header = parsed[0]
    body = parsed[1:]

    # строим markdown
    lines = []
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * max_cols) + " |")
    for r in body:
        lines.append("| " + " | ".join(r) + " |")

    return "\n".join(lines)


if __name__ == "__main__":
    # читаем весь stdin и конвертируем только содержимое между $$...$$
    text = sys.stdin.read()

    def repl(m):
        inner = m.group(1)
        return array_to_md_table(inner)

    pattern = r"\$\$(.*?)\$\$"
    out = re.sub(pattern, repl, text, flags=re.DOTALL)

    sys.stdout.write(out)