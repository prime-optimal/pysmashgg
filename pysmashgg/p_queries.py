# Queries for players.py

PLAYER_SHOW_INFO_QUERY = """query ($playerId: ID!) {
  player(id: $playerId) {
    gamerTag
    user {
      name
      genderPronoun
      authorizations(types: [TWITTER, TWITCH, DISCORD]) {
        type
        externalUsername
        url
      }
      location {
        country
        state
        city
      }
    }
    rankings(videogameId: 1) {
      title
      rank
    }
  }
} """

PLAYER_SHOW_TOURNAMENTS_QUERY = """query ($playerId: ID!, $page: Int!) {
  player (id: $playerId) {
    user {
      tournaments (query: {perPage: 64, page: $page}) {
        nodes {
          name
          slug
          id
          numAttendees
          countryCode
          startAt
        }
      }
    }
  }
}"""

PLAYER_SHOW_TOURNAMENTS_FOR_GAME_QUERY = """query ($playerId: ID!, $playerName: String!, $videogameId: [ID!], $page: Int!) {
  player (id: $playerId) {
    user {
      tournaments (query: {perPage: 25, page: $page, filter: {videogameId: $videogameId}}) {
        nodes {
          name
          slug
          id
          numAttendees
          countryCode
          startAt
          events {
            name
            id
            slug
            numEntrants
            videogame {
              id
            }
            entrants (query: {filter: {name: $playerName}}) {
              nodes {
                id
              }
            }
          }
        }
      }
    }
  }
}"""

PLAYER_BY_SLUG_QUERY = """query Profile($discriminatorSlug: String!) {
  user(slug: $discriminatorSlug) {
    id
    name
    player {
      id
      gamerTag
      prefix
    }
    bio
    birthday
    discriminator
    slug
    location {
      country
      state
      city
    }
    authorizations(types: [TWITTER, TWITCH, DISCORD]) {
      type
      externalUsername
      url
    }
    images {
      id
      url
      height
      width
      ratio
      type
    }
    events(query:{page:1,perPage:10}) {
      nodes {
        id
        name
        numEntrants
        slug
        startAt
        videogame {
          id
          name
        }
      }
    }
  }
}"""

PLAYER_RECENT_PLACEMENTS_QUERY = """query ($playerId: ID!, $videogameId: ID!) {
  player(id: $playerId) {
    id
    gamerTag
    prefix
    user {
      name
      discriminator
      slug
      images {
        height
        width
        url
        type
      }
      authorizations(types: [TWITTER, TWITCH, DISCORD]) {
        type
        externalUsername
        url
      }
      location {
        country
        state
        city
      }
    }
    recentStandings(videogameId: $videogameId, limit: 20) {
      id
      placement
      entrant {
        id
        name
        event {
          id
          name
          slug
          isOnline
          numEntrants
          tournament {
            name
            startAt
            images {
              url
              width
              height
              type
            }
          }
          videogame {
            displayName
            images {
              type
              url
              width
              height
            }
          }
        }
      }
    }
  }
}"""

PLAYER_LOOKUP_ID_QUERY = """query LookupPlayerId($discriminatorSlug: String!) {
  user(slug: $discriminatorSlug) {
    player {
      id
    }
  }
}"""
