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


def summarise():
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
            that can be represented in plain text. The following are the titles and contents to the articles:
            Article 1 - {top_tech.title}:
            {all_text[0]}
            
            Article 2 - {top_world[0].title}:
            {all_text[1]}

            Article 3 - {top_world[1].title}:
            {all_text[2]}"""
        )

        text_summary = response1.text

        # Generate the infographics using Gemini's native image model thingy
        response2 = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=f'Make 3 separate concise infographic cards with striking stats on these topics: 1. {top_tech.title}, 2. {top_world[0].title}, 3. {top_world[1].title}',
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="9:16"
                )
            )
        )

        # Extract and save images from response parts
        image_counter = 1
        for candidate in response2.candidates:
            for part in candidate.content.parts:
                if part.inline_data:
                    time.sleep(4)
                    # Use part.as_image() helper provided by google-genai
                    img = part.as_image()
                    file_name = f'generated_image{image_counter}.png'
                    img.save(file_name)
                    print(f'Saved image as "{file_name}".')
                    image_counter += 1

        return text_summary

        

if __name__ == '__main__':
    time.sleep(60)
    summary = summarise()
    print("------- SUMMARY OUTPUT -------")
    print(summary)