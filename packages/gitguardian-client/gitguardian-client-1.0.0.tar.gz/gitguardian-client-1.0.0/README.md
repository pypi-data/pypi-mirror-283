# Gitguardian Python SDK 1.0.0

Welcome to the Gitguardian SDK documentation. This guide will help you get started with integrating and using the Gitguardian SDK in your project.

## Versions

- API version: `1.1.0`
- SDK version: `1.0.0`

## About the API

Whether you want to build a complete integration with your software development workflow or simply want to test GitGuardian's policy break detection on any text content, you can use our API. - The base url for the latest version is `api.gitguardian.com/v1` over `HTTPS`. - All data is sent and received as JSON by default. - All timestamps returned are ISO-8601 compliant, example: `python 2020-03-16T04:46:00+00:00 # for date-time ` GitGuardian supported wrappers: - Python: [**py-gitguardian**](https://github.com/GitGuardian/py-gitguardian) GitGuardian provides you with [**GitGuardian Shield**](https://github.com/GitGuardian/gg-shield), a CLI application that uses the GitGuardian API through py-gitguardian to scan your files and detect potential secrets or issues in your code. This CLI application can be used in many CIs (such as GitHub Actions, GitLab Pipelines, CircleCI,...) or as a pre-commit or pre-receive hook. # Authentication The GitGuardian API uses API keys to authenticate requests. For a detailed explanation, please refer to our dedicated [documentation](https://docs.gitguardian.com/api-docs/authentication). Use [/v1/health](#operation/health_check) to check the validity of your token if needed. # Pagination The GitGuardian API employs cursor-based pagination. For a detailed explanation, please refer to our dedicated [documentation](https://docs.gitguardian.com/api-docs/pagination).

## Table of Contents

