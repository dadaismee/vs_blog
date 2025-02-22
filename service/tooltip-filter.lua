local bib_data = {}

-- Function to load bibliography into a table
local function load_bib(file)
  local bibtex = io.open(file, "r")
  if not bibtex then
    io.stderr:write("Error: Could not open bibliography file: " .. file .. "\n")
    return
  end

  local content = bibtex:read("*all")
  bibtex:close()

  for entry in content:gmatch("@%w+{(.-)}") do
    local id = entry:match("^(.-),")
    local metadata = entry:gsub("^(.-),", ""):gsub("\n", " "):gsub("%s+", " ")
    bib_data[id] = metadata
  end
end

-- Modify Meta function to load bibliography
function Meta (meta)
    -- Check if bibliography is passed via command line arguments
    if meta.commandLineArgs then
        for i, arg in ipairs(meta.commandLineArgs) do
            if arg:match("^--bibliography=(.*)$") then
                local bib_file = arg:match("^--bibliography=(.*)$")
                load_bib(bib_file)
                break
            end
        end
    end
    return meta
end

-- Replace citations with tooltips
function Cite(elem)
  local tooltip_content = ""
  for _, citation in ipairs(elem.citations) do
    local id = citation.id
    if bib_data[id] then
      tooltip_content = tooltip_content .. string.format(
        '<span class="tooltip">[%s]<span class="tooltiptext">%s</span></span>',
        id, bib_data[id]
      )
    else
      tooltip_content = tooltip_content .. string.format("[%s]", id)
    end
  end
  return pandoc.RawInline("html", tooltip_content)
end
