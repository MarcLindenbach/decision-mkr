import React from 'react';
import {render} from 'react-dom';
import DecisionTree from './decisionTree.jsx';
import {decisionTreeData} from './data.jsx';

class App extends React.Component {
  render () {
    return (
      <div>
        <DecisionTree tree={decisionTreeData} />
      </div>
    );
  }
}

render(<App/>, document.getElementById('app'));