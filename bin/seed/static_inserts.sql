-- SET search_path = volunteer, pg_catalog;

\set email '\'' '<The email you used to create the django account>' '\''
\set fname '\'' '<your first name>' '\''
\set lname '\'' '<your last name>' '\''
\set github_repo '\'' '<github test repo>' '\''

INSERT INTO team (focus, name, visibility, task_manager_id) VALUES ('Javascript/HTML', 'Team North Stars', 'Public', 1);
INSERT INTO team (focus, name, visibility, task_manager_id) VALUES ('PythonDjango', '2015 Summer Interns', 'Private', 1);

INSERT INTO schedule (name) VALUES ('NorthBridge Standard');

INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 1', '2015-01-11', '2015-02-07', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 2', '2015-02-01', '2015-02-28', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 3', '2015-02-22', '2015-03-21', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 4', '2015-03-15', '2015-04-11', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 5', '2015-04-05', '2015-05-02', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 6', '2015-04-26', '2015-05-23', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 7', '2015-05-17', '2015-06-13', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 8', '2015-06-07', '2015-07-04', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 9', '2015-06-28', '2015-07-25', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 10', '2015-07-19', '2015-08-15', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 11', '2015-08-09', '2015-09-05', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 12', '2015-08-30', '2015-09-26', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 13', '2015-09-20', '2015-10-17', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 14', '2015-10-11', '2015-11-07', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 15', '2015-11-01', '2015-11-28', 1);
INSERT INTO event (name, start_dttm, end_dttm, schedule_id_fk) VALUES ('Sprint 16', '2015-11-22', '2015-12-19', 1);

INSERT INTO campaign (name, description, amount_goal, respondent_goal) VALUES ('FriendsAndFamily', 'Friends And Family', 10000, 500);
INSERT INTO campaign (name, description, amount_goal, respondent_goal) VALUES ('Indiegogo', 'Indiegogo', 16000, 50);

-- alter table status add column descr character varying(20);
-- update status set descr = name;
-- update status set name = lower(name);
-- alter table status alter column descr set not null;
-- alter table status add constraint status_uk UNIQUE (category, name);

INSERT INTO status (category, name, descr) VALUES ('volunteer', 'inquired', 'Inquired');
INSERT INTO status (category, name, descr) VALUES ('volunteer', 'contacted', 'Contacted');
INSERT INTO status (category, name, descr) VALUES ('volunteer', 'oriented', 'Oriented');
INSERT INTO status (category, name, descr) VALUES ('volunteer', 'placed', 'Placed');
INSERT INTO status (category, name, descr) VALUES ('volunteer', 'trained', 'Trained');
INSERT INTO status (category, name, descr) VALUES ('backlog', 'open', 'Open');
INSERT INTO status (category, name, descr) VALUES ('backlog', 'selected', 'Selected');
INSERT INTO status (category, name, descr) VALUES ('backlog', 'queued', 'Queued');
INSERT INTO status (category, name, descr) VALUES ('backlog', 'accepted', 'Accepted');

INSERT INTO volunteer (email, fname, lname, create_dttm, descr, campaign_id_fk, status_id_fk) VALUES (:email, :fname, :lname, now(), '', 1, 5);

INSERT INTO application (name, description) VALUES ('Kumuku', 'Document cataloguing and publishing system to support grass roots human rights work in Africa');
INSERT INTO application (name, description) VALUES ('Nexus', 'Comprehensive framework to enable national collaboration among community service providers');
INSERT INTO application (name, description) VALUES ('Alliance-Android', 'NorthBridge development workspace-Android component');
INSERT INTO application (name, description) VALUES ('Alliance-Desktop', 'NorthBridge development workspace-Desktop component');
INSERT INTO application (name, description) VALUES ('Alliance-Core', 'NorthBridge development workspace-Service Core');

