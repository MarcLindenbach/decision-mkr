import React from 'react';
import {render} from 'react-dom';
import DecisionTree from './tree.jsx';

class App extends React.Component {
  render () {
    return (
      <div>
        <DecisionTree path={[[100, 100], [300, 100], [200, 300]]} />
      </div>
    );
  }
}

render(<App/>, document.getElementById('app'));