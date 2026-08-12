#!/usr/bin/awk -f

BEGIN {
    in_array = 0
    row_count = 0
}

# печать md-таблицы из rows[0..row_count-1]
function print_md_table(    i,j,max_cols,cols,line,cell) {
    if (row_count == 0) return

    max_cols = 0
    for (i = 0; i < row_count; i++) {
        n = split(rows[i], cols, "\t")
        if (n > max_cols) max_cols = n
    }

    # header
    split(rows[0], cols, "\t")
    line = "|"
    for (j = 1; j <= max_cols; j++) {
        cell = (j in cols ? cols[j] : "")
        line = line " " cell " |"
    }
    print line

    # separator
    line = "|"
    for (j = 1; j <= max_cols; j++) {
        line = line " --- |"
    }
    print line

    # body
    for (i = 1; i < row_count; i++) {
        split(rows[i], cols, "\t")
        line = "|"
        for (j = 1; j <= max_cols; j++) {
            cell = (j in cols ? cols[j] : "")
            line = line " " cell " |"
        }
        print line
    }
}

# вытаскиваем все строки из переменной s, разделённые на части по '\\'
function split_rows(s,    pos, chunk) {
    while (1) {
        pos = index(s, "\\\\")
        if (pos == 0) {
            # остаток без '\\'
            gsub(/^ *& */, "", s)
            if (length(s) > 0) {
                gsub(/ *& */, "\t", s)
                rows[row_count++] = s
            }
            break
        }
        # всё до '\\'
        chunk = substr(s, 1, pos - 1)
        s = substr(s, pos + 2)
        gsub(/^ *& */, "", chunk)
        if (length(chunk) > 0) {
            gsub(/ *& */, "\t", chunk)
            rows[row_count++] = chunk
        }
    }
}

{
    if (!in_array) {
        # ищем начало $$\begin{array}
        if ($0 ~ /\$\$/ && $0 ~ /\\begin\{array\}/) {
            in_array = 1
            row_count = 0

            line = $0
            # убираем всё до \begin{array}{...}
            sub(/.*\\begin\{array\}\{[^}]*\}/, "", line)
            gsub(/\\hline/, "", line)
            gsub(/\$\$/, "", line)

            if (length(line) > 0)
                split_rows(line)

            next
        } else {
            print $0
            next
        }
    } else {
        # внутри array
        if ($0 ~ /\\end\{array\}/) {
            line = $0
            sub(/\\end\{array\}.*/, "", line)
            gsub(/\\hline/, "", line)
            gsub(/\$\$/, "", line)

            if (length(line) > 0)
                split_rows(line)

            print_md_table()

            in_array = 0
            row_count = 0
            next
        }

        line = $0
        gsub(/\\hline/, "", line)
        if (length(line) > 0)
            split_rows(line)
    }
}