INSERT INTO project (name, descr, application_id_fk, end_event_fk, schedule_id_fk, start_event_fk) VALUES ('1.1', 'Release 1.0 enhancements and support', 1, 1, 1, 1);
INSERT INTO project (name, descr, application_id_fk, end_event_fk, schedule_id_fk, start_event_fk) VALUES ('1.0', 'Greenfield messaging portal', 2, 1, 1, 1);
INSERT INTO project (name, descr, application_id_fk, end_event_fk, schedule_id_fk, start_event_fk) VALUES ('1.0', 'Greenfield Android app.', 3, 1, 1, 1);
INSERT INTO project (name, descr, application_id_fk, end_event_fk, schedule_id_fk, start_event_fk) VALUES ('2.0', 'Build out the Resume features of Alliance Desktop', 4, 1, 1, 1);
INSERT INTO project (name, descr, application_id_fk, end_event_fk, schedule_id_fk, start_event_fk) VALUES ('1.1', 'Improve the existing features of Alliance Desktop', 4, 1, 1, 1);
INSERT INTO project (name, descr, application_id_fk, end_event_fk, schedule_id_fk, start_event_fk) VALUES ('Select a team, please.', '', 1, 1, 1, 1);
INSERT INTO project (name, descr, application_id_fk, end_event_fk, schedule_id_fk, start_event_fk) VALUES ('Pilot release', 'Controlled public engagement, 500+ community organizations across Illinois ', 2, 1, 1, 1);
INSERT INTO project (name, descr, application_id_fk, end_event_fk, schedule_id_fk, start_event_fk) VALUES ('1.0', 'Backlog/GitHub integration', 5, 1, 1, 1);

INSERT INTO backlog (story_title, story_descr, priority, module, skills, notes, github_number, github_repo, sprint_id_fk, status_id_fk, team_id_fk, create_dttm, update_dttm, project_id_fk) VALUES ('Bootstrap', 'Teach the system to start, stop and log messages', '1', 'Backlog', 'Python', 'Use python logging framework of your choice.', NULL, :github_repo, NULL, 6, 1, now(), NULL, 8);
INSERT INTO backlog (story_title, story_descr, priority, module, skills, notes, github_number, github_repo, sprint_id_fk, status_id_fk, team_id_fk, create_dttm, update_dttm, project_id_fk) VALUES ('DB Connect', 'Teach the system to connect to the database', '2', 'Backlog', 'Python, PostgreSQL', 'Kathy will provide connectivity details', NULL, :github_repo, NULL, 6, 1, now(), NULL, 8);
INSERT INTO backlog (story_title, story_descr, priority, module, skills, notes, github_number, github_repo, sprint_id_fk, status_id_fk, team_id_fk, create_dttm, update_dttm, project_id_fk) VALUES ('Backlog Read', 'Teach the system to locate Backlog items for export', '2', 'Backlog', 'Python, PostgreSQL', 'Kathy will provide table details', NULL, :github_repo, NULL, 6, 2, now(), NULL, 8);
INSERT INTO backlog (story_title, story_descr, priority, module, skills, notes, github_number, github_repo, sprint_id_fk, status_id_fk, team_id_fk, create_dttm, update_dttm, project_id_fk) VALUES ('GitHub Connect', 'Teach the system to connect to GitHub API', '1', 'Backlog', 'Python, GitHub API', 'Connection authentication, if needed, can probably be satisified with any user credentials.', NULL, :github_repo, NULL, 6, 2, now(), NULL, 8);

INSERT INTO acceptance_criteria (descr, title, backlog_id_fk) VALUES ('test description', 'test title', 4);
INSERT INTO acceptance_criteria (descr, title, backlog_id_fk) VALUES ('test descr', 'test title', 3);

INSERT INTO team_volunteer (team_id_fk, volunteer_id_fk, role, conference_link) VALUES (2, 1, 'Follower', '');
INSERT INTO team_project (team_id_fk, project_id_fk, start_event_fk, end_event_fk) VALUES (2, 8, 1, 16);

INSERT INTO auth_group (name) values ('Volunteers');
INSERT INTO auth_group_permissions (group_id, permission_id) SELECT 1, id FROM auth_permission WHERE codename IN ('change_backlog', 'add_acceptancecriteria', 'change_acceptancecriteria', 'delete_acceptancecriteria', 'add_estimate', 'change_estimate', 'delete_estimate');
