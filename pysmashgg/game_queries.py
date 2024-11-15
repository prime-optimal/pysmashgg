# Game-related queries for tournaments and events

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
