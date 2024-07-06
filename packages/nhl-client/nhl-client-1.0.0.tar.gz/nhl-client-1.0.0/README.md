# Nhl Python SDK 1.0.0

Welcome to the Nhl SDK documentation. This guide will help you get started with integrating and using the Nhl SDK in your project.

## Versions

- API version: `1.0.0`
- SDK version: `1.0.0`

## About the API

Documenting the publicly accessible portions of the NHL API.

## Table of Contents

- [Setup & Configuration](#setup--configuration)
  - [Supported Language Versions](#supported-language-versions)
  - [Installation](#installation)
- [Services](#services)
- [Models](#models)
- [License](#license)

## Setup & Configuration

### Supported Language Versions

This SDK is compatible with the following versions: `Python >= 3.7`

### Installation

To get started with the SDK, we recommend installing using `pip`:

```bash
pip install nhl-client
```

## Services

The SDK provides various services to interact with the API.

<details> 
<summary>Below is a list of all available services with links to their detailed documentation:</summary>

| Name                                                               |
| :----------------------------------------------------------------- |
| [ConferencesService](documentation/services/ConferencesService.md) |
| [DivisionsService](documentation/services/DivisionsService.md)     |
| [DraftService](documentation/services/DraftService.md)             |
| [GamesService](documentation/services/GamesService.md)             |
| [PlayersService](documentation/services/PlayersService.md)         |
| [ScheduleService](documentation/services/ScheduleService.md)       |
| [StandingsService](documentation/services/StandingsService.md)     |
| [StatsService](documentation/services/StatsService.md)             |
| [TeamsService](documentation/services/TeamsService.md)             |

</details>

## Models

The SDK includes several models that represent the data structures used in API requests and responses. These models help in organizing and managing the data efficiently.

<details> 
<summary>Below is a list of all available models with links to their detailed documentation:</summary>

| Name                                                                                 | Description |
| :----------------------------------------------------------------------------------- | :---------- |
| [Conferences](documentation/models/Conferences.md)                                   |             |
| [Division](documentation/models/Division.md)                                         |             |
| [Divisions](documentation/models/Divisions.md)                                       |             |
| [Draft](documentation/models/Draft.md)                                               |             |
| [DraftProspects](documentation/models/DraftProspects.md)                             |             |
| [GameBoxscores](documentation/models/GameBoxscores.md)                               |             |
| [GameContent](documentation/models/GameContent.md)                                   |             |
| [Game](documentation/models/Game.md)                                                 |             |
| [Players](documentation/models/Players.md)                                           |             |
| [PlayerStats](documentation/models/PlayerStats.md)                                   |             |
| [GetPlayerStatsStats](documentation/models/GetPlayerStatsStats.md)                   |             |
| [Schedule](documentation/models/Schedule.md)                                         |             |
| [GetScheduleExpand](documentation/models/GetScheduleExpand.md)                       |             |
| [Standings](documentation/models/Standings.md)                                       |             |
| [GetStandingsByTypeType](documentation/models/GetStandingsByTypeType.md)             |             |
| [StandingTypes](documentation/models/StandingTypes.md)                               |             |
| [StatTypes](documentation/models/StatTypes.md)                                       |             |
| [Teams](documentation/models/Teams.md)                                               |             |
| [GetTeamsExpand](documentation/models/GetTeamsExpand.md)                             |             |
| [Team](documentation/models/Team.md)                                                 |             |
| [Rosters](documentation/models/Rosters.md)                                           |             |
| [TeamStats](documentation/models/TeamStats.md)                                       |             |
| [Conference](documentation/models/Conference.md)                                     |             |
| [ConferenceName](documentation/models/ConferenceName.md)                             |             |
| [Abbreviation](documentation/models/Abbreviation.md)                                 |             |
| [ShortName](documentation/models/ShortName.md)                                       |             |
| [DivisionConference](documentation/models/DivisionConference.md)                     |             |
| [Drafts](documentation/models/Drafts.md)                                             |             |
| [Rounds](documentation/models/Rounds.md)                                             |             |
| [Picks](documentation/models/Picks.md)                                               |             |
| [PicksTeam](documentation/models/PicksTeam.md)                                       |             |
| [Prospect](documentation/models/Prospect.md)                                         |             |
| [DraftProspect](documentation/models/DraftProspect.md)                               |             |
| [DraftProspectPrimaryPosition](documentation/models/DraftProspectPrimaryPosition.md) |             |
| [ProspectCategory](documentation/models/ProspectCategory.md)                         |             |
| [AmateurTeam](documentation/models/AmateurTeam.md)                                   |             |
| [AmateurLeague](documentation/models/AmateurLeague.md)                               |             |
| [GameBoxscoresTeams](documentation/models/GameBoxscoresTeams.md)                     |             |
| [GameOfficial](documentation/models/GameOfficial.md)                                 |             |
| [GameBoxscoreTeam](documentation/models/GameBoxscoreTeam.md)                         |             |
| [GameBoxscoreTeamTeam](documentation/models/GameBoxscoreTeamTeam.md)                 |             |
| [GameBoxscoreTeamTeamStats](documentation/models/GameBoxscoreTeamTeamStats.md)       |             |
| [GameBoxscoreTeamPlayers](documentation/models/GameBoxscoreTeamPlayers.md)           |             |
| [OnIcePlus](documentation/models/OnIcePlus.md)                                       |             |
| [Coaches](documentation/models/Coaches.md)                                           |             |
| [TeamSkaterStats](documentation/models/TeamSkaterStats.md)                           |             |
| [PlayersPerson](documentation/models/PlayersPerson.md)                               |             |
| [PlayersPosition](documentation/models/PlayersPosition.md)                           |             |
| [PlayersStats](documentation/models/PlayersStats.md)                                 |             |
| [SkaterStats](documentation/models/SkaterStats.md)                                   |             |
| [CoachesPerson](documentation/models/CoachesPerson.md)                               |             |
| [CoachesPosition](documentation/models/CoachesPosition.md)                           |             |
| [Official](documentation/models/Official.md)                                         |             |
| [OfficialType](documentation/models/OfficialType.md)                                 |             |
| [Editorial](documentation/models/Editorial.md)                                       |             |
| [GameContentMedia](documentation/models/GameContentMedia.md)                         |             |
| [Highlights](documentation/models/Highlights.md)                                     |             |
| [GameEditorials](documentation/models/GameEditorials.md)                             |             |
| [GameEditorial](documentation/models/GameEditorial.md)                               |             |
| [TokenData](documentation/models/TokenData.md)                                       |             |
| [Contributor](documentation/models/Contributor.md)                                   |             |
| [GameEditorialKeyword](documentation/models/GameEditorialKeyword.md)                 |             |
| [GameEditorialMedia](documentation/models/GameEditorialMedia.md)                     |             |
| [TokenDataType](documentation/models/TokenDataType.md)                               |             |
| [Contributors](documentation/models/Contributors.md)                                 |             |
| [GameEditorialKeywordType](documentation/models/GameEditorialKeywordType.md)         |             |
| [Photo](documentation/models/Photo.md)                                               |             |
| [Cuts](documentation/models/Cuts.md)                                                 |             |
| [Milestones](documentation/models/Milestones.md)                                     |             |
| [Title](documentation/models/Title.md)                                               |             |
| [Items](documentation/models/Items.md)                                               |             |
| [ItemsType](documentation/models/ItemsType.md)                                       |             |
| [GameHighlight](documentation/models/GameHighlight.md)                               |             |
| [GameHighlightType_1](documentation/models/GameHighlightType1.md)                    |             |
| [Playbacks](documentation/models/Playbacks.md)                                       |             |
| [PlaybacksName](documentation/models/PlaybacksName.md)                               |             |
| [GameHighlights](documentation/models/GameHighlights.md)                             |             |
| [GameHighlightsGameCenter_2](documentation/models/GameHighlightsGameCenter2.md)      |             |
| [MetaData](documentation/models/MetaData.md)                                         |             |
| [GameData](documentation/models/GameData.md)                                         |             |
| [LiveData](documentation/models/LiveData.md)                                         |             |
| [GameDataGame](documentation/models/GameDataGame.md)                                 |             |
| [Datetime](documentation/models/Datetime.md)                                         |             |
| [GameDataStatus](documentation/models/GameDataStatus.md)                             |             |
| [GameDataTeams](documentation/models/GameDataTeams.md)                               |             |
| [Player](documentation/models/Player.md)                                             |             |
| [GameDataVenue](documentation/models/GameDataVenue.md)                               |             |
| [Venue](documentation/models/Venue.md)                                               |             |
| [TeamDivision](documentation/models/TeamDivision.md)                                 |             |
| [TeamConference](documentation/models/TeamConference.md)                             |             |
| [Franchise](documentation/models/Franchise.md)                                       |             |
| [TeamRoster](documentation/models/TeamRoster.md)                                     |             |
| [NextGameSchedule](documentation/models/NextGameSchedule.md)                         |             |
| [TimeZone](documentation/models/TimeZone.md)                                         |             |
| [Roster](documentation/models/Roster.md)                                             |             |
| [RosterPerson](documentation/models/RosterPerson.md)                                 |             |
| [RosterPosition](documentation/models/RosterPosition.md)                             |             |
| [Dates](documentation/models/Dates.md)                                               |             |
| [Games](documentation/models/Games.md)                                               |             |
| [GamesStatus](documentation/models/GamesStatus.md)                                   |             |
| [GamesTeams](documentation/models/GamesTeams.md)                                     |             |
| [GamesVenue](documentation/models/GamesVenue.md)                                     |             |
| [GamesContent](documentation/models/GamesContent.md)                                 |             |
| [AbstractGameState](documentation/models/AbstractGameState.md)                       |             |
| [CodedGameState](documentation/models/CodedGameState.md)                             |             |
| [DetailedState](documentation/models/DetailedState.md)                               |             |
| [StatusCode](documentation/models/StatusCode.md)                                     |             |
| [TeamsAway_1](documentation/models/TeamsAway1.md)                                    |             |
| [TeamsHome_1](documentation/models/TeamsHome1.md)                                    |             |
| [AwayLeagueRecord_1](documentation/models/AwayLeagueRecord1.md)                      |             |
| [AwayTeam_1](documentation/models/AwayTeam1.md)                                      |             |
| [HomeLeagueRecord_1](documentation/models/HomeLeagueRecord1.md)                      |             |
| [HomeTeam_1](documentation/models/HomeTeam1.md)                                      |             |
| [ShootsCatches](documentation/models/ShootsCatches.md)                               |             |
| [CurrentTeam](documentation/models/CurrentTeam.md)                                   |             |
| [PlayerPrimaryPosition](documentation/models/PlayerPrimaryPosition.md)               |             |
| [Plays](documentation/models/Plays.md)                                               |             |
| [GameLinescore](documentation/models/GameLinescore.md)                               |             |
| [GameBoxscore](documentation/models/GameBoxscore.md)                                 |             |
| [Decisions](documentation/models/Decisions.md)                                       |             |
| [GamePlay](documentation/models/GamePlay.md)                                         |             |
| [PlaysByPeriod](documentation/models/PlaysByPeriod.md)                               |             |
| [GamePlayPlayers](documentation/models/GamePlayPlayers.md)                           |             |
| [Result](documentation/models/Result.md)                                             |             |
| [About](documentation/models/About.md)                                               |             |
| [Coordinates](documentation/models/Coordinates.md)                                   |             |
| [GamePlayTeam](documentation/models/GamePlayTeam.md)                                 |             |
| [PlayersPlayer](documentation/models/PlayersPlayer.md)                               |             |
| [Goals](documentation/models/Goals.md)                                               |             |
| [GamePeriod](documentation/models/GamePeriod.md)                                     |             |
| [ShootoutInfo](documentation/models/ShootoutInfo.md)                                 |             |
| [GameLinescoreTeams](documentation/models/GameLinescoreTeams.md)                     |             |
| [IntermissionInfo](documentation/models/IntermissionInfo.md)                         |             |
| [PowerPlayInfo](documentation/models/PowerPlayInfo.md)                               |             |
| [GamePeriodHome](documentation/models/GamePeriodHome.md)                             |             |
| [GamePeriodAway](documentation/models/GamePeriodAway.md)                             |             |
| [ShootoutInfoAway](documentation/models/ShootoutInfoAway.md)                         |             |
| [ShootoutInfoHome](documentation/models/ShootoutInfoHome.md)                         |             |
| [GameLinescoreTeam](documentation/models/GameLinescoreTeam.md)                       |             |
| [GameLinescoreTeamTeam](documentation/models/GameLinescoreTeamTeam.md)               |             |
| [GameBoxscoreTeams](documentation/models/GameBoxscoreTeams.md)                       |             |
| [GameDecisionPlayer](documentation/models/GameDecisionPlayer.md)                     |             |
| [PlayerStatsStats](documentation/models/PlayerStatsStats.md)                         |             |
| [StatsType_1](documentation/models/StatsType1.md)                                    |             |
| [StatsSplits_1](documentation/models/StatsSplits1.md)                                |             |
| [TypeDisplayName](documentation/models/TypeDisplayName.md)                           |             |
| [SplitsStat_1](documentation/models/SplitsStat1.md)                                  |             |
| [Opponent](documentation/models/Opponent.md)                                         |             |
| [OpponentDivision](documentation/models/OpponentDivision.md)                         |             |
| [OpponentConference](documentation/models/OpponentConference.md)                     |             |
| [ScheduleDay](documentation/models/ScheduleDay.md)                                   |             |
| [ScheduleGame](documentation/models/ScheduleGame.md)                                 |             |
| [ScheduleGameStatus](documentation/models/ScheduleGameStatus.md)                     |             |
| [ScheduleGameTeams](documentation/models/ScheduleGameTeams.md)                       |             |
| [ScheduleGameVenue](documentation/models/ScheduleGameVenue.md)                       |             |
| [Tickets](documentation/models/Tickets.md)                                           |             |
| [ScheduleGameContent](documentation/models/ScheduleGameContent.md)                   |             |
| [TeamsAway_2](documentation/models/TeamsAway2.md)                                    |             |
| [TeamsHome_2](documentation/models/TeamsHome2.md)                                    |             |
| [AwayLeagueRecord_2](documentation/models/AwayLeagueRecord2.md)                      |             |
| [AwayTeam_2](documentation/models/AwayTeam2.md)                                      |             |
| [HomeLeagueRecord_2](documentation/models/HomeLeagueRecord2.md)                      |             |
| [HomeTeam_2](documentation/models/HomeTeam2.md)                                      |             |
| [TicketType](documentation/models/TicketType.md)                                     |             |
| [Records](documentation/models/Records.md)                                           |             |
| [StandingsType](documentation/models/StandingsType.md)                               |             |
| [League](documentation/models/League.md)                                             |             |
| [RecordsDivision](documentation/models/RecordsDivision.md)                           |             |
| [RecordsConference](documentation/models/RecordsConference.md)                       |             |
| [TeamRecords](documentation/models/TeamRecords.md)                                   |             |
| [TeamRecordsTeam](documentation/models/TeamRecordsTeam.md)                           |             |
| [TeamRecordsLeagueRecord](documentation/models/TeamRecordsLeagueRecord.md)           |             |
| [Streak](documentation/models/Streak.md)                                             |             |
| [StatTypesDisplayName](documentation/models/StatTypesDisplayName.md)                 |             |
| [TeamStatsStats](documentation/models/TeamStatsStats.md)                             |             |
| [StatsType_2](documentation/models/StatsType2.md)                                    |             |
| [StatsSplits_2](documentation/models/StatsSplits2.md)                                |             |
| [SplitsStat_2](documentation/models/SplitsStat2.md)                                  |             |
| [SplitsTeam](documentation/models/SplitsTeam.md)                                     |             |

</details>

## License

This SDK is licensed under the MIT License.

See the [LICENSE](LICENSE) file for more details.

<!-- This file was generated by liblab | https://liblab.com/ -->
