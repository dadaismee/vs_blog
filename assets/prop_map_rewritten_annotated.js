const article = document.querySelector("article");
const map = document.getElementById("triple-map");
const W = document.getElementById('triple-map').clientWidth
const H = document.getElementById('triple-map').clientWidth

// vocabulary: relation normalization (mirrors cg)
const RELATION_SYNONYMS = {
	"is_a":"is_a","is a":"is_a","are":"is_a","is":"is_a",
	"is example": "is_example_of", "is_example_of":"is_example_of",
	"is_about":"is_about",
	"part_of":"part_of","part of":"part_of","component_of":"part_of",
	"has_attribute":"has_attribute","has":"has_attribute","has_property":"has_attribute",
	"requires":"requires","needs":"requires","depends_on":"requires",
	"cause_of":"cause_of","causes":"cause_of","leads_to":"cause_of","results_in":"cause_of",
	"enables":"enables","allows":"enables","makes_possible":"enables",
	"contrasts_with":"contrasts_with","contrasts":"contrasts_with","opposes":"contrasts_with",
	"analogous_to":"analogous_to","analogous":"analogous_to","similar_to":"analogous_to",
	"synthesizes":"synthesizes","combines":"synthesizes","integrates":"synthesizes","creates":"synthesizes",
	"references":"references","refers_to":"references","cites":"references",
	"asserts":"asserts","claims":"asserts","argues":"asserts","states":"asserts",
	"conflicts_with":"conflicts_with","conflicts":"conflicts_with",
	"maps_to":"represents","encode":"represents","encodes":"represents","embody":"represents",
	"embodies":"represents"
	// author's own additions go here, e.g.:
	// ,"is-an-a-priori-form-of": "is_a"
};

// → строим множество допустимых отношений
const getCanonicalRelationSet = (relationsObj) => new Set(Object.values(relationsObj))

// → чистим проверяемое отношение от пробелов и нормируем
const sanitizeRelation = (relation, relationsObj) => {
	const key = relation.toLowerCase().trim().replace(/\s+/g, "_");
	return relationsObj[key] || relation;
}

// → проверяем, что отношение каноничное
// [?] не уверен, можно ли просто вызвать внешнюю функцию внутри другой функции…
const isCanonical = (cleanRelation, relationsObj, canonicalSet) => canonicalSet.has(relationsObj[cleanRelation])

// console.log(isCanonical('argues ', RELATION_SYNONYMS, getCanonicalRelationSet(RELATION_SYNONYMS)))


// ---------- PART 1: PARSE ----------
// → находим родительский элемент, а в нем — нужные элементы с дата-атрибутами
const getSpansNodeList= (htmlContainer) => document.querySelector(htmlContainer).querySelectorAll('span[data-triple]')

// поскольку getSpansNodeList возвращает NodeList, чтобы достать значения, нужно превратить его в массив + потом оставить только слова и убрать пунктцацию, посольку дата-трипл пишем как "minimalism, is_a, technofetishism, CLAIM"

// V 1
// const parsedTriples = Array.from(parseTriples('article'), el => el.dataset.triple
// .replace(/\,/g,'')
// .split(' '))
// .map(([obj, rel, subj, type]) => ({obj, rel, subj, type}))

// Этого массива ↑ недостаточно: нужен объект, а чтобы его сделать нужно отдельно делать массив и отдельно доставать y-координаты. Поэтому нужно сделать ФУНКЦИЮ, а не переменную, где Array.from будет лишь частью:
// V2 — не сработало, так как деструктурирование выдает части массива как строки, из-за чего получается `{ obj: 'm', rel: 'i' … }`
// const getParsedTriples = (nodeList) => { 
// const triplesArray = Array.from(nodeList)
	// .map(el => el.dataset.triple.split(', '))
// return triplesArray.map(([obj, rel, subj, type]) => ({ obj, rel, subj, type }))
// }

// V3 — получилось грязно (не чистая функция + без деструктурирования), но зато работает — почищу позже — #todo
const getParsedTriples = (nodeList) => { 
const triplesArray = Array.from(nodeList)
	.map(el => ({ 
		triple: el.dataset.triple.split(', '), 
		provenance: el.textContent,
		yPos: el.getBoundingClientRect().top + window.scrollY }))
return triplesArray.map((triple, index) => {
	const relation = sanitizeRelation(triple.triple[1], RELATION_SYNONYMS)
	return { 
		obj: triple.triple[0], 
		rel: isCanonical(relation, RELATION_SYNONYMS, getCanonicalRelationSet(RELATION_SYNONYMS)) ? relation : null, 
		subj: triple.triple[2],
		type: triple.triple[3],
		provenance: triple.provenance,
		order: index + 1,
		yPos: triple.yPos
}})
}

