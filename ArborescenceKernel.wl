(* ::Package:: *)

(* Getting connection probability based on distance of two nodes (r) *)
GetProb[r_]:=(
	N[Exp[-Power[r,2]/2]]
);


(* Building maximum tree of spanning arborescence *)
StaticHierarchy[connProbabilityMx_]:=(
	sizeConProbMx = Length[connProbabilityMx[[1]]];
	connPowerMx = connProbabilityMx * Transpose[connProbabilityMx];
	For[i = 1, i <= sizeConProbMx, i++,
    connPowerMx[[1,i]] = Power[connProbabilityMx[[1,i]], 2]];
	tempMx = ConstantArray[1, {sizeConProbMx, sizeConProbMx}];
	For[i = 1, i <= sizeConProbMx, i++, {
		tempMx[[i,1]] = \[Infinity],
		tempMx[[i,i]] = \[Infinity]}];
	tempMx = tempMx - connPowerMx;
	fullSystemGraph = WeightedAdjacencyGraph[tempMx, DirectedEdges -> True,
    EdgeLabels -> "EdgeWeight", VertexLabels -> "Name"];
	spanningTreeMx = WeightedAdjacencyMatrix[
    FindSpanningTree[fullSystemGraph, VertexLabels -> "Name",
      EdgeLabels -> "EdgeWeight"]];
	result = spanningTreeMx
);


(* Test func *)
GetArg[x_]:=(
	x
);
