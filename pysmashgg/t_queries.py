# Queries for tournaments.py

# Query to get a player's ID from an event
PLAYER_ID_QUERY = """query EventEntrants($eventId: ID!, $name: String!) {
    event(id: $eventId) {
    entrants(query: {
      page: 1
      perPage: 32
      filter: {name: $name}
    }) {
      nodes {
        participants {
          gamerTag
          player {
            id 
          }
        }
      }
    }
    }
    }"""

# Query to get an event's ID from a tournament
EVENT_ID_QUERY = """query ($tourneySlug: String!) {
  tournament(slug: $tourneySlug) {
    events {
      id
      slug
    }
  }
}"""

# Query to get an entrant's ID from an event
ENTRANT_ID_QUERY = """query EventEntrants($eventId: ID!, $name: String!) {
    event(id: $eventId) {
    entrants(query: {
      page: 1
      perPage: 32
      filter: {
        name: $name
      }
    }) {
      nodes {
        id
        name
      }
    }
    }
    }"""

# Query to get basic tournament metadata
# Updated 2024-10-24: Added additional fields for tournament metadata:
# - owner (id, name) for tournament organizer information
# - links (discord, facebook) for social media
# - rules for tournament rules
# - publishing status
# - streams information
# - tournament images
SHOW_QUERY = """query ($tourneySlug: String!) {
  tournament(slug: $tourneySlug) {
    id
    name
    countryCode
    addrState
    city
    startAt
    endAt
    numAttendees
    links {
      discord
      facebook
    }
    rules
    publishing
    streams {
      id
      streamName
      streamSource
      streamGame
      streamStatus
      streamType
      isOnline
      followerCount
      streamLogo
      parentStreamId
      enabled
    }
    images {
      id
      url
    }
    owner {
      id
      name
    }
  }
}"""

# Query to get tournament metadata with bracket information
SHOW_WITH_BRACKETS_QUERY = """query ($tourneySlug: String!) {
  tournament(slug: $tourneySlug) {
    id
    name
    countryCode
    addrState
    city
    startAt
    endAt
    numAttendees
    events {
      id
      name
      slug
      phaseGroups {
        id
      }
    }
  }
}"""

# Query to get all events from a tournament
SHOW_EVENTS_QUERY = """query ($tourneySlug: String!) {
  tournament(slug: $tourneySlug) {
    events {
      id
      name
      slug
      numEntrants
    }
  }
}"""

# Query to get all sets from an event
SHOW_SETS_QUERY = """query EventSets($eventId: ID!, $page: Int!) {
  event(id: $eventId) {
    tournament {
      id
      name
    }
    name
    sets(page: $page, perPage: 18, sortType: STANDARD) {
      nodes {
        fullRoundText
        games {
          winnerId
          selections {
            selectionValue
            entrant {
              id
            }
          }
        }
        id
        slots {
          standing {
            id
            placement
            stats {
              score {
                value
              }
            }
          }
          entrant {
            id
            name
            participants {
              entrants {
                id
              }
              player {
                id
                gamerTag
              }
            }
          }
        }
        phaseGroup {
          id
          phase {
            name
          }
        }
      }
    }
  }
}"""

# Query to get all entrants from an event
SHOW_ENTRANTS_QUERY = """query EventStandings($eventId: ID!, $page: Int!) {
  event(id: $eventId) {
    id
    name
    standings(query: {
      perPage: 25,
      page: $page}){
      nodes {
        placement
        entrant {
          id
          name
          participants {
            player {
              id
              gamerTag
            }
          }
          seeds {
            seedNum
          }
        }
      }
    }
  }
}"""

# Query to get event bracket information
SHOW_EVENT_BRACKETS_QUERY = """query ($tourneySlug: String!) {
  tournament(slug: $tourneySlug) {
    events {
      name
      slug
      phaseGroups {
        id
      }
    }
  }
}"""

# Query to get sets for a specific entrant
SHOW_ENTRANT_SETS_QUERY = """query EventSets($eventId: ID!, $entrantId: ID!, $page: Int!) {
  event(id: $eventId) {
    sets(
      page: $page
      perPage: 16
      filters: {
        entrantIds: [$entrantId]
      }
    ) {
      nodes {
        id
        fullRoundText
        slots {
          standing {
            placement
            stats {
              score {
                value
              }
            }
          }
          entrant {
            id
            name
          }
        }
        phaseGroup {
          id
        }
      }
    }
  }
}"""

