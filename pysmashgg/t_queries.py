# Core tournament-related queries

# Query to get basic tournament metadata
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

# Query to get tournament owner information
TOURNAMENT_OWNER_QUERY = """query ($tourneySlug: String!) {
  tournament(slug: $tourneySlug) {
    id
    name
    owner {
      id
      player {
        gamerTag
      }
    }
  }
}"""
