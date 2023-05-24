from elasticsearch_dsl import query


def search_person(
    search,
    search_params,
    param_nom,
    param_prenom,
    param_date_min,
    param_date_max,
    list_persons,
):
    search_options = []
    for person in list_persons:
        person_filters = []
        boost_queries = []
        # Nom
        nom_person = getattr(search_params, param_nom)
        if nom_person:
            # match queries returns any document containing the search item,
            # even if it contains another item
            for nom in nom_person.split(" "):
                person_filters.append(
                    {"match": {person["type_person"] + "." + person["match_nom"]: nom}}
                )
            # match_phrase on the name `keyword` makes sure to boost the documents
            # with the exact match
            # Example : search query "jean", the `match` will give "jean pierre" and
            # "jean" the same score. The match_phrase used with a 'should' query will
            # boost "jean" (the exact match) over "jean pierre"
            boost_queries.append(
                {
                    "match_phrase": {
                        person["type_person"]
                        + "."
                        + person["match_nom"]
                        + ".keyword": {
                            "query": nom_person,
                            "boost": 8,
                        }
                    }
                }
            )

        # Prénoms
        prenoms_person = getattr(search_params, param_prenom)
        if prenoms_person:
            # Same logic as "nom" is used for "prenoms"
            for prenom in prenoms_person.split(" "):
                person_filters.append(
                    {
                        "match": {
                            person["type_person"] + "." + person["match_prenom"]: prenom
                        }
                    }
                )
            boost_queries.append(
                {
                    "match_phrase": {
                        person["type_person"]
                        + "."
                        + person["match_prenom"]
                        + ".keyword": {
                            "query": prenoms_person,
                            "boost": 8,
                        }
                    }
                }
            )

        # Date de naissance
        min_date_naiss_person = getattr(search_params, param_date_min)
        if min_date_naiss_person:
            person_filters.append(
                {
                    "range": {
                        **{
                            person["type_person"]
                            + "."
                            + person["match_date"]: {"gte": min_date_naiss_person}
                        }
                    }
                }
            )

        max_date_naiss_person = getattr(search_params, param_date_max)
        if max_date_naiss_person:
            person_filters.append(
                {
                    "range": {
                        **{
                            person["type_person"]
                            + "."
                            + person["match_date"]: {"lte": max_date_naiss_person}
                        }
                    }
                }
            )

        # Using a query (must and should) instead of a filter because filters do not
        # give a score which in turn does not boost certain documents over others.
        # The `must` parameter removes documents which do not contain the query terms,
        # whereas the `should` clause gives higher scores to those documents without
        # removing the other documents.
        # Consequently, we use the `must` to find only the documents containing the
        # query terms, and use the `should` clause, with keyword, to give a higher
        # score to exact
        # matches
        if person_filters or boost_queries:
            search_options.append(
                query.Q(
                    "nested",
                    path=person["type_person"],
                    query=query.Bool(must=person_filters, should=boost_queries),
                )
            )

    search = search.query("bool", should=search_options)
    return search
