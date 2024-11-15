# Location-based queries for finding tournaments

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
