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
  
  flattenedDecisionTree() {
    let tree = this.props.tree;
    
    let flattenTree = (node, level=0) => {
      let data = [{'id':node.id, 'text':node.text, 'level':level}];
      if (node.yes_node)
        data = data.concat(flattenTree(node.yes_node, level + 1));
      if (node.no_node)
        data = data.concat(flattenTree(node.no_node, level + 1));
      return data;
    };
    
    return flattenTree(tree);
  }
  
  getDecisionNodes() {
    let nodes = this.flattenedDecisionTree();
    let levels = nodes.map((node) => node.level);
    let highestLevel = Math.max(...levels);
    let nodesPerLevel = this.getNodesPerLevel(levels)
    
    let lineHeight = (this.viewBoxHeight / (highestLevel + 1));
    let lineWidth = (level) => (this.viewBoxWidth / nodesPerLevel[level]);
    
    let nodesAddedToLine = {};
    return nodes.map((node) => {
      let level = node.level;
      nodesAddedToLine[level] = nodesAddedToLine[level] ? nodesAddedToLine[level] + 1 : 1;
      
      node.y = (lineHeight * node.level) + (lineHeight / 2);
      node.x = (lineWidth(level) * (nodesAddedToLine[level] - 1)) + (lineWidth(level) / 2)
      
      return node;
    });
  }
  
  getNodesPerLevel(levels) {
    let counts = {};
      for (let i=0; i<levels.length; i++) {
        var num = levels[i];
        counts[num] = counts[num] ? counts[num] + 1 : 1;
      }
      return counts;
  }
  
  render() {
    return (
      <svg width="100%" height="100%" viewBox={this.getViewBoxBounds()}>
        {this.getDecisionNodes().map((node) => {
          return (
            //<circle cx={node.x} cy ={node.y} r="10">
            <text x={node.x} y={node.y} stroke="red">{node.text}</text>
            //</circle>
          );
        })}
      </svg>
    );
  }
}