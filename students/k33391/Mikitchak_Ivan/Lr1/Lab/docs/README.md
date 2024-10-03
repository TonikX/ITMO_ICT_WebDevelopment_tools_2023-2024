# Documentation for FastAPI

<a name="documentation-for-api-endpoints"></a>
## Documentation for API Endpoints

All URIs are relative to *http://localhost*

| Class | Method | HTTP request | Description |
|------------ | ------------- | ------------- | -------------|
| *DefaultApi* | [**createContestContestsPost**](Apis/DefaultApi.md#createcontestcontestspost) | **POST** /contests | Create Contest |
*DefaultApi* | [**createOrganizerContestsContestIdOrganizersPost**](Apis/DefaultApi.md#createorganizercontestscontestidorganizerspost) | **POST** /contests/{contest_id}/organizers | Create Organizer |
*DefaultApi* | [**createParticipantContestsContestIdParticipantsPost**](Apis/DefaultApi.md#createparticipantcontestscontestidparticipantspost) | **POST** /contests/{contest_id}/participants | Create Participant |
*DefaultApi* | [**createProblemContestsContestIdProblemsPost**](Apis/DefaultApi.md#createproblemcontestscontestidproblemspost) | **POST** /contests/{contest_id}/problems | Create Problem |
*DefaultApi* | [**createSubmissionContestsContestIdProblemsProblemIdSubmissionsPost**](Apis/DefaultApi.md#createsubmissioncontestscontestidproblemsproblemidsubmissionspost) | **POST** /contests/{contest_id}/problems/{problem_id}/submissions | Create Submission |
*DefaultApi* | [**createTeamContestsContestIdTeamsPost**](Apis/DefaultApi.md#createteamcontestscontestidteamspost) | **POST** /contests/{contest_id}/teams | Create Team |
*DefaultApi* | [**createTeamMemberContestsContestIdTeamsTeamIdMembersPost**](Apis/DefaultApi.md#createteammembercontestscontestidteamsteamidmemberspost) | **POST** /contests/{contest_id}/teams/{team_id}/members | Create Team Member |
*DefaultApi* | [**createUserUsersPost**](Apis/DefaultApi.md#createuseruserspost) | **POST** /users | Create User |
*DefaultApi* | [**deleteContestContestsContestIdDelete**](Apis/DefaultApi.md#deletecontestcontestscontestiddelete) | **DELETE** /contests/{contest_id} | Delete Contest |
*DefaultApi* | [**deleteMyOrganizerContestsContestIdOrganizersMeDelete**](Apis/DefaultApi.md#deletemyorganizercontestscontestidorganizersmedelete) | **DELETE** /contests/{contest_id}/organizers/me | Delete My Organizer |
*DefaultApi* | [**deleteMyParticipantContestsContestIdParticipantsMeDelete**](Apis/DefaultApi.md#deletemyparticipantcontestscontestidparticipantsmedelete) | **DELETE** /contests/{contest_id}/participants/me | Delete My Participant |
*DefaultApi* | [**deleteMyTeamContestsContestIdTeamsMyDelete**](Apis/DefaultApi.md#deletemyteamcontestscontestidteamsmydelete) | **DELETE** /contests/{contest_id}/teams/my | Delete My Team |
*DefaultApi* | [**deleteMyTeamMemberContestsContestIdTeamsMyMembersMemberIdDelete**](Apis/DefaultApi.md#deletemyteammembercontestscontestidteamsmymembersmemberiddelete) | **DELETE** /contests/{contest_id}/teams/my/members/{member_id} | Delete My Team Member |
*DefaultApi* | [**deleteMyUserUsersMeDelete**](Apis/DefaultApi.md#deletemyuserusersmedelete) | **DELETE** /users/me | Delete My User |
*DefaultApi* | [**deleteOrganizerContestsContestIdOrganizersOrganizerIdDelete**](Apis/DefaultApi.md#deleteorganizercontestscontestidorganizersorganizeriddelete) | **DELETE** /contests/{contest_id}/organizers/{organizer_id} | Delete Organizer |
*DefaultApi* | [**deleteParticipantContestsContestIdParticipantsParticipantIdDelete**](Apis/DefaultApi.md#deleteparticipantcontestscontestidparticipantsparticipantiddelete) | **DELETE** /contests/{contest_id}/participants/{participant_id} | Delete Participant |
*DefaultApi* | [**loginAuthLoginPost**](Apis/DefaultApi.md#loginauthloginpost) | **POST** /auth/login | Login |
*DefaultApi* | [**logoutAuthLogoutPost**](Apis/DefaultApi.md#logoutauthlogoutpost) | **POST** /auth/logout | Logout |
*DefaultApi* | [**readContestContestsContestIdGet**](Apis/DefaultApi.md#readcontestcontestscontestidget) | **GET** /contests/{contest_id} | Read Contest |
*DefaultApi* | [**readContestsContestsGet**](Apis/DefaultApi.md#readcontestscontestsget) | **GET** /contests | Read Contests |
*DefaultApi* | [**readMyOrganizerContestsContestIdOrganizersMeGet**](Apis/DefaultApi.md#readmyorganizercontestscontestidorganizersmeget) | **GET** /contests/{contest_id}/organizers/me | Read My Organizer |
*DefaultApi* | [**readMyParticipantContestsContestIdParticipantsMeGet**](Apis/DefaultApi.md#readmyparticipantcontestscontestidparticipantsmeget) | **GET** /contests/{contest_id}/participants/me | Read My Participant |
*DefaultApi* | [**readMyTeamContestsContestIdTeamsMyGet**](Apis/DefaultApi.md#readmyteamcontestscontestidteamsmyget) | **GET** /contests/{contest_id}/teams/my | Read My Team |
*DefaultApi* | [**readMyTeamMemberContestsContestIdTeamsMyMembersMemberIdGet**](Apis/DefaultApi.md#readmyteammembercontestscontestidteamsmymembersmemberidget) | **GET** /contests/{contest_id}/teams/my/members/{member_id} | Read My Team Member |
*DefaultApi* | [**readMyTeamMembersContestsContestIdTeamsMyMembersGet**](Apis/DefaultApi.md#readmyteammemberscontestscontestidteamsmymembersget) | **GET** /contests/{contest_id}/teams/my/members | Read My Team Members |
*DefaultApi* | [**readMyTeamMembersContestsContestIdTeamsMyMembersMeDelete**](Apis/DefaultApi.md#readmyteammemberscontestscontestidteamsmymembersmedelete) | **DELETE** /contests/{contest_id}/teams/my/members/me | Read My Team Members |
*DefaultApi* | [**readMyTeamMembersContestsContestIdTeamsMyMembersMeGet**](Apis/DefaultApi.md#readmyteammemberscontestscontestidteamsmymembersmeget) | **GET** /contests/{contest_id}/teams/my/members/me | Read My Team Members |
*DefaultApi* | [**readOrganizerContestsContestIdOrganizersOrganizerIdGet**](Apis/DefaultApi.md#readorganizercontestscontestidorganizersorganizeridget) | **GET** /contests/{contest_id}/organizers/{organizer_id} | Read Organizer |
*DefaultApi* | [**readOrganizersContestsContestIdOrganizersGet**](Apis/DefaultApi.md#readorganizerscontestscontestidorganizersget) | **GET** /contests/{contest_id}/organizers | Read Organizers |
*DefaultApi* | [**readParticipantContestsContestIdParticipantsParticipantIdGet**](Apis/DefaultApi.md#readparticipantcontestscontestidparticipantsparticipantidget) | **GET** /contests/{contest_id}/participants/{participant_id} | Read Participant |
*DefaultApi* | [**readParticipantsContestsContestIdParticipantsGet**](Apis/DefaultApi.md#readparticipantscontestscontestidparticipantsget) | **GET** /contests/{contest_id}/participants | Read Participants |
*DefaultApi* | [**readProblemContestsContestIdProblemsProblemIdGet**](Apis/DefaultApi.md#readproblemcontestscontestidproblemsproblemidget) | **GET** /contests/{contest_id}/problems/{problem_id} | Read Problem |
*DefaultApi* | [**readProblemsContestsContestIdProblemsGet**](Apis/DefaultApi.md#readproblemscontestscontestidproblemsget) | **GET** /contests/{contest_id}/problems | Read Problems |
*DefaultApi* | [**readSubmissionContestsContestIdProblemsProblemIdSubmissionsSubmissionIdGet**](Apis/DefaultApi.md#readsubmissioncontestscontestidproblemsproblemidsubmissionssubmissionidget) | **GET** /contests/{contest_id}/problems/{problem_id}/submissions/{submission_id} | Read Submission |
*DefaultApi* | [**readSubmissionsContestsContestIdProblemsProblemIdSubmissionsGet**](Apis/DefaultApi.md#readsubmissionscontestscontestidproblemsproblemidsubmissionsget) | **GET** /contests/{contest_id}/problems/{problem_id}/submissions | Read Submissions |
*DefaultApi* | [**readTeamMemberContestsContestIdTeamsTeamIdMembersGet**](Apis/DefaultApi.md#readteammembercontestscontestidteamsteamidmembersget) | **GET** /contests/{contest_id}/teams/{team_id}/members | Read Team Member |
*DefaultApi* | [**readTeamMemberContestsContestIdTeamsTeamIdMembersMemberIdGet**](Apis/DefaultApi.md#readteammembercontestscontestidteamsteamidmembersmemberidget) | **GET** /contests/{contest_id}/teams/{team_id}/members/{member_id} | Read Team Member |
*DefaultApi* | [**readTeamsContestsContestIdTeamsGet**](Apis/DefaultApi.md#readteamscontestscontestidteamsget) | **GET** /contests/{contest_id}/teams | Read Teams |
*DefaultApi* | [**readUserUsersUserIdGet**](Apis/DefaultApi.md#readuserusersuseridget) | **GET** /users/{user_id} | Read User |
*DefaultApi* | [**readUsersUsersGet**](Apis/DefaultApi.md#readusersusersget) | **GET** /users | Read Users |
*DefaultApi* | [**retrieveMyUserUsersMeGet**](Apis/DefaultApi.md#retrievemyuserusersmeget) | **GET** /users/me | Retrieve My User |
*DefaultApi* | [**retrieveTeamContestsContestIdTeamsTeamIdGet**](Apis/DefaultApi.md#retrieveteamcontestscontestidteamsteamidget) | **GET** /contests/{contest_id}/teams/{team_id} | Retrieve Team |
*DefaultApi* | [**scoreParticipantContestsContestIdParticipantsParticipantIdScorePost**](Apis/DefaultApi.md#scoreparticipantcontestscontestidparticipantsparticipantidscorepost) | **POST** /contests/{contest_id}/participants/{participant_id}/score | Score Participant |
*DefaultApi* | [**updateContestCodeContestsContestIdUpdateCodePost**](Apis/DefaultApi.md#updatecontestcodecontestscontestidupdatecodepost) | **POST** /contests/{contest_id}/update_code | Update Contest Code |
*DefaultApi* | [**updateContestContestsContestIdPut**](Apis/DefaultApi.md#updatecontestcontestscontestidput) | **PUT** /contests/{contest_id} | Update Contest |
*DefaultApi* | [**updateMyTeamCodeContestsContestIdTeamsMyUpdateCodePost**](Apis/DefaultApi.md#updatemyteamcodecontestscontestidteamsmyupdatecodepost) | **POST** /contests/{contest_id}/teams/my/update_code | Update My Team Code |
*DefaultApi* | [**updateMyTeamContestsContestIdTeamsMyPut**](Apis/DefaultApi.md#updatemyteamcontestscontestidteamsmyput) | **PUT** /contests/{contest_id}/teams/my | Update My Team |
*DefaultApi* | [**updateMyUserEmailUsersMeUpdateEmailPost**](Apis/DefaultApi.md#updatemyuseremailusersmeupdateemailpost) | **POST** /users/me/update_email | Update My User Email |
*DefaultApi* | [**updateMyUserPasswordUsersMeUpdatePasswordPost**](Apis/DefaultApi.md#updatemyuserpasswordusersmeupdatepasswordpost) | **POST** /users/me/update_password | Update My User Password |
*DefaultApi* | [**updateMyUserUsersMePut**](Apis/DefaultApi.md#updatemyuserusersmeput) | **PUT** /users/me | Update My User |
*DefaultApi* | [**updateProblemContestsContestIdProblemsProblemIdDelete**](Apis/DefaultApi.md#updateproblemcontestscontestidproblemsproblemiddelete) | **DELETE** /contests/{contest_id}/problems/{problem_id} | Update Problem |
*DefaultApi* | [**updateProblemContestsContestIdProblemsProblemIdPut**](Apis/DefaultApi.md#updateproblemcontestscontestidproblemsproblemidput) | **PUT** /contests/{contest_id}/problems/{problem_id} | Update Problem |


<a name="documentation-for-models"></a>
## Documentation for Models

 - [ContestCreateForm](./Models/ContestCreateForm.md)
 - [ContestSerialized](./Models/ContestSerialized.md)
 - [ContestSerializedAdmin](./Models/ContestSerializedAdmin.md)
 - [ContestUpdateForm](./Models/ContestUpdateForm.md)
 - [CreateProblemForm](./Models/CreateProblemForm.md)
 - [HTTPValidationError](./Models/HTTPValidationError.md)
 - [JoinAsOrganizerForm](./Models/JoinAsOrganizerForm.md)
 - [JoinTeamForm](./Models/JoinTeamForm.md)
 - [LoginForm](./Models/LoginForm.md)
 - [LoginResponse](./Models/LoginResponse.md)
 - [OrganizerRole](./Models/OrganizerRole.md)
 - [OrganizerSerialized](./Models/OrganizerSerialized.md)
 - [ParticipantSerialized](./Models/ParticipantSerialized.md)
 - [ProblemSerialized](./Models/ProblemSerialized.md)
 - [ProblemSerializedShort](./Models/ProblemSerializedShort.md)
 - [ScoreParticipantForm](./Models/ScoreParticipantForm.md)
 - [SubmissionForm](./Models/SubmissionForm.md)
 - [SubmissionSerialized](./Models/SubmissionSerialized.md)
 - [SubmissionSerializedMy](./Models/SubmissionSerializedMy.md)
 - [SubmissionSerializedMyShort](./Models/SubmissionSerializedMyShort.md)
 - [SubmissionSerializedShort](./Models/SubmissionSerializedShort.md)
 - [SubmissionSerializedTeam](./Models/SubmissionSerializedTeam.md)
 - [SubmissionSerializedTeamShort](./Models/SubmissionSerializedTeamShort.md)
 - [TeamForm](./Models/TeamForm.md)
 - [TeamMemberSerialized](./Models/TeamMemberSerialized.md)
 - [TeamRole](./Models/TeamRole.md)
 - [TeamSerialized](./Models/TeamSerialized.md)
 - [TeamSerializedOwner](./Models/TeamSerializedOwner.md)
 - [UpdateProblemForm](./Models/UpdateProblemForm.md)
 - [UserCreateForm](./Models/UserCreateForm.md)
 - [UserDeleteForm](./Models/UserDeleteForm.md)
 - [UserSerialized](./Models/UserSerialized.md)
 - [UserUpdateEmailForm](./Models/UserUpdateEmailForm.md)
 - [UserUpdateForm](./Models/UserUpdateForm.md)
 - [UserUpdatePasswordForm](./Models/UserUpdatePasswordForm.md)
 - [ValidationError](./Models/ValidationError.md)


<a name="documentation-for-authorization"></a>
## Documentation for Authorization

<a name="OAuth2PasswordBearer"></a>
### OAuth2PasswordBearer

- **Type**: OAuth
- **Flow**: password
- **Authorization URL**: 
- **Scopes**: N/A

