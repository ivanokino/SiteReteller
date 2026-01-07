from openai import AsyncOpenAI


client = AsyncOpenAI(api_key="",
                base_url="https://openrouter.ai/api/v1")


retell_prompt = 'Your task is simply to paraphrase the text from this fragment taken from the website. Dont say anything like, "Okay, Ill do it now," JUST paraphrase it. If the website is just a registration page or some kind of bot protection, just say you wont be able to read the data and explain why.'
