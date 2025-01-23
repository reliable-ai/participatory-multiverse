---
toc: false
---

# Using Participatory Input to Navigate the Machine Learning Multiverse

<div class="grid grid-cols-2">

<div>

This document is an interactive companion article illustrating a subset of the results from the paper *"Preventing Harmful Data Practices by using Participatory Input to Navigate the Machine Learning Multiverse"*.

For a detailed explanation of the methodology, analysis and decision paths explored, please refer to the *Methods* and *Results* sections of the paper.

This interactive analysis allows for the exploration of the participatory multiverse for **individual countries**. You can select a country from the dropdown below to view its particular figure.

After selecting a country, you can click individual nodes in the analysis to see the actual path that leads to a node. The further to the right of the figure you select a node, the longer, thinner and more detailed a path will be. Hovering over a node will display a tooltip with the decision and choice that node represents.

To protect participant privacy, we only generate separate figures for countries with at least *N >= 5* participants after filtering. To reduce the complexity of the figures we only include data from participants with complete data for all decisions for this analysis. The full list of counts per country is available in Table&nbsp;1, as well as information on whether or not this country's data is visible in a separate plot or in aggregate.

</div>

<div>

*Table 1. Number of participants per country included in the figure below. To avoid further complexity, only data from participants with complete responses for all decisions were included for these figures.*

```js
const countryCounts = await FileAttachment("data/country_counts.csv").csv({typed: true})
```

```js
Inputs.table(
  countryCounts,
  {
    select: false,
    format: {
      separate_plot: d => d === "TRUE" ? "✅️" : "❌️"
    },
    maxHeight: 180
  })
```

</div>

</div>

<div class="grid grid-cols-4">

<div class="grid-colspan-3">

```js
const sankeyCSVs = {
  "Aotearoa New Zealand": FileAttachment("data/countries-sankey/sankey-ptcp-ctr--Aotearoa New Zealand.csv"),
  "Australia": FileAttachment("data/countries-sankey/sankey-ptcp-ctr--Australia.csv"),
  "Brazil": FileAttachment("data/countries-sankey/sankey-ptcp-ctr--Brazil.csv"),
  "Canada": FileAttachment("data/countries-sankey/sankey-ptcp-ctr--Canada.csv"),
  "Denmark": FileAttachment("data/countries-sankey/sankey-ptcp-ctr--Denmark.csv"),
  "France": FileAttachment("data/countries-sankey/sankey-ptcp-ctr--France.csv"),
  "Germany": FileAttachment("data/countries-sankey/sankey-ptcp-ctr--Germany.csv"),
  "Poland": FileAttachment("data/countries-sankey/sankey-ptcp-ctr--Poland.csv"),
  "Russia": FileAttachment("data/countries-sankey/sankey-ptcp-ctr--Russia.csv"),
  "South Korea": FileAttachment("data/countries-sankey/sankey-ptcp-ctr--South Korea.csv"),
  "Sweden": FileAttachment("data/countries-sankey/sankey-ptcp-ctr--Sweden.csv"),
  "United Kingdom": FileAttachment("data/countries-sankey/sankey-ptcp-ctr--United Kingdom.csv"),
  "United States": FileAttachment("data/countries-sankey/sankey-ptcp-ctr--United States.csv"),
  "Aggregated Countries": FileAttachment("data/countries-sankey/sankey-ptcp-ctr--Other.csv"),
}
```

```js
const countries = Object.keys(sankeyCSVs)
```

```js
const country = view(
  Inputs.select(
    countries,
    {value: "United States", label: "Country"}
  )
);
```

