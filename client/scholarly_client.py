from scholarly import scholarly

class ScholarlyClient:

    @staticmethod
    def get_author_profile(name, affiliation):
        search_query = scholarly.search_author(name)
        for result in search_query:
            if affiliation and affiliation.lower() not in result['affiliation'].lower():
                continue
            return scholarly.fill(result)
        return None

    @staticmethod
    def get_publications(profile):
        if not profile:
            return []
        publications = []
        for pub in profile["publications"][:5]:
            filled = scholarly.fill(pub)

            pub_url = filled.get("pub_url")
            if not pub_url and "cluster_id" in filled:
                pub_url = f"https://scholar.google.com/scholar?cluster={filled['cluster_id']}"

            publications.append({
                "title": filled["bib"]["title"],
                "year": filled["bib"].get("pub_year", "N/A"),
                "citations": filled.get("num_citations", 0),
                "url": pub_url or "N/A"
            })
        return publications
