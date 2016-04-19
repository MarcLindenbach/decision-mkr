import React from 'react';
import {render} from 'react-dom';
import Greeting from './greeting.jsx';

class App extends React.Component {
  render () {
    return (
      <div>
        <p> Hello React!</p>
        <Greeting name="World" />
      </div>
    );
  }
}

render(<App/>, document.getElementById('app'));