# pytest library
import pytest

import re

from ingredient_slicer import _utils

# -------------------------------------------------------------------------------
# ---- Test utils._remove_emojis(): Removes emojis from strings... ----
# -------------------------------------------------------------------------------

emoji_ingredients = [
    "🥕 2 carrots, chopped",
    "🍅 3 tomatoes, diced",
    "🧄 4 cloves of garlic, minced",
    "🥬 1 head of lettuce, shredded",
    "🥒 2 cucumbers, sliced",
    "🍚 1 cup of rice",
    "🥩 500g of beef, sliced",
    "🍞 2 slices of bread",
    "🧀 100g of cheese, grated",
    "🍓 200g of strawberries",
    "🍌 3 bananas",
    "🍗 2 chicken breasts",
    "🥛 1 liter of milk",
    "🧈 100g of butter",
    "🥔 5 potatoes, peeled and cubed",
    "🍏 4 green apples, sliced",
    "🍤 200g of shrimp",
    "🍋 1 lemon, juiced",
    "🥖 1 baguette, sliced",
    "🍫 100g of dark chocolate, chopped"
]

# def test_remove_emojis():
#     _utils._remove_emojis("🥕 2 carrots, chopped") == " 2 carrots, chopped"


# # Credit: https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
# # Stackoverflow user: https://stackoverflow.com/users/4279/jfs
# @pytest.mark.parametrize("ingredient", emoji_ingredients)
# def test_remove_emojis(ingredient):
    
#     assert _utils._remove_emojis(ingredient) == re.sub(r"\p{So}", "", ingredient)