// PART 2: граф
// Пока оставлю так и пойду дальше — нужно доделать places (yOrder, xOrder, yPos для каждого) + именование каждого link в links — #todo
// const buildGraphObj = (triplesArray) => {
// 	return triplesArray.reduce((acc, x) => {
// 		const keys = [x.subj, x.obj].forEach((key, idx) => {
// 			if (!acc.nodes.hasOwnProperty(key)) acc.nodes[key] = {
// 				name: key,
// 				yOrder: x.order,
// 				yPos: x.yPos,
// 				provenance: x.provenance,
// 				places: [],
// 				}
// 			if (!acc.links.includes(x.obj)) acc.links[x.obj] = {
// 				...x,
// 				isCanonical: isCanonical(x.rel, RELATION_SYNONYMS, getCanonicalRelationSet(RELATION_SYNONYMS)),
// 			}
// 		})
// 		return acc
// 	}, { nodes: {}, links: [] })
// }

	// V2 — спросил у ИИ, как сделать places и links. ответы простые: каждый place храним в переменной, проверяем else если понятие УЖЕ ЕСТЬ в массиве, links — просто проверяем, что связь subj-rel-obj уже существует в массиве
	const buildGraphObj = (triplesArray) => {
	return triplesArray.reduce((acc, x) => {
		[x.subj, x.obj].forEach((key) => {
			const place = {
				yPos: x.yPos, 
				xOrder: key == x.obj ? 1 : 2, 
				yOrder: x.order 
			}
			if (!acc.nodes[key]) {
				acc.nodes[key] = {
					name: key,
					provenance: x.provenance,
					places: [place]
				} 
			} else {
				acc.nodes[key].places.push(place)
			}
			// проверяем, что существует как минимум одна идентичная связь в массиве — если нет, push-им новую
			acc.links.some(link => link.subj === x.subj && link.obj === x.obj && link.rel === x.rel) 
				? null 
				: acc.links.push({
				...x,
				isCanonical: isCanonical(
					x.rel, 
					RELATION_SYNONYMS, 
					getCanonicalRelationSet(RELATION_SYNONYMS)),
			})
		})
		return acc
	}, { nodes: {}, links: [] })
}

// ---------- PART 3: LAYOUT (куда ставить) ----------

const buildLayout = (graph, width, height) => {
	const sortedEntries = Object.entries(graph.nodes).sort((a, b) => {
		if (a[1].yOrder === b[1].yOrder) return a[1].xOrder - b[1].xOrder
		return a[1].yOrder - b[1].yOrder
	})
	const yStep = Math.max(44, height / Math.max(1, sortedEntries.length))
	sortedEntries.map((entry, i) => {
		const point = entry[1]
		// const yStep = height / sortedEntries.length
		const yStep = width / 3
		point.x = yStep * (point.xOrder - 0.25)
		point.y = yStep / 2 * (point.yOrder - 0.25)
	})
	return { 
		width: width,
		height: height,
		nodes: sortedEntries,
		links: graph.links
	}
}


