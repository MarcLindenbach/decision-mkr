import React from 'react';
import {render} from 'react-dom';
import DecisionTree from './tree.jsx';
import {myData, decisionTreeData} from './data.jsx';

let treeHeight = getDecisionTreeHeight(decisionTreeData);

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