import pandas as pd


def convert_to_minutes(time_str):
    """
    Converts a time duration string into the total number of minutes.

    Parameters:
    ----------
    time_str : str
        A string representing the time duration.

    Returns:
    -------
    int or None
        The total time converted into minutes as an integer. Returns None if the input is NaN.
    """
    if pd.isna(time_str):
        return None  # Keep NaN if missing
    # Extend time_map to handle singular and plural forms, including days
    time_map = {"day": 1440, "days": 1440, "hr": 60, "hrs": 60, "min": 1, "mins": 1}
    
    # Split the time string into parts and calculate total minutes
    time_parts = time_str.split()
    return sum(int(num) * time_map[unit] for num, unit in zip(time_parts[:-1:2], time_parts[1::2]))


def get_random_recipes(df, max_results):
    """
    Selects a random subset of recipes from the provided DataFrame.

    Parameters:
    ----------
    df : pd.DataFrame
        The DataFrame containing recipe data.
    max_results : int
        The maximum number of recipes to return.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing a random subset of recipes, up to `max_results`.
    """
    return df.sample(n=min(max_results, len(df)))


def filter_by_preferences(ingredients, df):
    """
    Filters recipes based on the provided ingredient preferences.

    Parameters:
    ----------
    ingredients : str
        A comma-separated string of desired ingredients.
    df : pd.DataFrame
        The DataFrame containing recipe data.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing recipes that match at least one of the preferred ingredients.
    """
    ingredient_list = [item.strip().lower() for item in ingredients.split(',')]
    mask = df.apply(
        lambda row: all(
            keyword in (row['ingredients'] or "").lower() or
            keyword in (row['title'] or "").lower() or
            keyword in (row['category'] or "").lower()
            for keyword in ingredient_list
        ),
        axis=1
    )
    return df[mask]


def exclude_restricted_items(restrictions, df):
    """
    Excludes recipes containing restricted ingredients.

    Parameters:
    ----------
    restrictions : str
        A comma-separated string of restricted ingredients.
    df : pd.DataFrame
        The DataFrame containing recipe data.

    Returns:
    -------
    pd.DataFrame
        A DataFrame excluding recipes with any of the restricted ingredients.
    """
    restricted_list = [item.strip().lower() for item in restrictions.split(',')]
    mask = ~df.apply(
        lambda row: any(
            restricted in (row['ingredients'] or "").lower() or
            restricted in (row['title'] or "").lower() or
            restricted in (row['category'] or "").lower()
            for restricted in restricted_list
        ),
        axis=1
    )
    return df[mask]


def apply_dietary_restrictions(dietary_preferences, df):
    """
    Filters recipes based on dietary preferences (e.g., vegan, vegetarian, gluten-free).

    Parameters:
    ----------
    dietary_preferences : list of str
        A list of dietary preference terms.
    df : pd.DataFrame
        The DataFrame containing recipe data.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing recipes that match all specified dietary preferences.
    """
    if not dietary_preferences:
        return df

    dietary_terms = [pref.lower() for pref in dietary_preferences]
    mask = df.apply(
        lambda row: all(
            term in (row['title'] or "").lower() or term in (row['category'] or "").lower()
            for term in dietary_terms
        ),
        axis=1
    )
    return df[mask]


def filter_by_ranges(df, calorie_min, calorie_max, protein_min, protein_max, fat_min, fat_max, carbs_min, carbs_max, max_time):
    """
    Filters recipes based on numeric ranges for calories, protein, fat, carbs, and cooking time.

    Parameters:
    ----------
    df : pd.DataFrame
        The DataFrame containing recipe data.
    calorie_min : int or None
        The minimum calorie value.
    calorie_max : int or None
        The maximum calorie value.
    protein_min : int or None
        The minimum protein value (grams).
    protein_max : int or None
        The maximum protein value (grams).
    fat_min : int or None
        The minimum fat value (grams).
    fat_max : int or None
        The maximum fat value (grams).
    carbs_min : int or None
        The minimum carbohydrate value (grams).
    carbs_max : int or None
        The maximum carbohydrate value (grams).
    max_time : int or None
        The maximum cooking time (minutes).

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing recipes that meet all specified numeric criteria.
    """
    if calorie_min is not None:
        df = df[df['calories'] >= calorie_min]
    if calorie_max is not None:
        df = df[df['calories'] <= calorie_max]
    if protein_min is not None:
        df = df[df['protein'] >= protein_min]
    if protein_max is not None:
        df = df[df['protein'] <= protein_max]
    if carbs_min is not None:
        df = df[df['carbs'] >= carbs_min]
    if carbs_max is not None:
        df = df[df['carbs'] <= carbs_max]
    if fat_min is not None:
        df = df[df['fat'] >= fat_min]
    if fat_max is not None:
        df = df[df['fat'] <= fat_max]
    if max_time is not None:
        df = df[df['total_time_mins'] <= max_time]
    return df


def convert_rating_to_stars(rating):
    """
    Converts a numeric rating into a visual representation of stars (★, ☆).

    Parameters:
    ----------
    rating : float or str
        The numeric rating to convert (e.g., 4.5).

    Returns:
    -------
    str
        A string of stars representing the rating.
        Returns "No Rating" for invalid inputs.
    """
    try:
        rating = float(rating)
        full_stars = int(rating)  # Number of full stars
        half_star = 1 if (rating - full_stars) >= 0.5 else 0  # Check for half-star
        empty_stars = 5 - full_stars - half_star  # Remaining empty stars
        return "★" * full_stars + "☆" * empty_stars + ("½" if half_star else "")
    except (ValueError, TypeError):
        return "No Rating"