# GitHub Projects (Projects v2) API – Practical Guide

## 1. Overview

When using the GitHub Projects (v2) GraphQL API, always remember:

- "Fields" (like Status, Priority, Size) and their "options" do not use plain
  English values.
- You must use the project’s internal IDs (field and option IDs) when building
  your queries/mutations.
- IDs might change if fields are edited—learn how to look them up!

## 2. Common Useful IDs in "GirlInRealLife App" Project

### Single-Select Fields and Option IDs

**Status** (Field ID: `PVTSSF_lADODTPBw84A-5t3zgyKmgo`)

- Todo: `f75ad846`
- In Progress: `47fc9ee4`
- Done: `98236657`

**Priority** (Field ID: `PVTSSF_lADODTPBw84A-5t3zgyKmlQ`)

- P0: `395be96e`
- P1: `920d5468`
- P2: `83b9d367`

**Size** (Field ID: `PVTSSF_lADODTPBw84A-5t3zgyKmlU`)

- XS: `09daeac5`
- S: `e5b731df`
- M: `6029ef79`
- L: `62f1d7ad`
- XL: `dfd3a2df`

(Other fields like Assignees, Labels, Milestone, Repository, etc., also use
IDs—fetch using similar queries as below.)

## 3. Queries to Discover Project, Field, or Option IDs

### a. Find Your Organization’s Projects

```graphql
query {
  organization(login: "GirlInRealLife") {
    projectsV2(first: 20) {
      nodes {
        id
        title
        shortDescription
      }
    }
  }
}
```

### b. Find Fields and Options for a Project

Replace `PROJECT_ID` with the real Project ID.

```graphql
query {
  node(id: "PROJECT_ID") {
    ... on ProjectV2 {
      fields(first: 30) {
        nodes {
          __typename
          ... on ProjectV2FieldCommon {
            id
            name
            dataType
          }
          ... on ProjectV2SingleSelectField {
            id
            name
            options {
              id
              name
            }
          }
        }
      }
    }
  }
}
```

## 4. Common Project Operations

### a. Create a New Project

```graphql
mutation {
  createProjectV2(input: {
    ownerId: "ORG_ID", # Find org ID with a separate query for your org
    title: "New_Project_Name"
  }) {
    projectV2 {
      id
      title
    }
  }
}
```

### b. Find Existing Items/Issues in a Project

```graphql
query {
  node(id: "PROJECT_ID") {
    ... on ProjectV2 {
      items(first: 50) {
        nodes {
          id
          content {
            ... on Issue {
              id
              title
              state
            }
          }
        }
      }
    }
  }
}
```

## 5. Issue/Item Operations

### a. Add an Issue to a Project

Assuming you already know the issueId and projectId:

```graphql
mutation {
  addProjectV2ItemById(input: {
    projectId: "PROJECT_ID"
    contentId: "ISSUE_NODE_ID"
  }) {
    item {
      id
    }
  }
}
```

### b. Update Project Item Fields (Set Status, Priority, Size, etc.)

```graphql
mutation {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: "PROJECT_ID"
      itemId: "ITEM_ID"
      fieldId: "PVTSSF_lADODTPBw84A-5t3zgyKmlQ" # Priority field
      value: { singleSelectOptionId: "920d5468" } # For P1
    }
  ) {
    projectV2Item {
      id
    }
  }
}
```

Repeat for other fields using their relevant IDs and option IDs as needed.

### c. Create a New Issue (and add to a project)

First, create the issue:

```graphql
mutation {
  createIssue(input: {
    repositoryId: "REPO_ID"
    title: "Describe the issue here"
    body: "Issue details here"
  }) {
    issue {
      id
      number
      title
    }
  }
}
```

Follow up by adding the new issue to your project as above.

## 6. Finding IDs for Other Elements

- **Organization ID:**

```graphql
query {
  organization(login: "GirlInRealLife") {
    id
  }
}
```

- **Repository ID:**

```graphql
query {
  repository(owner: "GirlInRealLife", name: "YOUR_REPO_NAME") {
    id
  }
}
```

## 7. Tips

- Never hardcode option IDs long-term; always check they’re up-to-date before
  scripting/automation.
- If a field or option disappears or IDs change, re-list fields/options as shown
  in Section 3.
