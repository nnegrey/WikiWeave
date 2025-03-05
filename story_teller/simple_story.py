""" This script uses the OpenAI API to generate a weaved story. """

import os
from dotenv import load_dotenv
from openai import OpenAI


class StoryTeller:
    """A whimsical and imaginative storyteller that crafts captivating narratives."""

    def __init__(self):
        """Load environment variables from .env file and initialize the OpenAI client."""
        load_dotenv()
        self.client = OpenAI(api_key=os.environ.get("OPEN_AI_TEST_API_KEY"))

    def generate_story(self):
        """Generate a story using the OpenAI API."""
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=self.__create_the_prompt_messages(),
        )

        print(completion.choices[0].message)

    def __create_the_prompt_messages(self):
        messages = []
        # Set up the Developer Role
        messages.append(
            {
                "role": "developer",
                "content": (
                    "You are a whimsical and imaginative storyteller, a weaver of tales that "
                    "bend the very fabric of reality."
                ),
            }
        )
        # Set up the Task
        messages.append(
            {
                "role": "user",
                "content": "Your task is to create a captivating narrative that "
                "connects two seemingly disparate concepts, using a series of intermediary ideas "
                "as essential stepping stones in this evolutionary process. You will be given a "
                "list of items, each representing a stage "
                "in a fantastical evolutionary journey. Your mission is to craft a story that "
                "explains how the first item, through a series of improbable but delightful "
                "transformations, ultimately led to the creation or evolution of the last item. "
                "You should use your existing knowledge of the items to creatively link them in "
                "known or new ways. "
                "Embrace the absurd and the fantastical. Feel free to defy conventional logic and "
                "scientific understanding. The goal is not to be accurate, but to be entertaining "
                "and imaginative.",
            },
        )
        # Set up the Guidelines
        messages.append(
            {
                "role": "user",
                "content": "**Guidelines:** "
                "1. **Sequential Flow:** The narrative should progress logically, detailing how "
                "each item contributed to the emergence of the next item in a directed chain of "
                "evolution. "
                "2. **Creative Imagination:** Embrace imagination within each section "
                "3. **Direct Consequence:** Each item (except the first, which should be treated "
                "as a constant) must arise directly from the preceding item, explicitly indicating "
                "the cause-and-effect relationship showing progression.",
            },
        )
        # TODO Provide an example
        # Provide the success criteria
        messages.append(
            {
                "role": "user",
                "content": "**Success Criteria:** Create a fictional story that seamlessly "
                "connects these disparate elements and weaving the items together.",
            },
        )
        # Provide the user input list of items
        messages.extend(
            {"role": "user", "content": f"Item {i + 1}: {item}"}
            for i, item in enumerate(self.__get_user_input())
        )
        messages.append({"role": "user", "content": "Start your narrative now."})
        return messages

    def __get_user_input(self):
        """Get user input to generate a story."""
        return input("Enter a comma separated list of items for the story: ").split(",")


if __name__ == "__main__":
    StoryTeller().generate_story()

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
