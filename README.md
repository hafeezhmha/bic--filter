# BIC Event Filter

This project contains a Python script that fetches an iCalendar feed from the Bangalore International Centre (BIC), filters the events based on keywords, and saves the result to a new iCalendar file. This is useful for subscribing to a calendar of BIC events that only includes performances of Western classical music and related genres.

## How It Works

The script `filter_bic.py` performs the following actions:

1.  **Fetches** the event calendar from a predefined BIC iCalendar feed URL.
2.  **Parses** the calendar data.
3.  **Filters** events based on a set of inclusion and exclusion keywords in the event's summary and description.
    -   **Inclusion keywords**: `jazz`, `orchestra`, `symphony`, `ballet`, `mozart`, `beethoven`, `choir`, `musical`.
    -   **Exclusion keywords**: `bharatanatyam`, `kuchipudi`, `kathak`, `odissi`, `carnatic`, `hindustani`, `raag`, `tabla`, `mridangam`, `sitar`.
4.  **Saves** the filtered events to a new iCalendar file named `bic_filtered.ics`.
5.  **Logs** the included and excluded events in `log.md` with a timestamp.

If the script fails to fetch or parse the feed, it will keep the existing `bic_filtered.ics` file to avoid breaking calendar subscriptions. It also won't overwrite the file if no matching events are found.

## Automated Updates

A GitHub Actions workflow is set up in `.github/workflows/update.yml` to run the script automatically.

-   The workflow runs **daily at 3 AM UTC**.
-   It can also be triggered manually.
-   The workflow checks out the repository, sets up Python, installs dependencies, and runs the script.
-   If `bic_filtered.ics` or `log.md` are updated, the changes are automatically committed and pushed to the repository.

## Usage

### Subscribing to the Calendar

You can subscribe to the filtered calendar feed using the following URL:

```
https://raw.githubusercontent.com/USERNAME/REPOSITORY/main/bic_filtered.ics
```

Replace `USERNAME` and `REPOSITORY` with the correct GitHub username and repository name.

### Manual Setup and Execution

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/USERNAME/REPOSITORY.git
    cd REPOSITORY
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the script:**
    ```bash
    python filter_bic.py
    ```

This will generate `bic_filtered.ics` and update `log.md`.

## Files

-   `filter_bic.py`: The main Python script for filtering events.
-   `requirements.txt`: A list of Python dependencies required to run the script.
-   `bic_filtered.ics`: The output iCalendar file with the filtered events.
-   `log.md`: A log file that records which events were included or excluded on each run.
-   `.github/workflows/update.yml`: The GitHub Actions workflow for automated execution.
