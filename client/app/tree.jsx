import React from 'react';

export default class DecisionTree extends React.Component {
  
  getPath() {
    return this.generate_path(this.props.path);
  }
  
  generate_path(path) {
    const [head, ...tail] = path
    let points = '';
    tail.forEach((point) => points += `L ${point[0]} ${point[1]} `);
    return `M ${head[0]} ${head[0]} ${points} z`;
  }
  
  render() {
    return (
      <svg width="50%" height="50%" viewBox="0 0 400 400">
        <path d={ this.getPath() }
            fill="orange" stroke="black" stroke-width="3">
        </path>
      </svg>
    );
  }
}