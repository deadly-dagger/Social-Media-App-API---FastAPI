const object1 = {
  query: {
    function_score: {
      query: {
        bool: {
          must: {
            bool: {
              minimum_should_match: 1,
              should: [
                {
                  multi_match: {
                    minimum_should_match: "2<67%",
                    query: "{{baseUrl}}/v1/account_links",
                    type: "best_fields",
                    fields: ["url", "url.wildcardUrl"],
                    tie_breaker: 1,
                  },
                },
                {
                  term: {
                    "url.raw": {
                      value: "{{baseUrl}}/v1/account_links",
                      boost: 30,
                    },
                  },
                },
                {
                  bool: {
                    must: [
                      {
                        match: {
                          "url.path": {
                            query: "{{baseUrl}}/v1/account_links",
                            minimum_should_match: "2<67%",
                          },
                        },
                      },
                      {
                        match: {
                          customHostName: {
                            query: "{{baseUrl}}/v1/account_links",
                            minimum_should_match: "2<67%",
                          },
                        },
                      },
                    ],
                  },
                },
                {
                  bool: {
                    must: [
                      {
                        match: {
                          "url.path": {
                            query: "{{baseUrl}}/v1/account_links",
                            minimum_should_match: "2<67%",
                          },
                        },
                      },
                      {
                        match: {
                          customHostName: {
                            query: "{{baseUrl}}/v1/account_links",
                            minimum_should_match: "2<67%",
                          },
                        },
                      },
                    ],
                  },
                },
              ],
              filter: {
                bool: {
                  must: [
                    {
                      bool: {
                        should: [
                          {
                            match: {
                              collectionTags: "FEATURED",
                            },
                          },
                          {
                            match: {
                              isPublisherVerified: true,
                            },
                          },
                          {
                            range: {
                              collectionForkCount: {
                                gte: 100,
                              },
                            },
                          },
                        ],
                        minimum_should_match: 1,
                      },
                    },
                  ],
                  must_not: [
                    {
                      bool: {
                        minimum_should_match: 1,
                        should: [
                          {
                            bool: {
                              must: [
                                {
                                  terms: {
                                    publisherId: ["125648"],
                                  },
                                },
                                {
                                  term: {
                                    publisherType: "team",
                                  },
                                },
                              ],
                            },
                          },
                          {
                            term: {
                              isBlacklisted: true,
                            },
                          },
                        ],
                      },
                    },
                    {
                      terms: {
                        type: [
                          "ws-raw-request",
                          "grpc-request",
                          "ws-socketio-request",
                        ],
                      },
                    },
                  ],
                },
              },
            },
          },
          should: [
            {
              match: {
                "url.hostName": {
                  query: "{{baseUrl}}/v1/account_links",
                  boost: 10,
                },
              },
            },
            {
              match_phrase: {
                "url.hostName": {
                  query: "{{baseUrl}}/v1/account_links",
                  boost: 10,
                },
              },
            },
            {
              match: {
                "url.path": {
                  query: "{{baseUrl}}/v1/account_links",
                  boost: 10,
                },
              },
            },
            {
              match: {
                customHostName: {
                  query: "{{baseUrl}}/v1/account_links",
                  boost: 10,
                },
              },
            },
            {
              match_phrase: {
                customHostName: {
                  query: "{{baseUrl}}/v1/account_links",
                  boost: 10,
                },
              },
            },
            {
              match: {
                method: {
                  query: "GET",
                  boost: 10,
                },
              },
            },
            {
              match: {
                name: {
                  query: "ES context bar query",
                  boost: 10,
                },
              },
            },
          ],
        },
      },
      functions: [
        {
          field_value_factor: {
            field: "collectionViews",
            factor: 1,
            modifier: "log1p",
            missing: 0,
          },
          weight: 5,
        },
        {
          field_value_factor: {
            field: "collectionForkCount",
            factor: 1,
            modifier: "log1p",
            missing: 0,
          },
          weight: 10,
        },
        {
          filter: {
            term: {
              isDomainNonTrivial: true,
            },
          },
          weight: 10,
        },
        {
          filter: {
            term: {
              collectionTags: "FEATURED",
            },
          },
          weight: 10,
        },
        {
          filter: {
            term: {
              isPublisherVerified: true,
            },
          },
          weight: 10,
        },
        {
          filter: {
            exists: {
              field: "curatedInList",
            },
          },
          weight: 20,
        },
      ],
      score_mode: "sum",
      boost_mode: "sum",
    },
  },
  _source: {
    excludes: [
      "description",
      "collectionCategories",
      "createdAt",
      "updatedAt",
      "users",
      "isDomainNonTrivial",
    ],
  },
  from: 7,
  size: 7,
};
