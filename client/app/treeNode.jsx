import React from 'react';

export default class TreeNode extends React.Component {
  render() {
    return(
      <svg x={this.props.x-50} y={this.props.y-10} height="20" width="100">
        <rect x="" y="0" width="100" height="20" fill="blue" />
        <text x="0" y="15" stroke="red">
          {this.props.text}
        </text>
      </svg>
    );
  }
}