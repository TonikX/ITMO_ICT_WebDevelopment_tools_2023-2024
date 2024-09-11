# DefaultApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createContestContestsPost**](DefaultApi.md#createContestContestsPost) | **POST** /contests | Create Contest |
| [**createOrganizerContestsContestIdOrganizersPost**](DefaultApi.md#createOrganizerContestsContestIdOrganizersPost) | **POST** /contests/{contest_id}/organizers | Create Organizer |
| [**createParticipantContestsContestIdParticipantsPost**](DefaultApi.md#createParticipantContestsContestIdParticipantsPost) | **POST** /contests/{contest_id}/participants | Create Participant |
| [**createProblemContestsContestIdProblemsPost**](DefaultApi.md#createProblemContestsContestIdProblemsPost) | **POST** /contests/{contest_id}/problems | Create Problem |
| [**createSubmissionContestsContestIdProblemsProblemIdSubmissionsPost**](DefaultApi.md#createSubmissionContestsContestIdProblemsProblemIdSubmissionsPost) | **POST** /contests/{contest_id}/problems/{problem_id}/submissions | Create Submission |
| [**createTeamContestsContestIdTeamsPost**](DefaultApi.md#createTeamContestsContestIdTeamsPost) | **POST** /contests/{contest_id}/teams | Create Team |
| [**createTeamMemberContestsContestIdTeamsTeamIdMembersPost**](DefaultApi.md#createTeamMemberContestsContestIdTeamsTeamIdMembersPost) | **POST** /contests/{contest_id}/teams/{team_id}/members | Create Team Member |
| [**createUserUsersPost**](DefaultApi.md#createUserUsersPost) | **POST** /users | Create User |
| [**deleteContestContestsContestIdDelete**](DefaultApi.md#deleteContestContestsContestIdDelete) | **DELETE** /contests/{contest_id} | Delete Contest |
| [**deleteMyOrganizerContestsContestIdOrganizersMeDelete**](DefaultApi.md#deleteMyOrganizerContestsContestIdOrganizersMeDelete) | **DELETE** /contests/{contest_id}/organizers/me | Delete My Organizer |
| [**deleteMyParticipantContestsContestIdParticipantsMeDelete**](DefaultApi.md#deleteMyParticipantContestsContestIdParticipantsMeDelete) | **DELETE** /contests/{contest_id}/participants/me | Delete My Participant |
| [**deleteMyTeamContestsContestIdTeamsMyDelete**](DefaultApi.md#deleteMyTeamContestsContestIdTeamsMyDelete) | **DELETE** /contests/{contest_id}/teams/my | Delete My Team |
| [**deleteMyTeamMemberContestsContestIdTeamsMyMembersMemberIdDelete**](DefaultApi.md#deleteMyTeamMemberContestsContestIdTeamsMyMembersMemberIdDelete) | **DELETE** /contests/{contest_id}/teams/my/members/{member_id} | Delete My Team Member |
| [**deleteMyUserUsersMeDelete**](DefaultApi.md#deleteMyUserUsersMeDelete) | **DELETE** /users/me | Delete My User |
| [**deleteOrganizerContestsContestIdOrganizersOrganizerIdDelete**](DefaultApi.md#deleteOrganizerContestsContestIdOrganizersOrganizerIdDelete) | **DELETE** /contests/{contest_id}/organizers/{organizer_id} | Delete Organizer |
| [**deleteParticipantContestsContestIdParticipantsParticipantIdDelete**](DefaultApi.md#deleteParticipantContestsContestIdParticipantsParticipantIdDelete) | **DELETE** /contests/{contest_id}/participants/{participant_id} | Delete Participant |
| [**loginAuthLoginPost**](DefaultApi.md#loginAuthLoginPost) | **POST** /auth/login | Login |
| [**logoutAuthLogoutPost**](DefaultApi.md#logoutAuthLogoutPost) | **POST** /auth/logout | Logout |
| [**readContestContestsContestIdGet**](DefaultApi.md#readContestContestsContestIdGet) | **GET** /contests/{contest_id} | Read Contest |
| [**readContestsContestsGet**](DefaultApi.md#readContestsContestsGet) | **GET** /contests | Read Contests |
| [**readMyOrganizerContestsContestIdOrganizersMeGet**](DefaultApi.md#readMyOrganizerContestsContestIdOrganizersMeGet) | **GET** /contests/{contest_id}/organizers/me | Read My Organizer |
| [**readMyParticipantContestsContestIdParticipantsMeGet**](DefaultApi.md#readMyParticipantContestsContestIdParticipantsMeGet) | **GET** /contests/{contest_id}/participants/me | Read My Participant |
| [**readMyTeamContestsContestIdTeamsMyGet**](DefaultApi.md#readMyTeamContestsContestIdTeamsMyGet) | **GET** /contests/{contest_id}/teams/my | Read My Team |
| [**readMyTeamMemberContestsContestIdTeamsMyMembersMemberIdGet**](DefaultApi.md#readMyTeamMemberContestsContestIdTeamsMyMembersMemberIdGet) | **GET** /contests/{contest_id}/teams/my/members/{member_id} | Read My Team Member |
| [**readMyTeamMembersContestsContestIdTeamsMyMembersGet**](DefaultApi.md#readMyTeamMembersContestsContestIdTeamsMyMembersGet) | **GET** /contests/{contest_id}/teams/my/members | Read My Team Members |
| [**readMyTeamMembersContestsContestIdTeamsMyMembersMeDelete**](DefaultApi.md#readMyTeamMembersContestsContestIdTeamsMyMembersMeDelete) | **DELETE** /contests/{contest_id}/teams/my/members/me | Read My Team Members |
| [**readMyTeamMembersContestsContestIdTeamsMyMembersMeGet**](DefaultApi.md#readMyTeamMembersContestsContestIdTeamsMyMembersMeGet) | **GET** /contests/{contest_id}/teams/my/members/me | Read My Team Members |
| [**readOrganizerContestsContestIdOrganizersOrganizerIdGet**](DefaultApi.md#readOrganizerContestsContestIdOrganizersOrganizerIdGet) | **GET** /contests/{contest_id}/organizers/{organizer_id} | Read Organizer |
| [**readOrganizersContestsContestIdOrganizersGet**](DefaultApi.md#readOrganizersContestsContestIdOrganizersGet) | **GET** /contests/{contest_id}/organizers | Read Organizers |
| [**readParticipantContestsContestIdParticipantsParticipantIdGet**](DefaultApi.md#readParticipantContestsContestIdParticipantsParticipantIdGet) | **GET** /contests/{contest_id}/participants/{participant_id} | Read Participant |
| [**readParticipantsContestsContestIdParticipantsGet**](DefaultApi.md#readParticipantsContestsContestIdParticipantsGet) | **GET** /contests/{contest_id}/participants | Read Participants |
| [**readProblemContestsContestIdProblemsProblemIdGet**](DefaultApi.md#readProblemContestsContestIdProblemsProblemIdGet) | **GET** /contests/{contest_id}/problems/{problem_id} | Read Problem |
| [**readProblemsContestsContestIdProblemsGet**](DefaultApi.md#readProblemsContestsContestIdProblemsGet) | **GET** /contests/{contest_id}/problems | Read Problems |
| [**readSubmissionContestsContestIdProblemsProblemIdSubmissionsSubmissionIdGet**](DefaultApi.md#readSubmissionContestsContestIdProblemsProblemIdSubmissionsSubmissionIdGet) | **GET** /contests/{contest_id}/problems/{problem_id}/submissions/{submission_id} | Read Submission |
| [**readSubmissionsContestsContestIdProblemsProblemIdSubmissionsGet**](DefaultApi.md#readSubmissionsContestsContestIdProblemsProblemIdSubmissionsGet) | **GET** /contests/{contest_id}/problems/{problem_id}/submissions | Read Submissions |
| [**readTeamMemberContestsContestIdTeamsTeamIdMembersGet**](DefaultApi.md#readTeamMemberContestsContestIdTeamsTeamIdMembersGet) | **GET** /contests/{contest_id}/teams/{team_id}/members | Read Team Member |
| [**readTeamMemberContestsContestIdTeamsTeamIdMembersMemberIdGet**](DefaultApi.md#readTeamMemberContestsContestIdTeamsTeamIdMembersMemberIdGet) | **GET** /contests/{contest_id}/teams/{team_id}/members/{member_id} | Read Team Member |
| [**readTeamsContestsContestIdTeamsGet**](DefaultApi.md#readTeamsContestsContestIdTeamsGet) | **GET** /contests/{contest_id}/teams | Read Teams |
| [**readUserUsersUserIdGet**](DefaultApi.md#readUserUsersUserIdGet) | **GET** /users/{user_id} | Read User |
| [**readUsersUsersGet**](DefaultApi.md#readUsersUsersGet) | **GET** /users | Read Users |
| [**retrieveMyUserUsersMeGet**](DefaultApi.md#retrieveMyUserUsersMeGet) | **GET** /users/me | Retrieve My User |
| [**retrieveTeamContestsContestIdTeamsTeamIdGet**](DefaultApi.md#retrieveTeamContestsContestIdTeamsTeamIdGet) | **GET** /contests/{contest_id}/teams/{team_id} | Retrieve Team |
| [**scoreParticipantContestsContestIdParticipantsParticipantIdScorePost**](DefaultApi.md#scoreParticipantContestsContestIdParticipantsParticipantIdScorePost) | **POST** /contests/{contest_id}/participants/{participant_id}/score | Score Participant |
| [**updateContestCodeContestsContestIdUpdateCodePost**](DefaultApi.md#updateContestCodeContestsContestIdUpdateCodePost) | **POST** /contests/{contest_id}/update_code | Update Contest Code |
| [**updateContestContestsContestIdPut**](DefaultApi.md#updateContestContestsContestIdPut) | **PUT** /contests/{contest_id} | Update Contest |
| [**updateMyTeamCodeContestsContestIdTeamsMyUpdateCodePost**](DefaultApi.md#updateMyTeamCodeContestsContestIdTeamsMyUpdateCodePost) | **POST** /contests/{contest_id}/teams/my/update_code | Update My Team Code |
| [**updateMyTeamContestsContestIdTeamsMyPut**](DefaultApi.md#updateMyTeamContestsContestIdTeamsMyPut) | **PUT** /contests/{contest_id}/teams/my | Update My Team |
| [**updateMyUserEmailUsersMeUpdateEmailPost**](DefaultApi.md#updateMyUserEmailUsersMeUpdateEmailPost) | **POST** /users/me/update_email | Update My User Email |
| [**updateMyUserPasswordUsersMeUpdatePasswordPost**](DefaultApi.md#updateMyUserPasswordUsersMeUpdatePasswordPost) | **POST** /users/me/update_password | Update My User Password |
| [**updateMyUserUsersMePut**](DefaultApi.md#updateMyUserUsersMePut) | **PUT** /users/me | Update My User |
| [**updateProblemContestsContestIdProblemsProblemIdDelete**](DefaultApi.md#updateProblemContestsContestIdProblemsProblemIdDelete) | **DELETE** /contests/{contest_id}/problems/{problem_id} | Update Problem |
| [**updateProblemContestsContestIdProblemsProblemIdPut**](DefaultApi.md#updateProblemContestsContestIdProblemsProblemIdPut) | **PUT** /contests/{contest_id}/problems/{problem_id} | Update Problem |


<a name="createContestContestsPost"></a>
# **createContestContestsPost**
> ContestSerializedAdmin createContestContestsPost(ContestCreateForm)

Create Contest

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **ContestCreateForm** | [**ContestCreateForm**](../Models/ContestCreateForm.md)|  | |

### Return type

[**ContestSerializedAdmin**](../Models/ContestSerializedAdmin.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="createOrganizerContestsContestIdOrganizersPost"></a>
# **createOrganizerContestsContestIdOrganizersPost**
> OrganizerSerialized createOrganizerContestsContestIdOrganizersPost(contest\_id, JoinAsOrganizerForm)

Create Organizer

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **JoinAsOrganizerForm** | [**JoinAsOrganizerForm**](../Models/JoinAsOrganizerForm.md)|  | |

### Return type

[**OrganizerSerialized**](../Models/OrganizerSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="createParticipantContestsContestIdParticipantsPost"></a>
# **createParticipantContestsContestIdParticipantsPost**
> ParticipantSerialized createParticipantContestsContestIdParticipantsPost(contest\_id)

Create Participant

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**ParticipantSerialized**](../Models/ParticipantSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="createProblemContestsContestIdProblemsPost"></a>
# **createProblemContestsContestIdProblemsPost**
> ProblemSerialized createProblemContestsContestIdProblemsPost(contest\_id, CreateProblemForm)

Create Problem

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **CreateProblemForm** | [**CreateProblemForm**](../Models/CreateProblemForm.md)|  | |

### Return type

[**ProblemSerialized**](../Models/ProblemSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="createSubmissionContestsContestIdProblemsProblemIdSubmissionsPost"></a>
# **createSubmissionContestsContestIdProblemsProblemIdSubmissionsPost**
> SubmissionSerializedMy createSubmissionContestsContestIdProblemsProblemIdSubmissionsPost(contest\_id, problem\_id, SubmissionForm)

Create Submission

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **problem\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **SubmissionForm** | [**SubmissionForm**](../Models/SubmissionForm.md)|  | |

### Return type

[**SubmissionSerializedMy**](../Models/SubmissionSerializedMy.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="createTeamContestsContestIdTeamsPost"></a>
# **createTeamContestsContestIdTeamsPost**
> TeamSerializedOwner createTeamContestsContestIdTeamsPost(contest\_id, TeamForm)

Create Team

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **TeamForm** | [**TeamForm**](../Models/TeamForm.md)|  | |

### Return type

[**TeamSerializedOwner**](../Models/TeamSerializedOwner.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="createTeamMemberContestsContestIdTeamsTeamIdMembersPost"></a>
# **createTeamMemberContestsContestIdTeamsTeamIdMembersPost**
> TeamMemberSerialized createTeamMemberContestsContestIdTeamsTeamIdMembersPost(contest\_id, team\_id, JoinTeamForm)

Create Team Member

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **team\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **JoinTeamForm** | [**JoinTeamForm**](../Models/JoinTeamForm.md)|  | |

### Return type

[**TeamMemberSerialized**](../Models/TeamMemberSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="createUserUsersPost"></a>
# **createUserUsersPost**
> UserSerialized createUserUsersPost(UserCreateForm)

Create User

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **UserCreateForm** | [**UserCreateForm**](../Models/UserCreateForm.md)|  | |

### Return type

[**UserSerialized**](../Models/UserSerialized.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="deleteContestContestsContestIdDelete"></a>
# **deleteContestContestsContestIdDelete**
> deleteContestContestsContestIdDelete(contest\_id)

Delete Contest

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

null (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="deleteMyOrganizerContestsContestIdOrganizersMeDelete"></a>
# **deleteMyOrganizerContestsContestIdOrganizersMeDelete**
> deleteMyOrganizerContestsContestIdOrganizersMeDelete(contest\_id)

Delete My Organizer

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

null (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="deleteMyParticipantContestsContestIdParticipantsMeDelete"></a>
# **deleteMyParticipantContestsContestIdParticipantsMeDelete**
> deleteMyParticipantContestsContestIdParticipantsMeDelete(contest\_id)

Delete My Participant

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

null (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="deleteMyTeamContestsContestIdTeamsMyDelete"></a>
# **deleteMyTeamContestsContestIdTeamsMyDelete**
> deleteMyTeamContestsContestIdTeamsMyDelete(contest\_id)

Delete My Team

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

null (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="deleteMyTeamMemberContestsContestIdTeamsMyMembersMemberIdDelete"></a>
# **deleteMyTeamMemberContestsContestIdTeamsMyMembersMemberIdDelete**
> deleteMyTeamMemberContestsContestIdTeamsMyMembersMemberIdDelete(contest\_id, member\_id)

Delete My Team Member

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **member\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

null (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="deleteMyUserUsersMeDelete"></a>
# **deleteMyUserUsersMeDelete**
> deleteMyUserUsersMeDelete(UserDeleteForm)

Delete My User

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **UserDeleteForm** | [**UserDeleteForm**](../Models/UserDeleteForm.md)|  | |

### Return type

null (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="deleteOrganizerContestsContestIdOrganizersOrganizerIdDelete"></a>
# **deleteOrganizerContestsContestIdOrganizersOrganizerIdDelete**
> deleteOrganizerContestsContestIdOrganizersOrganizerIdDelete(contest\_id, organizer\_id)

Delete Organizer

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **organizer\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

null (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="deleteParticipantContestsContestIdParticipantsParticipantIdDelete"></a>
# **deleteParticipantContestsContestIdParticipantsParticipantIdDelete**
> deleteParticipantContestsContestIdParticipantsParticipantIdDelete(contest\_id, participant\_id)

Delete Participant

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **participant\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

null (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="loginAuthLoginPost"></a>
# **loginAuthLoginPost**
> LoginResponse loginAuthLoginPost(LoginForm)

Login

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **LoginForm** | [**LoginForm**](../Models/LoginForm.md)|  | |

### Return type

[**LoginResponse**](../Models/LoginResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="logoutAuthLogoutPost"></a>
# **logoutAuthLogoutPost**
> oas_any_type_not_mapped logoutAuthLogoutPost()

Logout

### Parameters
This endpoint does not need any parameter.

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readContestContestsContestIdGet"></a>
# **readContestContestsContestIdGet**
> oas_any_type_not_mapped readContestContestsContestIdGet(contest\_id)

Read Contest

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readContestsContestsGet"></a>
# **readContestsContestsGet**
> oas_any_type_not_mapped readContestsContestsGet(keywords, offset, limit)

Read Contests

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **keywords** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to null] |
| **offset** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to 0] |
| **limit** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to 10] |

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readMyOrganizerContestsContestIdOrganizersMeGet"></a>
# **readMyOrganizerContestsContestIdOrganizersMeGet**
> OrganizerSerialized readMyOrganizerContestsContestIdOrganizersMeGet(contest\_id)

Read My Organizer

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**OrganizerSerialized**](../Models/OrganizerSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readMyParticipantContestsContestIdParticipantsMeGet"></a>
# **readMyParticipantContestsContestIdParticipantsMeGet**
> ParticipantSerialized readMyParticipantContestsContestIdParticipantsMeGet(contest\_id)

Read My Participant

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**ParticipantSerialized**](../Models/ParticipantSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readMyTeamContestsContestIdTeamsMyGet"></a>
# **readMyTeamContestsContestIdTeamsMyGet**
> oas_any_type_not_mapped readMyTeamContestsContestIdTeamsMyGet(contest\_id)

Read My Team

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readMyTeamMemberContestsContestIdTeamsMyMembersMemberIdGet"></a>
# **readMyTeamMemberContestsContestIdTeamsMyMembersMemberIdGet**
> TeamMemberSerialized readMyTeamMemberContestsContestIdTeamsMyMembersMemberIdGet(contest\_id, member\_id)

Read My Team Member

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **member\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**TeamMemberSerialized**](../Models/TeamMemberSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readMyTeamMembersContestsContestIdTeamsMyMembersGet"></a>
# **readMyTeamMembersContestsContestIdTeamsMyMembersGet**
> oas_any_type_not_mapped readMyTeamMembersContestsContestIdTeamsMyMembersGet(contest\_id)

Read My Team Members

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readMyTeamMembersContestsContestIdTeamsMyMembersMeDelete"></a>
# **readMyTeamMembersContestsContestIdTeamsMyMembersMeDelete**
> readMyTeamMembersContestsContestIdTeamsMyMembersMeDelete(contest\_id)

Read My Team Members

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

null (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readMyTeamMembersContestsContestIdTeamsMyMembersMeGet"></a>
# **readMyTeamMembersContestsContestIdTeamsMyMembersMeGet**
> TeamMemberSerialized readMyTeamMembersContestsContestIdTeamsMyMembersMeGet(contest\_id)

Read My Team Members

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**TeamMemberSerialized**](../Models/TeamMemberSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readOrganizerContestsContestIdOrganizersOrganizerIdGet"></a>
# **readOrganizerContestsContestIdOrganizersOrganizerIdGet**
> OrganizerSerialized readOrganizerContestsContestIdOrganizersOrganizerIdGet(contest\_id, organizer\_id)

Read Organizer

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **organizer\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**OrganizerSerialized**](../Models/OrganizerSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readOrganizersContestsContestIdOrganizersGet"></a>
# **readOrganizersContestsContestIdOrganizersGet**
> oas_any_type_not_mapped readOrganizersContestsContestIdOrganizersGet(contest\_id)

Read Organizers

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readParticipantContestsContestIdParticipantsParticipantIdGet"></a>
# **readParticipantContestsContestIdParticipantsParticipantIdGet**
> ParticipantSerialized readParticipantContestsContestIdParticipantsParticipantIdGet(contest\_id, participant\_id)

Read Participant

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **participant\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**ParticipantSerialized**](../Models/ParticipantSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readParticipantsContestsContestIdParticipantsGet"></a>
# **readParticipantsContestsContestIdParticipantsGet**
> oas_any_type_not_mapped readParticipantsContestsContestIdParticipantsGet(contest\_id, keywords, offset, limit)

Read Participants

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **keywords** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to null] |
| **offset** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to 0] |
| **limit** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to 10] |

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readProblemContestsContestIdProblemsProblemIdGet"></a>
# **readProblemContestsContestIdProblemsProblemIdGet**
> ProblemSerialized readProblemContestsContestIdProblemsProblemIdGet(contest\_id, problem\_id)

Read Problem

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **problem\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**ProblemSerialized**](../Models/ProblemSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readProblemsContestsContestIdProblemsGet"></a>
# **readProblemsContestsContestIdProblemsGet**
> oas_any_type_not_mapped readProblemsContestsContestIdProblemsGet(contest\_id)

Read Problems

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readSubmissionContestsContestIdProblemsProblemIdSubmissionsSubmissionIdGet"></a>
# **readSubmissionContestsContestIdProblemsProblemIdSubmissionsSubmissionIdGet**
> oas_any_type_not_mapped readSubmissionContestsContestIdProblemsProblemIdSubmissionsSubmissionIdGet(contest\_id, problem\_id, submission\_id)

Read Submission

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **problem\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **submission\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readSubmissionsContestsContestIdProblemsProblemIdSubmissionsGet"></a>
# **readSubmissionsContestsContestIdProblemsProblemIdSubmissionsGet**
> oas_any_type_not_mapped readSubmissionsContestsContestIdProblemsProblemIdSubmissionsGet(contest\_id, problem\_id, mode, author, content, offset, limit, date\_st, date\_end)

Read Submissions

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **problem\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **mode** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to all] [enum: all, my, team] |
| **author** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to null] |
| **content** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to null] |
| **offset** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to 0] |
| **limit** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to 10] |
| **date\_st** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to null] |
| **date\_end** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to null] |

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readTeamMemberContestsContestIdTeamsTeamIdMembersGet"></a>
# **readTeamMemberContestsContestIdTeamsTeamIdMembersGet**
> oas_any_type_not_mapped readTeamMemberContestsContestIdTeamsTeamIdMembersGet(contest\_id, team\_id)

Read Team Member

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **team\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readTeamMemberContestsContestIdTeamsTeamIdMembersMemberIdGet"></a>
# **readTeamMemberContestsContestIdTeamsTeamIdMembersMemberIdGet**
> TeamMemberSerialized readTeamMemberContestsContestIdTeamsTeamIdMembersMemberIdGet(contest\_id, team\_id, member\_id)

Read Team Member

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **team\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **member\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**TeamMemberSerialized**](../Models/TeamMemberSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readTeamsContestsContestIdTeamsGet"></a>
# **readTeamsContestsContestIdTeamsGet**
> oas_any_type_not_mapped readTeamsContestsContestIdTeamsGet(contest\_id, keywords, offset, limit)

Read Teams

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **keywords** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to null] |
| **offset** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to 0] |
| **limit** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to 10] |

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readUserUsersUserIdGet"></a>
# **readUserUsersUserIdGet**
> UserSerialized readUserUsersUserIdGet(user\_id)

Read User

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **user\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**UserSerialized**](../Models/UserSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="readUsersUsersGet"></a>
# **readUsersUsersGet**
> oas_any_type_not_mapped readUsersUsersGet(keywords, offset, limit)

Read Users

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **keywords** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to null] |
| **offset** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to 0] |
| **limit** | [**oas_any_type_not_mapped**](../Models/.md)|  | [optional] [default to 10] |

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="retrieveMyUserUsersMeGet"></a>
# **retrieveMyUserUsersMeGet**
> UserSerialized retrieveMyUserUsersMeGet()

Retrieve My User

### Parameters
This endpoint does not need any parameter.

### Return type

[**UserSerialized**](../Models/UserSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="retrieveTeamContestsContestIdTeamsTeamIdGet"></a>
# **retrieveTeamContestsContestIdTeamsTeamIdGet**
> TeamSerialized retrieveTeamContestsContestIdTeamsTeamIdGet(contest\_id, team\_id)

Retrieve Team

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **team\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**TeamSerialized**](../Models/TeamSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="scoreParticipantContestsContestIdParticipantsParticipantIdScorePost"></a>
# **scoreParticipantContestsContestIdParticipantsParticipantIdScorePost**
> ParticipantSerialized scoreParticipantContestsContestIdParticipantsParticipantIdScorePost(contest\_id, participant\_id, ScoreParticipantForm)

Score Participant

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **participant\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **ScoreParticipantForm** | [**ScoreParticipantForm**](../Models/ScoreParticipantForm.md)|  | |

### Return type

[**ParticipantSerialized**](../Models/ParticipantSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="updateContestCodeContestsContestIdUpdateCodePost"></a>
# **updateContestCodeContestsContestIdUpdateCodePost**
> ContestSerializedAdmin updateContestCodeContestsContestIdUpdateCodePost(contest\_id)

Update Contest Code

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**ContestSerializedAdmin**](../Models/ContestSerializedAdmin.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="updateContestContestsContestIdPut"></a>
# **updateContestContestsContestIdPut**
> oas_any_type_not_mapped updateContestContestsContestIdPut(contest\_id, ContestUpdateForm)

Update Contest

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **ContestUpdateForm** | [**ContestUpdateForm**](../Models/ContestUpdateForm.md)|  | |

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="updateMyTeamCodeContestsContestIdTeamsMyUpdateCodePost"></a>
# **updateMyTeamCodeContestsContestIdTeamsMyUpdateCodePost**
> TeamSerializedOwner updateMyTeamCodeContestsContestIdTeamsMyUpdateCodePost(contest\_id)

Update My Team Code

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

[**TeamSerializedOwner**](../Models/TeamSerializedOwner.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="updateMyTeamContestsContestIdTeamsMyPut"></a>
# **updateMyTeamContestsContestIdTeamsMyPut**
> TeamSerializedOwner updateMyTeamContestsContestIdTeamsMyPut(contest\_id, TeamForm)

Update My Team

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **TeamForm** | [**TeamForm**](../Models/TeamForm.md)|  | |

### Return type

[**TeamSerializedOwner**](../Models/TeamSerializedOwner.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="updateMyUserEmailUsersMeUpdateEmailPost"></a>
# **updateMyUserEmailUsersMeUpdateEmailPost**
> UserSerialized updateMyUserEmailUsersMeUpdateEmailPost(UserUpdateEmailForm)

Update My User Email

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **UserUpdateEmailForm** | [**UserUpdateEmailForm**](../Models/UserUpdateEmailForm.md)|  | |

### Return type

[**UserSerialized**](../Models/UserSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="updateMyUserPasswordUsersMeUpdatePasswordPost"></a>
# **updateMyUserPasswordUsersMeUpdatePasswordPost**
> UserSerialized updateMyUserPasswordUsersMeUpdatePasswordPost(UserUpdatePasswordForm)

Update My User Password

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **UserUpdatePasswordForm** | [**UserUpdatePasswordForm**](../Models/UserUpdatePasswordForm.md)|  | |

### Return type

[**UserSerialized**](../Models/UserSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="updateMyUserUsersMePut"></a>
# **updateMyUserUsersMePut**
> UserSerialized updateMyUserUsersMePut(UserUpdateForm)

Update My User

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **UserUpdateForm** | [**UserUpdateForm**](../Models/UserUpdateForm.md)|  | |

### Return type

[**UserSerialized**](../Models/UserSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="updateProblemContestsContestIdProblemsProblemIdDelete"></a>
# **updateProblemContestsContestIdProblemsProblemIdDelete**
> updateProblemContestsContestIdProblemsProblemIdDelete(contest\_id, problem\_id)

Update Problem

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **problem\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |

### Return type

null (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="updateProblemContestsContestIdProblemsProblemIdPut"></a>
# **updateProblemContestsContestIdProblemsProblemIdPut**
> ProblemSerialized updateProblemContestsContestIdProblemsProblemIdPut(contest\_id, problem\_id, UpdateProblemForm)

Update Problem

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **contest\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **problem\_id** | [**oas_any_type_not_mapped**](../Models/.md)|  | [default to null] |
| **UpdateProblemForm** | [**UpdateProblemForm**](../Models/UpdateProblemForm.md)|  | |

### Return type

[**ProblemSerialized**](../Models/ProblemSerialized.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

