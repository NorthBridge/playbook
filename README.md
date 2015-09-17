# The Problem 

GitHub provides lots of essential things that are needed in order to collaborate productively in an open-source, decentralized way: self managed user accounts, teams, messaging, task management, and even simple burndown charting. There is one component that Northbridge Technology Alliance needs in order to make GitHub hit the sweet spot of our agile development methodology, and that is backlog management.

This project provides a web-based backlog that Northbridge uses to prioritize all of our volunteer work across several projects. When a team selects a user story to accomplish, a button push exports the story into GitHub as a milestone and the associated acceptance criteria as tasks associated to that milestone.

Upon completion of the milestone, a GitHub API web hook is used to signal that the story is complete, and our backlog is udated accordingly.

We have researched lots of task management tools, and there are some very nice ones available. However they generally required the construction of a rather siloed user base. Northbridge wants to leverage the user infrastructure of GitHub, and all the other GitHub goodness. So this project give us the backlog we need in order to do that seamlessly.

# Overview

This repository wiki describes Northbridge agile team processes.

This repository code supports the Alliance project, which is responsible
for the interactions between Northbridge agile team processes and GitHub
issues tracking.

There are three major components to Alliance: **web interface**,
**export**, and **import**. These are represented as the yellow
components of this diagram.

- **Web Interface**: Allows Northbridge volunteers to estimate and
  select user stories from a prioritized backlog of work.

- **Export**: When invoked, export all Backlog User Stories in state
  "Selected" from the database to a GitHub Issues list using the GitHub
API.

- **Import**: When invoked, update a Backlog User Story to Accepted.
  This process will respond to a GitHub Issues Webhook.

![Project Diagram](http://northbridgetech.org/images/alliance2.jpg)

# Installing

Curious about contributing? Check out our [Installation Guide]().