# Query to get events by game, size, and date range
SHOW_EVENT_BY_GAME_SIZE_DATED_QUERY = """query TournamentsByVideogame($page: Int!, $videogameId: [ID!], $after: Timestamp!, $before: Timestamp!) {
  tournaments(query: {
    perPage: 32
    page: $page
    sortBy: "startAt asc"
    filter: {
      past: false
      videogameIds: $videogameId
      afterDate: $after
      beforeDate: $before
    }
  }) {
    nodes {
      name
      id
      slug
      isOnline
      startAt
      endAt
      events {
        name
        id
        numEntrants
        videogame {
          id
        }
      }
    }
  }
}"""

# Query to get lightweight event results
SHOW_LIGHTWEIGHT_RESULTS_QUERY = """query EventStandings($eventId: ID!, $page: Int!,) {
  event(id: $eventId) {
    standings(query: {perPage: 64, page: $page}) {
      nodes {
        placement
        entrant {
          name
          id
          participants {
            player {
              gamerTag
              user {
                authorizations(types: [TWITTER, TWITCH, DISCORD]) {
                  type
                  externalUsername
                  url
                }
              }
            }
          }
        }
      }
    }
  }
}"""

# Query to get tournaments by country
SHOW_BY_COUNTRY_QUERY = """query TournamentsByCountry($countryCode: String!, $page: Int!) {
  tournaments(query: {
    perPage: 32,
    page: $page,
    sortBy: "startAt desc"
    filter: {
      countryCode: $countryCode
    }
  }) {
    nodes {
      id
      name
      slug
      numAttendees
      addrState
      city
      startAt
      endAt
      state
    }
  }
}"""

# Query to get tournaments by state
SHOW_BY_STATE_QUERY = """query TournamentsByState($state: String!, $page: Int!) {
  tournaments(query: {
    perPage: 32
    page: $page
    filter: {
      addrState: $state
    }
  }) {
    nodes {
      id
      name
      slug
      numAttendees
      city
      startAt
      endAt
      state
    }
  }
}"""

# Query to get tournaments by radius
SHOW_BY_RADIUS_QUERY = """query ($page: Int, $coordinates: String!, $radius: String!) {
  tournaments(query: {
    page: $page
    perPage: 32
    filter: {
      location: {
        distanceFrom: $coordinates,
        distance: $radius
      }
    }
  }) {
    nodes {
      id
      name
      slug
      numAttendees
      countryCode
      addrState
      city
      startAt
      endAt
      state
    }
  }
}"""

# Query to get players by sponsor
SHOW_PLAYERS_BY_SPONSOR = """query ($slug:String!, $sponsor: String!) {
  tournament(slug: $slug) {
    participants(query: {
      filter: {
        search: {
          fieldsToSearch: ["prefix"],
          searchString: $sponsor
        }
      }
    }) {
      nodes {
        id
        gamerTag
        user {
          name
          location {
            country
            state
            city
          }
          player {
            id
          }
        }
      }
    }
  }
}"""

# Query to get tournaments by owner
SHOW_BY_OWNER_QUERY = """query TournamentsByOwner($ownerId: ID!, $page: Int!) {
    tournaments(query: {
      perPage: 25,
      page: $page,
      filter: { ownerId: $ownerId }
    }) {
    nodes {
      id
      name
      slug
      numAttendees
      countryCode
      addrState
      city
      startAt
      endAt
      state
    }
  }
}"""

# Query to get video game ID
GET_VIDEOGAME_ID_QUERY = """query VideoGameQuery($name: String!) {
  videogames(query: {
    filter: {
      name: $name
    }
  }) {
    nodes {
      id
      name
    }
  }
}"""

# Query to get tournaments by video game
SHOW_BY_VIDEOGAME_QUERY = """query TournamentsByVideogame($videogameId: ID!, $page: Int!, $after: Timestamp!, $before: Timestamp!) {
  tournaments(query: {
    page: $page
    perPage: 25
    sortBy: "startAt asc"
    filter: {
      past: false
      videogameIds: [$videogameId]
      afterDate: $after
      beforeDate: $before
    }
  }) {
    nodes {
      id
      name
      slug
      numAttendees
      countryCode
      addrState
      city
      startAt
      endAt
      state
      events {
        id
        name
        numEntrants
        videogame {
          id
          name
        }
      }
    }
  }
}"""
