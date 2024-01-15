import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai

def main_function():
  # Load environment variables
  load_dotenv()
  
  # Fetch Discord token from environment variables
  token = os.getenv('DISCORD_API_TOKEN')
  
  # Fetch Gemini token from environment variables
  api_key = os.getenv('GOOGLE_GEMINI_API_TOKEN')
  
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "generative-ai-gemini-1024a62eb540.json"
  
  # Configure GenerativeAI
  genai.configure(api_key= api_key)
  
  # Initialize Generative Model Settings
  generation_config = {
      "temperature": 0.9,
      "top_p": 1,
      "top_k": 1,
      "max_output_tokens": 2048,
  }
  
  safety_settings = [
      {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
      {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
      {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
      {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  ]
  
  model = genai.GenerativeModel(
      model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings
  )
  
  prompt_parts = []
  
  
  # Initialize the bot with intents
  intents = discord.Intents.all()
  bot = commands.Bot(command_prefix='', intents=intents)
  
  # Event: Bot is ready
  @bot.event
  async def on_ready():
      print(f'Logged in as {bot.user.name}')
  
  # Event: Message received
  @bot.event
  async def on_message(message):
      try:  # Add a try-except block to catch any exceptions and print them for debugging
          # Ignore messages sent by the bot itself
          if message.author == bot.user:
              # print("Message sent by the bot itself. Ignoring.")
              return
          # Process user messages
  
          # Print received message content for debugging
          # print(f"Received message content: {message.content}")  
          prompt_parts.append(message.content)
  
          # Generate content using the model
          response = model.generate_content(prompt_parts)
  
          # Append the generated response to prompt_parts
          prompt_parts.append(response.text)
  
          # Print the generated response for debugging
          # print(f"Generated response: {response.text}")  
  
          # Send the generated response back to the channel
          await message.channel.send(response.text)
  
      except Exception as e:  # Catch any exceptions and print them for debugging
          print(f"An error occurred: {e}")
  
  # Run the bot using the token
  bot.run(token)
  
main_function()
  