```js
import * as d3Sankey from 'd3-sankey'

// Copyright 2021-2023 Observable, Inc.
// Released under the ISC license.
// https://observablehq.com/@d3/sankey-diagram
function SankeyChart({
  nodes, // an iterable of node objects (typically [{id}, …]); implied by links if missing
  links // an iterable of link objects (typically [{source, target}, …])
}, {
  format = ",", // a function or format specifier for values in titles
  align = "justify", // convenience shorthand for nodeAlign
  nodeId = d => d.id, // given d in nodes, returns a unique identifier (string)
  nodeGroup, // given d in nodes, returns an (ordinal) value for color
  nodeGroups, // an array of ordinal values representing the node groups
  nodeLabel, // given d in (computed) nodes, text to label the associated rect
  nodeTitle = d => `${d.id}\n${format(d.value)}`, // given d in (computed) nodes, hover text
  nodeAlign = align, // Sankey node alignment strategy: left, right, justify, center
  nodeSort, // comparator function to order nodes
  nodeWidth = 15, // width of node rects
  nodePadding = 10, // vertical separation between adjacent nodes
  nodeLabelPadding = 6, // horizontal separation between node and label
  nodeStroke = "currentColor", // stroke around node rects
  nodeStrokeWidth, // width of stroke around node rects, in pixels
  nodeStrokeOpacity, // opacity of stroke around node rects
  nodeStrokeLinejoin, // line join for stroke around node rects
  linkSource = ({source}) => source, // given d in links, returns a node identifier string
  linkTarget = ({target}) => target, // given d in links, returns a node identifier string
  linkValue = ({value}) => value, // given d in links, returns the quantitative value
  linkPath = d3Sankey.sankeyLinkHorizontal(), // given d in (computed) links, returns the SVG path
  linkTitle = d => `${d.source.id} → ${d.target.id}\n${format(d.value)}`, // given d in (computed) links
  linkColor = "source-target", // source, target, source-target, or static color
  linkStrokeOpacity = 0.5, // link stroke opacity
  linkMixBlendMode = "multiply", // link blending mode
  colors = d3.schemeTableau10, // array of colors
  width = 640, // outer width, in pixels
  height = 400, // outer height, in pixels
  marginTop = 5, // top margin, in pixels
  marginRight = 1, // right margin, in pixels
  marginBottom = 5, // bottom margin, in pixels
  marginLeft = 1, // left margin, in pixels
  iterations = 6, // number of iterations (new addition)
  onNodeClick = (event, data) => {},
} = {}) {
  // Convert nodeAlign from a name to a function (since d3-sankey is not part of core d3).
  if (typeof nodeAlign !== "function") nodeAlign = {
    left: d3Sankey.sankeyLeft,
    right: d3Sankey.sankeyRight,
    center: d3Sankey.sankeyCenter
  }[nodeAlign] ?? d3Sankey.sankeyJustify;

  // Compute values.
  const LS = d3.map(links, linkSource).map(intern);
  const LT = d3.map(links, linkTarget).map(intern);
  const LV = d3.map(links, linkValue);
  if (nodes === undefined) nodes = Array.from(d3.union(LS, LT), id => ({id}));
  const N = d3.map(nodes, nodeId).map(intern);
  const G = nodeGroup == null ? null : d3.map(nodes, nodeGroup).map(intern);

  // Replace the input nodes and links with mutable objects for the simulation.
  nodes = d3.map(nodes, (_, i) => ({id: N[i]}));
  links = d3.map(links, (_, i) => ({source: LS[i], target: LT[i], value: LV[i]}));

  // Ignore a group-based linkColor option if no groups are specified.
  if (!G && ["source", "target", "source-target"].includes(linkColor)) linkColor = "currentColor";

  // Compute default domains.
  if (G && nodeGroups === undefined) nodeGroups = G;

  // Construct the scales.
  const color = nodeGroup == null ? null : d3.scaleOrdinal(nodeGroups, colors);

  // Compute the Sankey layout.
  d3Sankey.sankey()
      .nodeId(({index: i}) => N[i])
      .nodeAlign(nodeAlign)
      .nodeWidth(nodeWidth)
      .nodePadding(nodePadding)
      .nodeSort(nodeSort)
      .extent([[marginLeft, marginTop], [width - marginRight, height - marginBottom]])
      .iterations(iterations)
    ({nodes, links});

  // Compute titles and labels using layout nodes, so as to access aggregate values.
  if (typeof format !== "function") format = d3.format(format);
  const Tl = nodeLabel === undefined ? N : nodeLabel == null ? null : d3.map(nodes, nodeLabel);
  const Tt = nodeTitle == null ? null : d3.map(nodes, nodeTitle);
  const Lt = linkTitle == null ? null : d3.map(links, linkTitle);

  // A unique identifier for clip paths (to avoid conflicts).
  const uid = `O-${Math.random().toString(16).slice(2)}`;

  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  const node = svg.append("g")
      .attr("stroke", nodeStroke)
      .attr("stroke-width", nodeStrokeWidth)
      .attr("stroke-opacity", nodeStrokeOpacity)
      .attr("stroke-linejoin", nodeStrokeLinejoin)
    .selectAll("rect")
    .data(nodes)
    .join("rect")
      .attr("x", d => d.x0)
      .attr("y", d => d.y0)
      .attr("height", d => d.y1 - d.y0)
      .attr("width", d => d.x1 - d.x0);

  if (G) node.attr("fill", ({index: i}) => color(G[i]));
  if (Tt) node.append("title").text(({index: i}) => Tt[i]);

  const link = svg.append("g")
      .attr("fill", "none")
      .attr("stroke-opacity", linkStrokeOpacity)
    .selectAll("g")
    .data(links)
    .join("g")
      .style("mix-blend-mode", linkMixBlendMode);

  if (linkColor === "source-target") link.append("linearGradient")
      .attr("id", d => `${uid}-link-${d.index}`)
      .attr("gradientUnits", "userSpaceOnUse")
      .attr("x1", d => d.source.x1)
      .attr("x2", d => d.target.x0)
      .call(gradient => gradient.append("stop")
          .attr("offset", "0%")
          .attr("stop-color", ({source: {index: i}}) => color(G[i])))
      .call(gradient => gradient.append("stop")
          .attr("offset", "100%")
          .attr("stop-color", ({target: {index: i}}) => color(G[i])));

  link.append("path")
      .attr("d", linkPath)
      .attr("stroke", linkColor === "source-target" ? ({index: i}) => `url(#${uid}-link-${i})`
          : linkColor === "source" ? ({source: {index: i}}) => color(G[i])
          : linkColor === "target" ? ({target: {index: i}}) => color(G[i])
          : linkColor)
      .attr("stroke-width", ({width}) => Math.max(1, width))
      .call(Lt ? path => path.append("title").text(({index: i}) => Lt[i]) : () => {});

  if (Tl) {
    svg.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
    .selectAll("text")
    .data(nodes)
    .join("text")
      .attr("x", d => d.x0 < width / 2 ? d.x1 + nodeLabelPadding : d.x0 - nodeLabelPadding)
      .attr("y", d => (d.y1 + d.y0) / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", d => d.x0 < width / 2 ? "start" : "end")
      .text(({index: i}) => Tl[i]);

    if (onNodeClick) {
      svg.selectAll("rect").on("click", onNodeClick);
    }
  };

  function intern(value) {
    return value !== null && typeof value === "object" ? value.valueOf() : value;
  }

  return Object.assign(svg.node(), {scales: {color}});
}
```

```js
import { parseIndividualDecisionString } from './helpers.js'