- [Setup & Configuration](#setup--configuration)
  - [Supported Language Versions](#supported-language-versions)
  - [Installation](#installation)
- [Authentication](#authentication)
  - [Access Token Authentication](#access-token-authentication)
- [Services](#services)
- [Models](#models)
- [License](#license)

## Setup & Configuration

### Supported Language Versions

This SDK is compatible with the following versions: `Python >= 3.7`

### Installation

To get started with the SDK, we recommend installing using `pip`:

```bash
pip install gitguardian-client
```

## Authentication

### Access Token Authentication

The Gitguardian API uses an Access Token for authentication.

This token must be provided to authenticate your requests to the API.

#### Setting the Access Token

When you initialize the SDK, you can set the access token as follows:

```py
Gitguardian(
    access_token="YOUR_ACCESS_TOKEN"
)
```

If you need to set or update the access token after initializing the SDK, you can use:

```py
sdk.set_access_token("YOUR_ACCESS_TOKEN")
```

## Services

The SDK provides various services to interact with the API.

<details> 
<summary>Below is a list of all available services with links to their detailed documentation:</summary>

| Name                                                                               |
| :--------------------------------------------------------------------------------- |
| [ApiTokensService](documentation/services/ApiTokensService.md)                     |
| [SecretIncidentsService](documentation/services/SecretIncidentsService.md)         |
| [SecretIncidentNotesService](documentation/services/SecretIncidentNotesService.md) |
| [SecretOccurrencesService](documentation/services/SecretOccurrencesService.md)     |
| [InvitationsService](documentation/services/InvitationsService.md)                 |
| [MembersService](documentation/services/MembersService.md)                         |
| [ScanMethodsService](documentation/services/ScanMethodsService.md)                 |
| [SecretDetectorsService](documentation/services/SecretDetectorsService.md)         |
| [QuotaService](documentation/services/QuotaService.md)                             |
| [IaCScanMethodsService](documentation/services/IaCScanMethodsService.md)           |
| [SourcesService](documentation/services/SourcesService.md)                         |
| [AuditLogsService](documentation/services/AuditLogsService.md)                     |
| [StatusService](documentation/services/StatusService.md)                           |
| [TeamsService](documentation/services/TeamsService.md)                             |
| [TeamInvitationsService](documentation/services/TeamInvitationsService.md)         |
| [TeamMembershipsService](documentation/services/TeamMembershipsService.md)         |
| [TeamRequestsService](documentation/services/TeamRequestsService.md)               |
| [TeamSourcesService](documentation/services/TeamSourcesService.md)                 |
| [HoneytokensService](documentation/services/HoneytokensService.md)                 |
| [HoneytokenNotesService](documentation/services/HoneytokenNotesService.md)         |
| [HoneytokenSourcesService](documentation/services/HoneytokenSourcesService.md)     |
| [HoneytokensEventsService](documentation/services/HoneytokensEventsService.md)     |
| [LabelsService](documentation/services/LabelsService.md)                           |
| [ScaService](documentation/services/ScaService.md)                                 |

</details>

## Models

The SDK includes several models that represent the data structures used in API requests and responses. These models help in organizing and managing the data efficiently.

<details> 
<summary>Below is a list of all available models with links to their detailed documentation:</summary>

| Name                                                                                                             | Description                                               |
| :--------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------- |
| [ApiTokenDetails](documentation/models/ApiTokenDetails.md)                                                       | Details of an API Token                                   |
| [ApiTokenStatusEnum](documentation/models/ApiTokenStatusEnum.md)                                                 |                                                           |
| [ApiTokenScopeEnum](documentation/models/ApiTokenScopeEnum.md)                                                   |                                                           |
| [ListApiTokensOrdering](documentation/models/ListApiTokensOrdering.md)                                           |                                                           |
| [PublicJwtCreateRequest](documentation/models/PublicJwtCreateRequest.md)                                         |                                                           |
| [PublicJwtCreateOkResponse](documentation/models/PublicJwtCreateOkResponse.md)                                   |                                                           |
| [IncidentWithoutOccurrences](documentation/models/IncidentWithoutOccurrences.md)                                 |                                                           |
| [StatusEnum](documentation/models/StatusEnum.md)                                                                 |                                                           |
| [SeverityEnum](documentation/models/SeverityEnum.md)                                                             |                                                           |
| [ValidityEnum](documentation/models/ValidityEnum.md)                                                             |                                                           |
| [ListIncidentsOrdering](documentation/models/ListIncidentsOrdering.md)                                           |                                                           |
| [Incident](documentation/models/Incident.md)                                                                     |                                                           |
| [RetrieveIncidentsLeaksOkResponse](documentation/models/RetrieveIncidentsLeaksOkResponse.md)                     |                                                           |
| [AssignIncidentRequest](documentation/models/AssignIncidentRequest.md)                                           |                                                           |
| [ResolveIncidentRequest](documentation/models/ResolveIncidentRequest.md)                                         |                                                           |
| [IgnoreIncidentRequest](documentation/models/IgnoreIncidentRequest.md)                                           |                                                           |
| [ShareIncidentRequest](documentation/models/ShareIncidentRequest.md)                                             |                                                           |
| [IncidentToken](documentation/models/IncidentToken.md)                                                           |                                                           |
| [GrantAccessIncidentRequest](documentation/models/GrantAccessIncidentRequest.md)                                 |                                                           |
| [RevokeAccessIncidentRequest](documentation/models/RevokeAccessIncidentRequest.md)                               |                                                           |
| [IncidentMember](documentation/models/IncidentMember.md)                                                         |                                                           |
| [IncidentPermissionEnum](documentation/models/IncidentPermissionEnum.md)                                         |                                                           |
| [MemberAccessLevelEnum](documentation/models/MemberAccessLevelEnum.md)                                           |                                                           |
| [IncidentTeam](documentation/models/IncidentTeam.md)                                                             |                                                           |
| [IncidentInvitation](documentation/models/IncidentInvitation.md)                                                 |                                                           |
| [Member](documentation/models/Member.md)                                                                         |                                                           |
| [ListSecretIncidentMemberAccessOrdering](documentation/models/ListSecretIncidentMemberAccessOrdering.md)         |                                                           |
| [Team](documentation/models/Team.md)                                                                             |                                                           |
| [Invitation](documentation/models/Invitation.md)                                                                 |                                                           |
| [ListSecretIncidentInvitationAccessOrdering](documentation/models/ListSecretIncidentInvitationAccessOrdering.md) |                                                           |
| [ListSourcesIncidentsOrdering](documentation/models/ListSourcesIncidentsOrdering.md)                             |                                                           |
| [ListTeamIncidentsOrdering](documentation/models/ListTeamIncidentsOrdering.md)                                   |                                                           |
| [IncidentNote](documentation/models/IncidentNote.md)                                                             |                                                           |
| [ListIncidentNotesOrdering](documentation/models/ListIncidentNotesOrdering.md)                                   |                                                           |
| [CreateIncidentNoteRequest](documentation/models/CreateIncidentNoteRequest.md)                                   |                                                           |
| [UpdateIncidentNoteRequest](documentation/models/UpdateIncidentNoteRequest.md)                                   |                                                           |
| [VcsOccurrence](documentation/models/VcsOccurrence.md)                                                           |                                                           |
| [SourceTypeQueryParamsEnum](documentation/models/SourceTypeQueryParamsEnum.md)                                   |                                                           |
| [PresenceEnum](documentation/models/PresenceEnum.md)                                                             |                                                           |
| [ListOccsOrdering](documentation/models/ListOccsOrdering.md)                                                     |                                                           |
| [ListInvitationsOrdering](documentation/models/ListInvitationsOrdering.md)                                       |                                                           |
| [CreateInvitationsRequest](documentation/models/CreateInvitationsRequest.md)                                     |                                                           |
| [ResendInvitationOkResponse](documentation/models/ResendInvitationOkResponse.md)                                 |                                                           |
| [ResourceInvitationAccess](documentation/models/ResourceInvitationAccess.md)                                     |                                                           |
| [ResourceType](documentation/models/ResourceType.md)                                                             |                                                           |
| [ListInvitationSecretIncidentAccessOrdering](documentation/models/ListInvitationSecretIncidentAccessOrdering.md) |                                                           |
| [ListMembersOrdering](documentation/models/ListMembersOrdering.md)                                               |                                                           |
| [ResourceMemberAccess](documentation/models/ResourceMemberAccess.md)                                             |                                                           |
| [ListMemberSecretIncidentAccessOrdering](documentation/models/ListMemberSecretIncidentAccessOrdering.md)         |                                                           |
| [TeamMembership](documentation/models/TeamMembership.md)                                                         |                                                           |
| [Document](documentation/models/Document.md)                                                                     |                                                           |
| [ScanResult](documentation/models/ScanResult.md)                                                                 | Result of a content scan.                                 |
| [DetectorGroup](documentation/models/DetectorGroup.md)                                                           |                                                           |
| [DetectorGroupTypeEnum](documentation/models/DetectorGroupTypeEnum.md)                                           |                                                           |
| [ListSecretDetectorsOrdering](documentation/models/ListSecretDetectorsOrdering.md)                               |                                                           |
| [Quota](documentation/models/Quota.md)                                                                           |                                                           |
| [ScanIacRequest](documentation/models/ScanIacRequest.md)                                                         |                                                           |
| [IacScanResult](documentation/models/IacScanResult.md)                                                           |                                                           |
| [DiffScanIacRequest](documentation/models/DiffScanIacRequest.md)                                                 |                                                           |
| [IacDiffScanResult](documentation/models/IacDiffScanResult.md)                                                   |                                                           |
| [Source](documentation/models/Source.md)                                                                         |                                                           |
| [ScanStatusEnum](documentation/models/ScanStatusEnum.md)                                                         |                                                           |
| [SourceHealthEnum](documentation/models/SourceHealthEnum.md)                                                     |                                                           |
| [ListSourcesOrdering](documentation/models/ListSourcesOrdering.md)                                               |                                                           |
| [ListSourcesVisibility](documentation/models/ListSourcesVisibility.md)                                           | Filter by visibility status.                              |
| [SourceCriticality](documentation/models/SourceCriticality.md)                                                   | Filter by source criticality.                             |
| [AuditLog](documentation/models/AuditLog.md)                                                                     |                                                           |
| [HealthCheckOkResponse](documentation/models/HealthCheckOkResponse.md)                                           | Health check response.                                    |
| [CreateTeamsRequest](documentation/models/CreateTeamsRequest.md)                                                 |                                                           |
| [ResourceTeamAccess](documentation/models/ResourceTeamAccess.md)                                                 |                                                           |
| [ListTeamSecretIncidentAccessOrdering](documentation/models/ListTeamSecretIncidentAccessOrdering.md)             |                                                           |
| [TeamInvitation](documentation/models/TeamInvitation.md)                                                         |                                                           |
| [TeamPermissionEnum](documentation/models/TeamPermissionEnum.md)                                                 |                                                           |
| [CreateTeamInvitationsRequest](documentation/models/CreateTeamInvitationsRequest.md)                             |                                                           |
| [UpdateTeamInvitationRequest](documentation/models/UpdateTeamInvitationRequest.md)                               |                                                           |
| [UpdateTeamMembershipRequest](documentation/models/UpdateTeamMembershipRequest.md)                               |                                                           |
| [TeamRequest](documentation/models/TeamRequest.md)                                                               |                                                           |
| [AcceptTeamRequestRequest](documentation/models/AcceptTeamRequestRequest.md)                                     |                                                           |
| [ListTeamSourcesType](documentation/models/ListTeamSourcesType.md)                                               | Filter by integration type.                               |
| [ListTeamSourcesOrdering](documentation/models/ListTeamSourcesOrdering.md)                                       |                                                           |
| [ListTeamSourcesVisibility](documentation/models/ListTeamSourcesVisibility.md)                                   | Filter by visibility status.                              |
| [UpdateTeamSourcesRequest](documentation/models/UpdateTeamSourcesRequest.md)                                     |                                                           |
| [Honeytoken](documentation/models/Honeytoken.md)                                                                 |                                                           |
| [ListHoneytokenStatus](documentation/models/ListHoneytokenStatus.md)                                             | Status of a honeytoken.                                   |
| [ListHoneytokenType](documentation/models/ListHoneytokenType.md)                                                 | Type of a honeytoken.                                     |
| [ListHoneytokenOrdering](documentation/models/ListHoneytokenOrdering.md)                                         |                                                           |
| [CreateHoneytokenRequest](documentation/models/CreateHoneytokenRequest.md)                                       |                                                           |
| [CreateHoneytokenWithContextRequest](documentation/models/CreateHoneytokenWithContextRequest.md)                 |                                                           |
| [HoneyTokenWithContext](documentation/models/HoneyTokenWithContext.md)                                           |                                                           |
| [UpdateHoneytokenRequest](documentation/models/UpdateHoneytokenRequest.md)                                       |                                                           |
| [HoneyTokenNote](documentation/models/HoneyTokenNote.md)                                                         |                                                           |
| [ListHoneytokenNotesOrdering](documentation/models/ListHoneytokenNotesOrdering.md)                               |                                                           |
| [CreateHoneytokenNoteRequest](documentation/models/CreateHoneytokenNoteRequest.md)                               |                                                           |
| [UpdateHoneytokenNoteRequest](documentation/models/UpdateHoneytokenNoteRequest.md)                               |                                                           |
| [HoneyTokenSource](documentation/models/HoneyTokenSource.md)                                                     |                                                           |
| [ListHoneytokenSourcesOrdering](documentation/models/ListHoneytokenSourcesOrdering.md)                           |                                                           |
| [HoneyTokenEvent](documentation/models/HoneyTokenEvent.md)                                                       |                                                           |
| [ListHoneytokensEventsOrdering](documentation/models/ListHoneytokensEventsOrdering.md)                           |                                                           |
| [ListHoneytokensEventsStatus](documentation/models/ListHoneytokensEventsStatus.md)                               |                                                           |
| [HoneyTokenLabel](documentation/models/HoneyTokenLabel.md)                                                       |                                                           |
| [CreateHoneytokenLabelRequest](documentation/models/CreateHoneytokenLabelRequest.md)                             |                                                           |
| [PatchHoneytokenLabelRequest](documentation/models/PatchHoneytokenLabelRequest.md)                               |                                                           |
| [ComputeScaFilesOkResponse](documentation/models/ComputeScaFilesOkResponse.md)                                   |                                                           |
| [ScaScanAllRequest](documentation/models/ScaScanAllRequest.md)                                                   |                                                           |
| [ScaScanAllOkResponse](documentation/models/ScaScanAllOkResponse.md)                                             |                                                           |
| [ScaScanDiffRequest](documentation/models/ScaScanDiffRequest.md)                                                 |                                                           |
| [ScaScanDiffOkResponse](documentation/models/ScaScanDiffOkResponse.md)                                           |                                                           |
| [ApiTokenTypeEnum](documentation/models/ApiTokenTypeEnum.md)                                                     |                                                           |
| [Detector](documentation/models/Detector.md)                                                                     |                                                           |
| [SecretStatusEnum](documentation/models/SecretStatusEnum.md)                                                     |                                                           |
| [TagEnum](documentation/models/TagEnum.md)                                                                       |                                                           |
| [OccurrenceKindEnum](documentation/models/OccurrenceKindEnum.md)                                                 |                                                           |
| [Match](documentation/models/Match.md)                                                                           |                                                           |
| [SecretIncidentsBreakdown](documentation/models/SecretIncidentsBreakdown.md)                                     | Detailed count of secret incidents linked to this source. |
| [Scan](documentation/models/Scan.md)                                                                             |                                                           |
| [SourceSeverityBreakdown](documentation/models/SourceSeverityBreakdown.md)                                       |                                                           |
| [SeverityBreakdown](documentation/models/SeverityBreakdown.md)                                                   |                                                           |
| [HmslSourceTypeEnum](documentation/models/HmslSourceTypeEnum.md)                                                 |                                                           |
| [NonOwnerMemberAccessLevelEnum](documentation/models/NonOwnerMemberAccessLevelEnum.md)                           |                                                           |
| [PolicyBreak](documentation/models/PolicyBreak.md)                                                               | Issue found in your Document                              |
| [Validity](documentation/models/Validity.md)                                                                     | Validity of the found secret.                             |
| [Matches](documentation/models/Matches.md)                                                                       |                                                           |
| [Content](documentation/models/Content.md)                                                                       |                                                           |
| [IacScanTarParameters](documentation/models/IacScanTarParameters.md)                                             |                                                           |
| [SeverityEnumIac](documentation/models/SeverityEnumIac.md)                                                       |                                                           |
| [EntitiesWithIncidents](documentation/models/EntitiesWithIncidents.md)                                           |                                                           |
| [Incidents](documentation/models/Incidents.md)                                                                   |                                                           |
| [IacStatusEnum](documentation/models/IacStatusEnum.md)                                                           |                                                           |
| [IacDiffScanResultEntitiesWithIncidents](documentation/models/IacDiffScanResultEntitiesWithIncidents.md)         |                                                           |
| [AuditLogActionTypeEnum](documentation/models/AuditLogActionTypeEnum.md)                                         |                                                           |
| [HoneytokenStatus](documentation/models/HoneytokenStatus.md)                                                     | Status of the honeytoken.                                 |
| [HoneytokenType](documentation/models/HoneytokenType.md)                                                         | Type of the honeytoken.                                   |
| [HoneyTokenEventTag](documentation/models/HoneyTokenEventTag.md)                                                 |                                                           |
| [CreateHoneytokenRequestType](documentation/models/CreateHoneytokenRequestType.md)                               | honeytoken type<br>                                       |
| [CreateHoneytokenWithContextRequestType](documentation/models/CreateHoneytokenWithContextRequestType.md)         | Honeytoken type.<br>                                      |
| [HoneyTokenSourceType](documentation/models/HoneyTokenSourceType.md)                                             |                                                           |
| [HoneyTokenEventStatus](documentation/models/HoneyTokenEventStatus.md)                                           | Status of the honeytoken event.                           |
| [ScaScanTarParameters](documentation/models/ScaScanTarParameters.md)                                             |                                                           |
| [ScaIgnoredVulnerability](documentation/models/ScaIgnoredVulnerability.md)                                       |                                                           |
| [LocationOutputSchema](documentation/models/LocationOutputSchema.md)                                             |                                                           |
| [PackageVulnerabilityOutputSchema](documentation/models/PackageVulnerabilityOutputSchema.md)                     |                                                           |
| [DependencyTypeEnum](documentation/models/DependencyTypeEnum.md)                                                 |                                                           |
| [ExposedVulnerabilityOutputSchema](documentation/models/ExposedVulnerabilityOutputSchema.md)                     |                                                           |

</details>

## License

This SDK is licensed under the MIT License.

See the [LICENSE](LICENSE) file for more details.

<!-- This file was generated by liblab | https://liblab.com/ -->
