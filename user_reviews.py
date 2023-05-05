from bs4 import BeautifulSoup
import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}

index = 0

user_review_page = requests.get(
    f"https://www.metacritic.com/game/playstation-4/middle-earth-shadow-of-mordor/user-reviews?page={index}",
    timeout=10,
    headers=headers,
).text

parser = BeautifulSoup(user_review_page, "lxml")

last_page_number = int(parser.find_all("li", class_="page")[-1].find("a").text)
print(last_page_number)


# Testing on Middle-Earth: Shadow of Mordor

with open("test.txt", "a", encoding="utf-8") as f:
    while index != last_page_number:
        try:
            user_reviews_text = requests.get(
                f"https://www.metacritic.com/game/playstation-4/middle-earth-shadow-of-mordor/user-reviews?page={index}",
                timeout=10,
                headers=headers,
            ).text

            parser = BeautifulSoup(user_reviews_text, "lxml")

            # First Review
            first_review = parser.find(
                "li", class_="review user_review first_review")
            first_user_name = first_review.find("div", class_="name").text
            first_user_score = first_review.find(
                "div", class_="review_grade").text
            first_date = first_review.find("div", class_="date").text
            first_helpfulratio_numerator = first_review.find(
                "span", class_="total_ups"
            ).text
            first_helpfulratio_denominator = first_review.find(
                "span", class_="total_thumbs"
            ).text
            f.write(f"Username: {first_user_name.strip()}\n")
            f.write(f"User Score: {first_user_score.strip()}\n")
            f.write(f"Date: {first_date.strip()}\n")
            f.write(
                f"Helpful Ratio Numerator: {first_helpfulratio_numerator.strip()}\n"
            )
            f.write(
                f"Helpful Ratio Denominator: {first_helpfulratio_denominator.strip()}\n"
            )

            first_review_text = (
                first_review.find("div", class_="review_body")
                .text.replace("\n", "")
                .strip()
            )
            if "Expand" in first_review_text:
                first_review_expanded_text = (
                    parser.find("li", class_="c")
                    .find("div", class_="review_body")
                    .find("span", class_="blurb blurb_expanded")
                    .text.replace("\n", "")
                    .strip()
                )
                f.write(f"User Review: {first_review_expanded_text}\n\n")
            else:
                f.write(f"User Review: {first_review_text}\n\n")

            # Middle Reviews
            middle_reviews = parser.find_all("li", class_="review user_review")

            for review in middle_reviews:
                user_name = review.find("div", class_="name").text
                user_score = review.find("div", class_="review_grade").text
                date = review.find("div", class_="date").text
                helpfulratio_numerator = review.find(
                    "span", class_="total_ups").text
                helpfulratio_denominator = review.find(
                    "span", class_="total_thumbs"
                ).text

                f.write(f"Username: {user_name.strip()}\n")
                f.write(f"User Score: {user_score.strip()}\n")
                f.write(f"Date: {date.strip()}\n")
                f.write(
                    f"Helpful Ratio Numerator: {helpfulratio_numerator.strip()}\n")
                f.write(
                    f"Helpful Ratio Denominator: {helpfulratio_denominator.strip()}\n"
                )

                middle_review_text = (
                    review.find("div", class_="review_body")
                    .text.replace("\n", "")
                    .strip()
                )
                if "Expand" in middle_review_text:
                    middle_expanded_text = (
                        review.find("span", class_="blurb blurb_expanded")
                        .text.replace("\n", "")
                        .strip()
                    )
                    f.write(f"User Review: {middle_expanded_text}\n\n")
                else:
                    f.write(f"User Review: {middle_review_text}\n\n")

            # Last Review
            last_review_text = (
                parser.find("li", class_="review user_review last_review")
                .find("div", class_="review_body")
                .text.replace("\n", "")
                .strip()
            )
            if "Expand" in last_review_text:
                last_review_expanded_text = (
                    parser.find("li", class_="review user_review last_review")
                    .find("div", class_="review_body")
                    .find("span", class_="blurb blurb_expanded")
                    .text.replace("\n", "")
                    .strip()
                )
                f.write(f"User Review: {last_review_expanded_text}\n\n")
            else:
                f.write(f"User Review: {last_review_text}\n\n")

            index += 1

        except Exception as e:
            print(f"An error occurred on page {index}: {e}. Stopping...")
            break