const selectedData = Mutable(null)
const resetSelectedNode = () => {
  selectedData.value = null
}
const selectNode = nodeData => {
  const id = nodeData.id

  // Referencing country here to trigger a reset on country change
  country;

  // Parse ID into proper info
  const info = {}
  const split = id.split("->")
  if (split.length === 1) {
    resetSelectedNode()
    return
  }
  for (let i = 0; i < split.length; i++) {
    const { key, value } = parseIndividualDecisionString(split[i]);
    
    if (value) {
      info[key] = value;
    }
  }

  selectedData.value = info
}
```

```js
const nrows = ptcp_eval.length;
const effectiveWidth = width > 1080 ? width * 0.75 : width;
let effectiveHeight = effectiveWidth * 0.05 * Math.sqrt(nrows);
if (country === "Australia") {
  effectiveHeight = effectiveHeight * 1.25;
}
const chartEval = SankeyChart({
  links: ptcp_eval
}, {
  // take last word for color
  nodeGroup: d => {
    const split = d.id.split("->")
    const label = split[split.length - 1]

    if (label.includes("none_checked")) {
      return 4
    } else if (label.includes("understand") || label.includes("prefer") || label.includes("alternative")) {
      return 3
    } else if (label.includes("not_present")) {
      return 2
    } else {
      return 1
    }
  },
  nodeGroups: [1, 3, 4, 2],
  // take last word for label / title
  nodeTitle: d => {
    const split = d.id.split("->")
    const lastEntry = split[split.length - 1]
    const parsedEntry = parseIndividualDecisionString(lastEntry)
    if (parsedEntry.key === "START") {
      return "Start node\n(only for visualization)"
    } else {
      return parsedEntry.key + ':\n' + parsedEntry.value
    }
  },
  nodeLabel: d => {
    return ""
    // For debugging only:
    // const split = d.id.split("->")
    // return split[split.length - 1]
  },
  colors: [
    "#278B9A",
    "#D8AF39",
    "#E75B64",
    "#E8C4A2"
  ],
  nodeStroke: "transparent",
  nodeStrokeWidth: 0,
  linkStrokeOpacity: .75,
  linkMixBlendMode: "normal",
  nodeAlign: "justify", // e.g., d3.sankeyJustify; set by input above
  linkColor: "source-target", // e.g., "source" or "target"; set by input above
  // format: (f => d => `${f(d)} TWh`)(d3.format(",.1~f")),

  // Layouting relevant options
  nodePadding: nrows < 100 ? 15 : (nrows < 400 ? 10 : (nrows < 1500 ? 6 : 3)),
  iterations: 6,
  width: effectiveWidth,
  height: effectiveHeight,
  onNodeClick: (event, data) => {
    // Remove previous selection
    const selected = document.querySelector(".selected-node")
    if (selected) {
      selected.classList.remove("selected-node")
    }
    // Select new node
    event.target.classList.add("selected-node")

    selectNode(data)
    console.log(data)
  }
})
```

<style>
rect {
  cursor: pointer;
  stroke-width: 2px;
}
rect:hover {
  stroke: rgba(0,0,0,0.5);
}
.selected-node {
  stroke: #000;
}
</style>

```js
chartEval
```

</div>

<div class="info-container">
<div class="card">

## Node Information

This card will contain information about the path to the selected node within the participatory multiverse.

The further to the right of the multiverse you select a node, the more specific its path will be.

```js
let infoHtml = ``
let exclSubgroupsNotice = false;
if (selectedData !== null) {
  for (let [key, value] of Object.entries(selectedData)) {
    if (key === "Exclude Subgroups") {
      exclSubgroupsNotice = true;
      key = key + "<sup>✝</sup>"
    }
    infoHtml += `<li><b>${key}:</b> <code>${value}</code></li>`
  }
} else {
  infoHtml = `<li><i>No decision node selected, please select a decision node to see its path of decisions.</i></li>`
}

if (exclSubgroupsNotice) {
  infoHtml += `<p><sup>✝</sup>Despite the name, the different options in the decision <i>Exclude Subgroups</i> correspond to all subgroups that were chosen to be retained rather than excluded from the data.</p>`
}

const ul = html`<ul></ul>`
ul.innerHTML = infoHtml
```

```js
ul
```

<style>
@media (min-width: 1080px) {
  .info-container {
    display: flex;
    justify-content: center;
    align-items: center;
  }
}
ul {
  padding-left: 1em;
}
</style>

</div>
</div>

</div>

```js
// Only for debugging
// view(selectedData)
// nrows
```

```js
const ptcp_eval_raw = sankeyCSVs[country].csv({typed: true})
```

```js
const ptcp_eval = ptcp_eval_raw.map(row => { return { source: row.from, target: row.to, value: row.n}})
```
