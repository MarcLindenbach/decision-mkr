import React from 'react';
import {render} from 'react-dom';
import DecisionTree from './tree.jsx';
import {myData, decisionTreeData} from './data.jsx';

let treeHeight = getDecisionTreeHeight(decisionTreeData);
let nodesPerLevel = getNodesPerLevel(getNodeLevels(decisionTreeData));
console.log(nodesPerLevel);

class App extends React.Component {
  render () {
    return (
      <div>
        <DecisionTree treeHeight="5" />
      </div>
    );
  }
}

render(<App/>, document.getElementById('app'));

function getNodesPerLevel(nodeLevels) {
  let counts = []
  for (var i; i < nodeLevels.length; i++) {
    counts[nodeLevels[i]] = 1 + (counts[nodeLevels[i]] || 0);
  }
  return counts[2];
}

function getNodeLevels(tree, nodeLevel=1) {
  let decisionTreeData = [nodeLevel];
  
  nodeLevel += 1;
  
  if (tree.yesNode !== null) {
    decisionTreeData = decisionTreeData.concat(getNodeLevels(tree.yesNode, nodeLevel))
  }
  
  if (tree.noNode !== null) {
    decisionTreeData = decisionTreeData.concat(getNodeLevels(tree.noNode, nodeLevel))
  }
  
  return decisionTreeData;
}

function getDecisionTreeHeight(tree, treeHeight=0) {
  treeHeight += 1;
  let yesHeight = treeHeight;
  let noHeight = treeHeight;
  
  if (tree.yesNode !== null) {
    yesHeight = getDecisionTreeHeight(tree.yesNode, yesHeight)
  }
  
  if (tree.noNode !== null) {
    noHeight = getDecisionTreeHeight(tree.noNode, noHeight)
  }
  
  if (yesHeight > noHeight) {
    return yesHeight;
  } else {
    return noHeight;
  }
}