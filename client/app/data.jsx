export const decisionTreeData = {
  id: 1,
  text: 'Start',
  yes_node: {
    id: 2,
    text: "Yes",
    yes_node: {
      id: 3,
      text: "Yes-Yes",
      yes_node: null,
      no_node: null
    },
    no_node: {
      id: 4,
      text: "Yes-No",
      yes_node: null,
      no_node: null
    }
  },
  no_node: {
    id: 5,
    text: "No",
    yes_node: {
      text: "No-Yes",
      yes_node: null,
      no_node: null
    },
    no_node: {
      id: 6,
      text: "No-No",
      yes_node: {
        id: 7,
        text: "No-No-Yes",
        yes_node: null,
        no_node: null
      },
      no_node: null
    }
  }
};