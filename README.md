# Real-Time News

Welcome to the "Real-Time News" project! This project is a news fetching and formatting tool that provides real-time news updates based on a specified search query. It uses an API to fetch news articles, formats them, and outputs them to the console.

## Features

- Fetches news articles from a specified API based on a search query.
- Formats the news articles into a tabulated format for easy reading.
- Outputs the formatted news to the console.
- Can run continuously to fetch news at regular intervals.

## Components

### 1. `OutputStrategy` Protocol

This is an interface that defines the `output` method, which should be implemented by output strategies.

### 2. `ConsoleOutputStrategy` Class

This class implements the `OutputStrategy` interface and defines the `output` method, which outputs the formatted news to the console in a tabulated format.

### 3. `NewsFetcher` Class

This class handles fetching news articles from an API using a specified search query. It uses the `requests` library's session to make HTTP requests and parses the JSON response to retrieve news articles.

### 4. `NewsFormatter` Class

This class formats the fetched news articles into a list of dictionaries. Each dictionary represents a news article with keys for "Author," "Title," "Description," and "Link."

### 5. `main` Function

The main function orchestrates the process of fetching, formatting, and outputting news:

- Retrieves the search query from command-line arguments.
- Initializes the `NewsFetcher` and fetches news articles.
- If there are news articles, it formats them using the `NewsFormatter`.
- Outputs the formatted news using the `ConsoleOutputStrategy`.

## Usage

To use this project, follow these steps:

1. Set up your environment variables using a `.env` file. Specify the API URL and API token for accessing the news API.
    ```
    NEWS_API_URL=https://newsapi.org/v2/everything
    NEWS_API_TOKEN=your_api_token
    ```

2. Install the required Python packages from the `requirements.txt` file:
    ```
    pip install -r requirements.txt
    ```

3. Run the script using a search query for news:
    ```
    python real_time_news.py --search_for "your_search_query"
    ```

4. The script will fetch news based on the specified search query and output it to the console.

## Scheduling

The script uses the `schedule` library to run the `main` function at regular intervals. The interval can be adjusted by modifying the schedule in the script:

- `schedule.every(30).seconds.do(main, args)` runs the function every 30 seconds (useful for testing).
- You can change the interval to minutes or hours as desired (e.g., `schedule.every(30).minutes.do(main, args)`).

## Logs

The script logs information and errors to a file named `app.log` and also prints them to the console.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
