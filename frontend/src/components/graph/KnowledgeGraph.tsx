import * as d3 from "d3";
import { useEffect, useRef } from "react";
import type { GraphEdge, GraphNode } from "../../types";

interface KnowledgeGraphProps {
  nodes: GraphNode[];
  edges: GraphEdge[];
  onNodeClick: (nodeId: string) => void;
}

export function KnowledgeGraph({ nodes, edges, onNodeClick }: KnowledgeGraphProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;
    const width = 400;
    const height = 350;
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const simulation = d3
      .forceSimulation(nodes as d3.SimulationNodeDatum[])
      .force("link", d3.forceLink(edges as unknown as d3.SimulationLinkDatum<d3.SimulationNodeDatum>[]).id((d: any) => d.id).distance(120))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(40));

    const link = svg
      .append("g")
      .selectAll("line")
      .data(edges)
      .join("line")
      .attr("stroke", (d) => (d.active ? "var(--color-border)" : "var(--color-danger)"))
      .attr("stroke-dasharray", (d) => (d.active ? null : "4 4"))
      .attr("opacity", (d) => (d.active ? 1 : 0.4));

    const node = svg
      .append("g")
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", (d) => (d.tier === "hot" ? 12 : d.tier === "warm" ? 9 : 6))
      .attr("fill", (d) => `var(--color-${d.type.replace("_", "-")})`)
      .on("click", (_, d) => onNodeClick(d.id));

    simulation.on("tick", () => {
      link
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);
      node.attr("cx", (d: any) => d.x).attr("cy", (d: any) => d.y);
    });

    const zoom = d3.zoom<SVGSVGElement, unknown>().scaleExtent([0.3, 5]).on("zoom", (event) => {
      svg.selectAll("g").attr("transform", event.transform.toString());
    });
    svg.call(zoom);

    return () => {
      simulation.stop();
    };
  }, [nodes, edges, onNodeClick]);

  return <svg ref={svgRef} width={400} height={350} />;
}
