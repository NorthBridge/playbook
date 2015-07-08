This project wiki describes Northbridge agile team processes.

This project code is responsible for the interactions between Northbridge agile team processes and GitHub issues tracking.

There are three major components to this project, export, import, and web interface. The first two are represented as the yellow portions of this diagram.

User Interface: Allows Northbridge volunteers to estimate and select backlog items for work.

Export: When invoked, export all Backlog User Stories in state "Selected" from the database to a GitHub Issues list using the GitHub API.

Import: When invoked, update a Backlog User Story to Accepted. This process will respond to a GitHub Issues Webhook.

![Project Diagram](http://northbridgetech.org/images/alliance1.jpg)
