# Event-specific queries

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

# Query to get an event's ID from a tournament
EVENT_ID_QUERY = """query ($tourneySlug: String!) {
  tournament(slug: $tourneySlug) {
    events {
      id
      slug
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
