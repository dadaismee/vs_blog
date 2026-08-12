# Названия файлов
INPUT = resume.md
META = assets/phd-meta.yaml
TEMPLATE = assets/template.docx
OUTPUT = resume-eng.docx

all: $(OUTPUT)

$(OUTPUT): $(INPUT) $(META) $(TEMPLATE)
	@echo "Сборка диссертации по ГОСТ..."
	pandoc $(INPUT) \
		--reference-doc=$(TEMPLATE) \
		--metadata-file=$(META) \
		--lua-filter=pagebreak.lua \
		--table-caption-position=below \
		--metadata link-citations=true \
		--citeproc \
		-o $(OUTPUT)

		# --lua-filter=add-math-spacer.lua \
