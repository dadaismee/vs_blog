# ==== настройки путей ====

SRC_DIR      := src
BUILD_DIR    := build

GLOBAL_ASSETS_SRC := assets
GLOBAL_ASSETS_DST := $(BUILD_DIR)/assets

TEMPLATE     := default-new.html
BIB          := /Users/valerii/Obsidian/Service/zotero-library.json
CSL          := /Users/valerii/Obsidian/Service/apa-5th-edition.csl

PANDOC       := pandoc

# ==== список исходников ====

# все markdown и html файлы в src (глубина до 3 как в твоём find)
PAGES_MD    := $(shell find $(SRC_DIR) -maxdepth 3 -type f -name '*.md')
PAGES_HTML  := $(shell find $(SRC_DIR) -maxdepth 3 -type f -name '*.html')

# соответствующие html в build (та же структура, но без префикса src/)
BUILT_MD_HTML   := $(patsubst $(SRC_DIR)/%.md,$(BUILD_DIR)/%.html,$(PAGES_MD))
COPIED_HTML     := $(patsubst $(SRC_DIR)/%.html,$(BUILD_DIR)/%.html,$(PAGES_HTML))

# итоговая цель "собрать всё"
.PHONY: all
all: $(BUILT_MD_HTML) $(COPIED_HTML) assets

# ==== правила сборки ====

# 1) md -> html через pandoc (как в твоём скрипте)
$(BUILD_DIR)/%.html: $(SRC_DIR)/%.md $(TEMPLATE) append-back-after-source.lua target_blank.lua
	@mkdir -p $(dir $@)
	# найдём директорию страницы, чтобы pandoc мог видеть локальные assets
	page_dir=$(dir $<); \
$(PANDOC) --toc "$<" -o "$@" \
    --citeproc \
    --mathjax \
    --filter mermaid-filter \
    --lua-filter=append-back-after-source.lua \
    --lua-filter=target_blank.lua \
    --toc-depth=3 \
    --metadata link-citations=true \
    --bibliography="$(BIB)" \
    --csl="$(CSL)" \
    --section-divs \
    --template="$(TEMPLATE)" \
    --resource-path="$$page_dir:assets"

# 2) html в src просто копируем
$(BUILD_DIR)/%.html: $(SRC_DIR)/%.html
	@mkdir -p $(dir $@)
	cp "$<" "$@"

# 3) глобальные ассеты
.PHONY: assets
assets: | $(BUILD_DIR)
ifneq ("$(wildcard $(GLOBAL_ASSETS_SRC))","")
	@mkdir -p "$(GLOBAL_ASSETS_DST)"
	rsync -a "$(GLOBAL_ASSETS_SRC)/" "$(GLOBAL_ASSETS_DST)/"
endif
ifneq ("$(wildcard $(SRC_DIR)/assets)","")
	@mkdir -p "$(GLOBAL_ASSETS_DST)"
	rsync -a "$(SRC_DIR)/assets/" "$(GLOBAL_ASSETS_DST)/"
endif

# 4) создать build dir, если его нет
$(BUILD_DIR):
	@mkdir -p "$(BUILD_DIR)"

# ==== служебные цели ====

.PHONY: clean
clean:
	rm -rf "$(BUILD_DIR)"

.PHONY: serve
serve: all
	cd "$(BUILD_DIR)" && python3 -m http.server 8000
