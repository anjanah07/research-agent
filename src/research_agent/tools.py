from duckduckgo_search import DDGS

def web_search(query:str) -> str:
    """
    Search the web for the given query and return the results
    """
    try:
        ddgs = DDGS()
        results = ddgs.text(keywords=query, max_results=3)
        if not results:
            return "No results found"
        formatted_results = ""
        for result in results:
            formatted_results += f"Title: {result['title']}\nLink: {result['href']}\n Description: {result['body']}\n\n"
        return formatted_results
    except Exception as e:
        return f"Error: {str(e)}"

AVAILABLE_TOOLS={
    "web_search": web_search,
}