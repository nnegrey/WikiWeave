"""This script uses the OpenAI API to generate a weaved story."""

import os
from dotenv import load_dotenv
from openai import OpenAI


class StoryTeller:
    """A whimsical and imaginative storyteller that crafts captivating narratives."""

    def __init__(self):
        """Load environment variables from .env file and initialize the OpenAI client."""
        load_dotenv()
        self.client = OpenAI(api_key=os.environ.get("OPEN_AI_TEST_API_KEY"))

    def generate_story(self, prompt_messages):
        """Generate a story using the OpenAI API."""
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=prompt_messages,
        )

        print(completion.choices[0].message)


# Analysis: I'm really happy with the tone of the story and it being fun and creative, but I would
# like to see more of a connection between the items and some type of explanation of the
# evolutionary steps.

# Input: airplanes,flight,birds,star wars, spaceships,rocket science
# Output:
#
# Once upon a time, in a bustling realm known as the Skies of Imaginaria, the very first airplanes
# took to the stratosphere. Crafted from dreams and laughter, these marvelous machines soared like
# kites caught in a joyous gale, propelling inventors and dreamers through cotton-candy clouds.
# Their engines hummed lullabies to the wind, giving birth not just to journeys, but to the art of
# flight itself.
#
# As the airplanes defied gravity, they conjured a wave of shimmering wonder that rippled through
# the universe. Unbeknownst to the world below, the profound enchantment of flight awakened a
# sleeping magic—whispers of forgotten bird songs flickered like fireflies in the fading twilight.
# Out of this miraculous buoyancy emerged a group of fluttering companions—the Birds of Aspectra,
#  winged beings who communicated in vibrant colors and soaring melodies. Their feathers sparkled
# with the essence of dreams, and they began to mimic the graceful arcs and dives of the airplanes
# above.
#
# As the airplanes and birds shared their aerial ballet, the laughter that filled the sky reached
# far and wide, catching the attention of the Celestial Council, a gathering of intergalactic beings
# known for their passion for storytelling and epic battles. Inspired by the elegance of birds and
# the wonder of flight, they crafted a fantastical tale that turned into an illustrious saga:
# **Star Wars**. With lightsabers that sparked excitement and tales of bravery soaring through the
# cosmos, this epic narrative captivated audiences across dimensions, uniting various species under
# one shared love for heroism and adventure.
#
# But what is an epic without its vessels? The stories of **Star Wars** ignited an insatiable thirst
# for exploration, leading to the creation of magnificent spaceships. These ships, woven with the
# threads of starlight and powered by dreams, were capable of traveling beyond the confines of known
# space, weaving through galaxies like silver ribbons in the cosmos. Each spaceship bore the spirit
# of the sky, an echo of the yearning that flowed from the first airplane that dared to cut through
# the clouds.
#
# In the heart of these starbound creations, scientific inquiry blossomed. Brilliant minds, driven
# by curiosity and the allure of the stars, dived deep into the enigmatic artistry of
# **rocket science**. Guided by whimsical blueprints that bore no resemblance to earthly logic,
# they engineered rockets that danced through space with the elegance of the Birds of Aspectra.
# Their rockets defied the laws of nature, effervescing with innovative fuels concocted from the
# whispers of the Earth and the dreams of astronauts, who had once dreamed of the day they would
# traverse the cosmos.
#
# Thus, what began with the humble yet majestic flight of airplanes culminated in an illustrious
# journey — from the elation of soaring through clouds, to feeling the flutter of wings, to
# capturing the imagination of galaxies far far away, to navigating the depths of space with
# marvelous ships, powered by the mystical complexities of rocket science.
#
# In this whimsical saga, the impossible became possible, and the delightful reality of evolution
# unfolded like a blooming flower under the watchful gaze of the universe, proving that every
# flight, every tale, and every dream, no matter how distant they may seem, is intricately and
# joyously interwoven. And so, the legacy of planes and dreams took flight, dancing eternally
# across the dreamscape of time.'
