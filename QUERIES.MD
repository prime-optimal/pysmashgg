# This is a document to collect queries that we use with the start.gg API

## Query a player with the start.gg player profile slug

```
query Profile($discriminatorSlug: String!) {
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
}
```
## Get 20 most recent placements for a player in a specific game
```
query ($playerId: ID!, $videogameId: ID!) {
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
}
```

## Get the recent sets of a player from a specific event(s) and show results with an online/offline filter

```
query Sets($playerId: ID!, $isOnline: Boolean!, $eventId: [ID]) {
  player(id: $playerId) {
    id
    gamerTag
    user {
      slug
    }
    sets(perPage: 15, page: 1, filters: {isEventOnline: $isOnline, eventIds: $eventId}) {
      nodes {
        id
        fullRoundText
        displayScore
        slots(includeByes: true) {
          id
          entrant {
            id
            name
          }
          standing {
            stats {
              score {
                value
              }
            }
          }
        }
        winnerId
        completedAt
        event {
          id
          numEntrants
          isOnline
          tournament {
            name
            slug
            startAt
          }
        }
      }
    }
  }
}
```
