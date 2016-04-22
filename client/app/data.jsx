export var myData = {
  path: [[1, 1], [200, 300]],
};

export const decisionTreeData = {
  heading: 'Start',
  yesNode: {
    heading: "Yes",
    yesNode: {
      heading: "Yes-Yes",
      yesNode: null,
      noNode: null
    },
    noNode: {
      heading: "Yes-No",
      yesNode: null,
      noNode: null
    }
  },
  noNode: {
    heading: "No",
    yesNode: {
      heading: "No-Yes",
      yesNode: null,
      noNode: null
    },
    noNode: {
      heading: "No-No",
      yesNode: {
        heading: "No-No-Yes",
        yesNode: null,
        noNode: null
      },
      noNode: null
    }
  }
};