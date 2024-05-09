from time import sleep

from aibot import instagram_comment_from_script
from selenium_helpers import start_chrome, initialize_driver, login, post_comment, like_post
from transcriber import transcribe_link


def main():
    start_chrome()
    driver = initialize_driver()
    login(driver)

    # Get multiple video links from the user
    links_input = input("Please enter video links for transcription, separated by commas: ")
    video_links = [link.strip() for link in links_input.split(',')]
    language_key = input("Please enter the language key (e.g., EN, AR): ")

    for video_link in video_links:
        try:
            transcription_text = transcribe_link(video_link, language_key)
            print(f"Transcription Text: {transcription_text}")
            ai_comment = instagram_comment_from_script(transcription_text)
            print(f"AI Comment: {ai_comment}")
            post_comment(driver, video_link, ai_comment)
            sleep(3)
            like_post(driver, video_link)
        except Exception as e:
            print(f"An error occurred while processing {video_link}: {e}")
        input('Press enter to go to next post.')

    input("Press Enter to close the browser...")
    driver.quit()


if __name__ == "__main__":
    main()
