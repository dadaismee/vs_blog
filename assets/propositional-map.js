/* propositional-map.js — external script for default-new.html
 *
 * «Скролл-линия понятий»: понятия и отношения появляются в карте
 * сверху-вниз в порядке их первого упоминания в тексте, ПО МЕРЕ СКРОЛЛА.
 * Скроллишь вниз — новое понятие входит в карту снизу. Скроллишь обратно —
 * оно снова исчезает (класс .hidden, visibility:hidden).
 *
 * Отличия от «графа»: никакой физики. Карта = вертикальный стек по порядку
 * появления. Новое отношение рисуется стрелкой ВВЕРХ к тому месту, где
 * понятие было встречено раньше.
 *
 * Источник данных: triple-аннотации [...] внутри <code> в <article>.
 * Формат: [subject|relation|object|domain] (или через запятую, 3–4 поля).
 */
(function () {
  var article = document.querySelector("article");
  var mapEl = document.getElementById("triple-map");
  if (!article || !mapEl) return;

  // ---------- vocabulary: relation normalization (mirrors cg) ----------
  var RELATION_SYNONYMS = {
    "is_a":"is_a","is a":"is_a","are":"is_a","is":"is_a",
    "part_of":"part_of","part of":"part_of","component_of":"part_of",
    "has_attribute":"has_attribute","has":"has_attribute","has_property":"has_attribute",
    "requires":"requires","needs":"requires","depends_on":"requires",
    "cause_of":"cause_of","causes":"cause_of","leads_to":"cause_of","results_in":"cause_of",
    "enables":"enables","allows":"enables","makes_possible":"enables",
    "contrasts_with":"contrasts_with","contrasts":"contrasts_with","opposes":"contrasts_with",
    "analogous_to":"analogous_to","analogous":"analogous_to","similar_to":"analogous_to",
    "fuses_with":"fuses_with","fuses":"fuses_with","merges_with":"fuses_with",
    "synthesizes":"synthesizes","combines":"synthesizes","integrates":"synthesizes","creates":"synthesizes",
    "references":"references","refers_to":"references","cites":"references",
    "asserts":"asserts","claims":"asserts","argues":"asserts","states":"asserts",
    "evolves_to":"evolves_to","evolves":"evolves_to","develops_into":"evolves_to",
    "conflicts_with":"conflicts_with","conflicts":"conflicts_with",
    "represents":"represents","represent":"represents","map":"represents","maps":"represents",
    "maps_to":"represents","encode":"represents","encodes":"represents","embody":"represents",
    "embodies":"represents"
    // author's own additions go here, e.g.:
    // ,"is-an-a-priori-form-of": "is_a"
  };
  var CANONICAL = {};
  Object.keys(RELATION_SYNONYMS).forEach(function (k) { CANONICAL[RELATION_SYNONYMS[k]] = true; });
  function normalizeRelation(rel) {
    var key = rel.toLowerCase().trim().replace(/\s+/g, "_");
    return RELATION_SYNONYMS[key] || rel;
  }

  // ---------- PART 1: PARSE ----------
  // Читает <code>-блоки в статье, вытаскивает triple-аннотации.
  // Для каждого найденного triple запоминает: subject/relation/object/domain,
  // order (порядок появления) и y (позицию в документе) — для видимости.
  function parseTriples() {
    var triples = [];
    var codes = article.querySelectorAll("code");
    codes.forEach(function (code) {
      var text = code.textContent;
      var pre = code.closest("pre");
      var y = code.getBoundingClientRect().top + window.scrollY;
      var lines = pre ? text.split("\n") : [text];
      lines.forEach(function (line) {
        var m = line.match(/\[([^\]]*)\]/);
        if (!m) return;
        var parts = (m[1].indexOf("|") !== -1 ? m[1].split("|") : m[1].split(","))
          .map(function (s) { return s.trim(); })
          .filter(function (s) { return s !== ""; });
        if (parts.length < 3) return;
        // пропускаем format-шаблоны вида [subject, typed relation, object, domain]
        var literal = ["subject", "typed relation", "relation", "object", "domain"];
        if (literal.indexOf(parts[0].toLowerCase()) !== -1) return;
        var rel = normalizeRelation(parts[1]);
        triples.push({
          subject: parts[0],
          relation: rel,
          original: parts[1],
          object: parts[2],
          domain: parts[3] || "",
          canonical: !!CANONICAL[rel],
          order: triples.length + 1,
          y: y,
          provenance: (pre ? code.textContent : text).replace(/\s+/g, " ").trim()
        });
      });
    });
    return triples;
  }

  // ---------- PART 2: STATE (полный граф, строится один раз) ----------
  function buildGraph(triples) {
    var graph = { nodes: {}, links: [] };
    function ensureNode(name, order, y) {
      if (graph.nodes[name]) return graph.nodes[name];
      graph.nodes[name] = { name: name, firstOrder: order, firstY: y, prov: [], places: [] };
      return graph.nodes[name];
    }
    triples.forEach(function (t) {
      var s = ensureNode(t.subject, t.order, t.y);
      var o = ensureNode(t.object, t.order, t.y);
      s.prov.push(t.provenance);
      o.prov.push(t.provenance);
      s.places.push({ y: t.y, prov: t.provenance });
      o.places.push({ y: t.y, prov: t.provenance });
      graph.links.push({
        s: t.subject, o: t.object,
        relation: t.relation, original: t.original,
        canonical: t.canonical, domain: t.domain,
        order: t.order, y: t.y, provenance: t.provenance
      });
    });
    Object.keys(graph.nodes).forEach(function (n) {
      var node = graph.nodes[n];
      node.prov = node.prov.filter(function (v, i, a) { return a.indexOf(v) === i; });
      var seen = {};
      node.places = node.places.filter(function (p) { if (seen[p.y]) return false; seen[p.y] = true; return true; });
    });
    return graph;
  }

  // ---------- PART 3: LAYOUT (куда ставить) ----------
  // Нода встаёт сверху-вниз по порядку первого упоминания. Компактный стек.
  function layout(graph, W, H) {
    var names = Object.keys(graph.nodes).sort(function (a, b) {
      return graph.nodes[a].firstOrder - graph.nodes[b].firstOrder;
    });
    var step = Math.max(44, H / Math.max(1, names.length));
    names.forEach(function (name, i) {
      var n = graph.nodes[name];
      n.y = step * (i + 1);
      n.x = i % 3 === 0 ? W * 0.25 : i % 3 === 1 ? W * 0.5 : W * 0.75; // зигзаг
    });
  }

  // ---------- PART 4: RENDER ----------
  // Рисует только «открытые» элементы (order <= cut). cut от скролла.
  var tooltip = null;
  function showTooltip(e, data) {
    if (!tooltip) {
      tooltip = document.createElement("div");
      tooltip.className = "tm-tooltip";
      document.body.appendChild(tooltip);
    }
    var flags = (data.flags || []).map(function (f) {
      return '<div class="tm-flag">\u26a0 ' + f + '</div>';
    }).join("");
    var prov = (data.provenance || "").split("|").map(function (s) {
      return '<div class="tm-prov">' + s.trim() + '</div>';
    }).join("");
    tooltip.innerHTML = '<div class="tm-rel">' + data.relation + '</div>' +
      (data.provenance ? '<div class="tm-prov-label">in the text:</div>' + prov : "") + flags;
    tooltip.style.left = (e.clientX + 14 < window.innerWidth - 280 ? e.clientX + 14 : e.clientX - tooltip.offsetWidth - 14) + "px";
    tooltip.style.top  = (e.clientY + 12) + "px";
    tooltip.style.display = "block";
  }
  function hideTooltip() { if (tooltip) tooltip.style.display = "none"; }

  // ---------- PART 4b: КЛИК — переход к месту в тексте ----------
  var panel = null;
  function closePanel() { if (panel) { panel.parentNode.removeChild(panel); panel = null; } }
  function jumpTo(y) { closePanel(); window.scrollTo({ top: Math.max(0, y - 60), behavior: "smooth" }); }
  function showPlacesPanel(n, graph) {
    closePanel();
    panel = document.createElement("div");
    panel.className = "tm-panel";
    var places = n.places.length ? n.places : [{ y: n.firstY, prov: "first mention" }];
    var html = '<div class="tm-panel-title">' + n.name + '</div>';
    html += '<div class="tm-panel-links">' + (places.length > 1 ? 'used in ' + places.length + ' places:' : 'used here:') + '</div>';
    places.forEach(function (p, k) {
      html += '<div class="tm-panel-item" data-y="' + p.y + '">\u25b8 ' + (k + 1) + '. ' + (p.prov || "").slice(0, 88) + '</div>';
    });
    html += '<div class="tm-panel-links">links:</div>';
    graph.links.forEach(function (l) {
      if (l.s !== n.name && l.o !== n.name) return;
      var other = l.s === n.name ? l.o : l.s;
      var dir = l.s === n.name ? "\u2192" : "\u2190";
      html += '<div class="tm-panel-link" data-y="' + l.y + '">\u2192 ' + l.relation + ' ' + dir + ' ' + other + '</div>';
    });
    panel.innerHTML = html;
    panel.addEventListener("click", function (e) {
      var tgt = e.target.closest("[data-y]");
      if (tgt) jumpTo(parseFloat(tgt.getAttribute("data-y")));
    });
    document.body.appendChild(panel);
    var mr = mapEl.getBoundingClientRect();
    panel.style.left = (mr.left - 8) + "px";
    panel.style.top = (mr.top + 8) + "px";
  }
  document.addEventListener("click", function (e) {
    if (panel && !panel.contains(e.target) && !e.target.closest(".triple-map .node")) closePanel();
  });

  function render(graph, cut, svg, W, H) {
    svg.innerHTML = "";
    var NS = "http://www.w3.org/2000/svg";
    var px = function (s) { return document.createElementNS(NS, s); };

    // стрелка-маркер: треугольник на конце ребра, orient=auto поворачивает
    // его по направлению линии (от subject к object).
    var defs = px("defs");
    var marker = px("marker");
    marker.setAttribute("id", "pm-arrow");
    marker.setAttribute("viewBox", "0 0 10 10");
    marker.setAttribute("refX", "9"); marker.setAttribute("refY", "5");
    marker.setAttribute("markerWidth", "7"); marker.setAttribute("markerHeight", "7");
    marker.setAttribute("orient", "auto-start-reverse");
    var triPath = px("path");
    triPath.setAttribute("d", "M0,0 L10,5 L0,10 z");
    triPath.setAttribute("class", "arrow");
    marker.appendChild(triPath);
    defs.appendChild(marker);
    svg.appendChild(defs);

    // ребро показываем, если его предложение уже открыто (order <= cut).
    // одно и то же ребро (s→o) не рисуем дважды.
    var seen = {};
    graph.links.forEach(function (link) {
      if (link.order > cut) return;
      var id = [link.s, link.o].sort().join("\u2192");
      if (seen[id]) return;
      seen[id] = true;
      var ns = graph.nodes[link.s];
      var no = graph.nodes[link.o];
      var flagged = !link.canonical;

      var line = px("line");
      line.setAttribute("class", flagged ? "link flag" : "link");
      line.setAttribute("x1", ns.x); line.setAttribute("y1", ns.y);
      line.setAttribute("x2", no.x); line.setAttribute("y2", no.y);
      line.setAttribute("marker-end", "url(#pm-arrow)");
      line.addEventListener("click", function () { jumpTo(link.y); });
      svg.appendChild(line);

      // подпись отношения посредине ребра
      var lbl = px("text");
      lbl.setAttribute("class", flagged ? "link-label flag" : "link-label");
      var midx = (ns.x + no.x) / 2, midy = (ns.y + no.y) / 2;
      lbl.setAttribute("x", midx); lbl.setAttribute("y", midy - 2);
      lbl.setAttribute("text-anchor", "middle");
      lbl.textContent = flagged ? link.original + " \u26a0" : link.relation;
      lbl.style.cursor = "pointer";
      lbl.addEventListener("click", function () { jumpTo(link.y); });
      svg.appendChild(lbl);
    });

    // понятия: рисуем все, но неоткрытые прячем классом hidden
    Object.keys(graph.nodes).forEach(function (name) {
      var n = graph.nodes[name];
      var g = px("g");
      g.setAttribute("class", n.firstOrder > cut ? "node hidden" : "node");

      var circle = px("circle");
      circle.setAttribute("class", "node-face");
      circle.setAttribute("r", 9);
      circle.setAttribute("cx", n.x); circle.setAttribute("cy", n.y);
      g.appendChild(circle);

      var t = px("text");
      t.setAttribute("class", "node-text");
      t.setAttribute("x", n.x + 12); t.setAttribute("y", n.y + 4);
      t.textContent = name;
      g.appendChild(t);

      var data = { relation: name, provenance: n.prov.join(" | "), flags: [] };
      g.addEventListener("mouseenter", function (ev) { showTooltip(ev, data); });
      g.addEventListener("mousemove", function (ev) { showTooltip(ev, data); });
      g.addEventListener("mouseleave", hideTooltip);
      g.addEventListener("click", function (e) {
        e.stopPropagation();
        if (n.places.length <= 1) jumpTo(n.places[0] ? n.places[0].y : n.firstY);
        else showPlacesPanel(n, graph);
      });
      svg.appendChild(g);
    });
  }

  // ---------- MAIN ----------
  var triples = parseTriples();
  if (!triples.length) { mapEl.parentNode.removeChild(mapEl); return; }
  var graph = buildGraph(triples);
  var svg = mapEl.querySelector("svg");

  function draw() {
    var W = svg.clientWidth || 460;
    var H = svg.clientHeight || 360;
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    layout(graph, W, H);
    // «открыто» = предложение уже достигло нижнего края вьюпорта.
    // y храним в координатах документа; нижний край = scrollY + innerHeight.
    var bottom = window.scrollY + window.innerHeight;
    var cut = 0;
    triples.forEach(function (t) { if (t.y <= bottom) cut = t.order; });
    render(graph, cut, svg, W, H);
  }

  var t = null;
  function th() { if (t) clearTimeout(t); t = setTimeout(draw, 80); }
  window.addEventListener("scroll", th, true);
  window.addEventListener("resize", function () { draw(); });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", draw);
  else draw();
})();
