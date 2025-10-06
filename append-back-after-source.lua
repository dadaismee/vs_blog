function Div(el)
  -- Check if this div is a reference entry (usually has 'ref-' prefix in id)
  if el.identifier and el.identifier:match("^ref%-") then
    -- Create a back button html block
    local back_button_html = '<button class="footnote-back" onclick="history.back()" style="border: none; color: blue">↩︎</button>'
    -- Append the button as a RawBlock after the existing content
    table.insert(el.content, pandoc.RawBlock('html', back_button_html))
    return el
  end
end