// ---------- PART 4: RENDER ----------
const renderToDOM = (layout, parentDomEl) => {
	// 1. create svg container + attach to DOM
	const createSVG = (el) => document.createElementNS("http://www.w3.org/2000/svg", el)
	const svgContainer = document.createElement('div')
	svgContainer.setAttribute('id', 'svgContainer')
	// svgContainer.style.border = "solid 1px black"
	const svg = createSVG('svg')
	const circleBaseSize = 9
	svg.id = 'svg'
	svg.setAttribute('viewBox', `0 0 ${layout.width} ${layout.height}`)
	svgContainer.appendChild(svg)
	// --- ↓ рисовать один граф на страницу (включить для дебаггинга)
	// if (!document.getElementById('svgContainer')) 
	// ---
	parentDomEl.appendChild(svgContainer)
	
	// draw lines 
	layout.links.forEach((link, idx) => {
		const sourceNode = layout.nodes.find(node => node[0] === link.obj)
		const targetNode = layout.nodes.find(node => node[0] === link.subj)
		
		const factor = targetNode[1].places.length * 5 // множитель для увеличения диаметра нодов
		const lineGroup = createSVG('g') // создаем группу для линии и подписи
		const line = createSVG('line')

		const x1 = sourceNode[1].x 
		const x2 = targetNode[1].x
		const y1 = sourceNode[1].y 
		const y2 = targetNode[1].y
		const dx = x2 - x1 
		const dy = y2 - y1
		const distance = Math.sqrt(dx * dx + dy * dy)
		const unitVectorX = dx / distance
		const unitVectorY = dy / distance
		const circleRadius = circleBaseSize + factor
		
		line.setAttribute("x1", x1) 
		line.setAttribute("y1", y1)
		line.setAttribute("x2", x2 - unitVectorX * circleRadius) 
		line.setAttribute("y2", y2 - unitVectorY * circleRadius) 

		line.style.stroke = '#94a3b8'
		line.setAttribute("marker-end", "url(#arrow)");
		line.style.strokeWidth = 1
		
		// draw rel labels 
		const relLable = createSVG('text')

		// tilt labels across lines
		const angle = 90 - Math.atan2(dx, dy) * 180 / Math.PI

		relLable.setAttribute('x', (x1 + x2) / 2)
		relLable.setAttribute('y', (y1 + y2) / 2 - 3)
		relLable.setAttribute('transform', `rotate(${angle} ${(x1+x2)/2} ${(y1+y2)/2})`)
		relLable.setAttribute('text-anchor', 'middle')
		relLable.style.fontSize = '8'
		relLable.style.fill = '#00f'
		relLable.style.fontFamily = 'monospace'
		relLable.textContent = link.rel
		lineGroup.appendChild(line)
		lineGroup.appendChild(relLable)

		// --- reveal
	  const revealY = link.yPos ?? y1
		lineGroup.style.visibility =
			window.scrollY + window.innerHeight >= revealY
				? 'visible'
				: 'hidden'
		// ---
		
		// document.querySelector('g').addEventListener('onmouseover', e => e.target.style.stroke = 'yellow')
		
		// window.scrollY <= link.yPos ? svg.appendChild(lineGroup) : null 
		// window.scrollY <= link.yPos ? lineGroup.style.visibility = 'hidden' : lineGroup.style.visibility = 'visible'
	})
	
	// draw nodes 
	layout.nodes.forEach(entry => {
		const point = entry[1]
		const factor = point.places.length * 5

		const node = createSVG('g')
		const circle = createSVG('circle')
		circle.setAttribute('cx', point.x)
		circle.setAttribute('cy', point.y)
		circle.setAttribute('r', circleBaseSize + factor)
		// circle.setAttribute('id', point.name)
		circle.setAttribute('fill', '#fff')
		circle.setAttribute('stroke', '#00f')
		circle.setAttribute('stroke-width', '0.5')
		circle.setAttribute('stroke-dasharray', '3 2')

		// const count = createSVG('text')
		// count.style.fontSize = `11 + ${point.places.length}`
		// count.style.fontWeight = '600'
		// count.setAttribute('x', point.x)
		// count.setAttribute('y', point.y)
		// count.textContent = point.places.length
		// count.style.fontFamily = 'monospace'
		
		const label = createSVG('text')
		label.setAttribute('x', point.x + (circleBaseSize/2 + factor) + 2)
		label.setAttribute('y', point.y - (circleBaseSize/2 + factor) - 2)
		label.textContent = point.name
		label.style.fontSize = '11'
		label.style.fontFamily = 'monospace'
		
		node.appendChild(circle)
		node.appendChild(label)
		svg.appendChild(node)
		// node.appendChild(count)

		// --- reveal
		const revealY = point.places[0].yPos ?? point.y
		node.style.visibility =
				window.scrollY + window.innerHeight >= revealY
					? 'visible'
					: 'hidden'
		// --- 

		window.scrollY <= point.places[0].yPos ? 
		window.scrollY <= point.places[0].yPos ? node.style.visibility = 'hidden' : node.style.visibility = 'visible'
	})
	
	const defs = createSVG("defs")
	const marker = createSVG("marker")
	marker.setAttribute("id", "arrow");
	marker.setAttribute("viewBox", "0 0 10 10");
	marker.setAttribute("refX", "9") 
	marker.setAttribute("refY", "5")
	marker.setAttribute("markerWidth", "7")
	marker.setAttribute("markerHeight", "7")
	marker.setAttribute("orient", "auto-start-reverse")
	const triPath = createSVG("path")
	triPath.setAttribute("d", "M0,0 L10,5 L0,10 z");
	triPath.style.stroke = 'black'
	marker.appendChild(triPath);
	defs.appendChild(marker);
	svg.appendChild(defs);
}

const triples = getParsedTriples(getSpansNodeList('article'))
const graphObj = buildGraphObj(triples)
const layout = buildLayout(graphObj, W, H)

renderToDOM(layout, map)

// window.addEventListener('scroll', renderToDOM(layout, map))


