function Link(el)
  -- Only add target="_blank" to external links starting with http:// or https://
  if el.target:match("^https?://") then
    el.attributes = el.attributes or {}
    el.attributes["target"] = "_blank"
    el.attributes["rel"] = "noopener noreferrer" -- security measure
  end
  return el
end
