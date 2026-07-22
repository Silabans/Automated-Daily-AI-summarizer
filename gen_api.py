import google.genai as ai
from google.genai import types
from pygooglenews import GoogleNews
import time
from newspaper import Article
from googlenewsdecoder import gnewsdecoder


def extract(raw_url):
    try:
        decoded = gnewsdecoder(raw_url)
        real_url = decoded.get('decoded_url', raw_url)

        article = Article(real_url)
        article.download() # loads the raw html
        article.parse() # formats and streamlines the html into callable parts (eg: article.text)
        return article.text
    
    except Exception as e:
        print(f'Extraction failed for {raw_url}: {e}')
        return 'Content Unavailable'


def summarise() -> str:
    # Finds and Collects relevant news
    gn = GoogleNews(lang='en', country='SG')

    tech_news = gn.topic_headlines('TECHNOLOGY')
    top_tech = tech_news['entries'][0]

    world_news = gn.topic_headlines('WORLD')
    top_world = [item for item in world_news['entries'][:2]]

    articles = [top_tech] + top_world

    # Text extraction
    all_text = []
    for article in articles:
        text = extract(article.link)
        all_text.append(text)

    # Generate the summary
    with ai.Client() as client:
        response1 = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=f"""Summarise these 3 article, 2 short paragraphs each, with the important statistics
            being listed at the end of each article summary. Do not use complex formatting - only use
            that can be represented in plain text. Each article summary should be separated by 2 newlines (2 empty newlines inbetween).
            Start each summary with its title and article number (1, 2 or 3).
            The following are the titles and contents to the articles:

            Article 1 - {top_tech.title}:
            {all_text[0]}
            
            Article 2 - {top_world[0].title}:
            {all_text[1]}

            Article 3 - {top_world[1].title}:
            {all_text[2]}"""
        )

        text_summary = str(response1.text)

        final = "------- NEWS OF THE DAY -------\n\n" + text_summary
        return final

        

if __name__ == '__main__':
    summary = summarise()
    print("------- SUMMARY OUTPUT -------")
    print(summary)

    