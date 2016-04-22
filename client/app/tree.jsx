import React from 'react';

export default class DecisionTree extends React.Component {
  
  constructor() {
    super();
    this.viewBoxWidth = 600;
    this.viewBoxHeight = 300;
    this.viewBoxMargin = 10;
  }
  
  getViewBoxBounds() {
    return `0 0 ${this.viewBoxWidth} ${this.viewBoxHeight}`;
  }
  
  getDecisionTreeNodes() {
    let nodes = [];
    let totalHeight = this.props.treeHeight
    for (let line = 1; line <= totalHeight; line++) {
      let lineHeight = (this.viewBoxHeight / totalHeight);
      let nodesOnLine = this.getNodesPerLine(line);
      for (let node = 1; node <= nodesOnLine; node++){
        let nodeWidth = (this.viewBoxWidth / nodesOnLine);
        nodes.push({
          y: (lineHeight * (line - 1)) + (lineHeight / 2),
          x: (nodeWidth * (node - 1)) + (nodeWidth / 2)
        });
      }
    }
    
    return nodes;
  }
  
  getNodesPerLine(line) {
    return Math.pow(2, line-1);
  }
  
  generatePath(pathPoints) {
    const [head, ...tail] = pathPoints;
    let points = '';
    tail.forEach((point) => points += `L ${point[0]} ${point[1]} `);
    return `M ${head[0]} ${head[0]} ${points}`;
  }
  
  
  
  render() {
    return (
      <svg width="100%" height="100%" viewBox={this.getViewBoxBounds()}>
        {this.getDecisionTreeNodes().map((node) => {
          return <circle cx={node.x} cy ={node.y} r="10"/>;
        })}
      </svg>
    );
  }
}