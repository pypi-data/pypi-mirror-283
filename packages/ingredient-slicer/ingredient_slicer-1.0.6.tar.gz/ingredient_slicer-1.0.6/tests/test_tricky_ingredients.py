# # pytest library
# import pytest

# import re

# from ingredient_slicer import IngredientSlicer

# # -------------------------------------------------------------------------------
# # ---- Test IngredientSlicer: Fraction words tests ----
# # -------------------------------------------------------------------------------

# # Github Issue: https://github.com/anguswg-ucsb/ingredient-slicer/issues/6
# tricky_ingredients = [
#     " ▢ 1 cup warm water (105 degrees f), warm water, 105, cup, cup,",
#     "1 10-ounce bag frozen cherries, cherries, 10, ounce, ounce,"
# ]

# # Credit: https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
# # Stackoverflow user: https://stackoverflow.com/users/4279/jfs
# def _remove_emojis(s):
#     """Remove emojis from a string
#     Args:
#         s: str, string from which to remove emojis
#     Returns:
#         str: string with emojis removed
#     """
    
#     if s is None or s == "":
#         return ""
    
#     emoj = re.compile("["
#         u"\U0001F600-\U0001F64F"  # emoticons
#         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#         u"\U0001F680-\U0001F6FF"  # transport & map symbols
#         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#         u"\U00002500-\U00002BEF"  # chinese char
#         u"\U00002702-\U000027B0"
#         u"\U000024C2-\U0001F251"
#         u"\U0001f926-\U0001f937"
#         u"\U00010000-\U0010ffff"
#         u"\u2640-\u2642" 
#         u"\u2600-\u2B55"
#         u"\u200d"
#         u"\u23cf"
#         u"\u23e9"
#         u"\u231a"
#         u"\ufe0f"  # dingbats
#         u"\u3030"
#                     "]+", re.UNICODE)
#     return re.sub(emoj, '', s)


# @pytest.mark.parametrize("ingredient", tricky_ingredients)
# def test_tricky_ingredients(ingredient):
#     ingredient = tricky_ingredients[0]
#     _remove_emojis(ingredient)
#     parse = IngredientSlicer(ingredient)
#     # parse.parse()
#     parsed = parse.to_json()
#     parsed
#     assert parsed['quantity'] == "1.0"
#     assert parsed['unit'] == 'cup'
#     assert parsed['standardized_unit'] == "cup"

#     assert parsed['secondary_quantity'] == None
#     assert parsed['secondary_unit'] == None
#     assert parsed['standardized_secondary_unit'] == None

#     assert parsed['is_required'] == True

#     assert parsed['prep'] == []
#     assert parsed['food'] == 'warm water'
#     assert parsed['size_modifiers'] == []