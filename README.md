# Job Listing Scraper (Practice Version)

A beginner web scraper that collects listings from a public website, extracts
four fields per listing, and saves them to a CSV file. It is built on
[quotes.toscrape.com](https://quotes.toscrape.com/), a site made for scraping
practice, and designed to show how the same method could track competitor job
postings for HR teams.

## Why it matters

HR managers at mid-size companies monitor competitor job postings to see which
skills are in demand and what salaries are offered. Doing this by opening pages
one at a time is slow. This tool automates the collection and delivers a
spreadsheet.

## Fields collected

| Column | Practice site meaning | Job board equivalent |
|---|---|---|
| text | Quote text | Job title |
| author | Author name | Company |
| tags | Topic tags (joined with commas) | Required skills |
| author_link | Author page URL | Listing URL |

## Tools used

- Python 3
- `requests` (downloads web pages)
- `beautifulsoup4` (finds data inside HTML)
- `csv` and `time` (built into Python)

## Setup

1. Install Python 3.
2. Create and activate a virtual environment:
   - Windows: `python -m venv venv`, then `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv`, then `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

## How to run

```
python scrape_all.py
```

The script visits each page in turn, waits 1 second between requests, follows
the "Next" button until there are no more pages, and writes the results to
`quotes.csv`.

## Output

`quotes.csv` contains a header row and one row per listing. On the practice
site this should be about 100 rows and 4 columns. The file opens in Excel or
Google Sheets. If curly quotes look garbled in Excel, use Data > From Text/CSV
and choose UTF-8.

## How the script works

1. `parse_quote()` turns one listing's HTML into a dictionary with four fields.
2. `scrape_all_pages()` downloads each page, applies `parse_quote()` to every
   listing, and follows the "Next" link until none remains.
3. `save_to_csv()` writes the list of dictionaries to a CSV file.

Safety settings at the top of the script: `DELAY_SECONDS` (pause between
requests) and `MAX_PAGES` (a cap so the loop can never run forever).

## Adapting this for a live jobs board

If a client gave me access to a live jobs board, I would not start by writing
code. I would first confirm in writing what I am allowed to collect, then
inspect the site's structure before changing anything.

1. **Confirm permission and terms.** Get the client's written confirmation of
   what they are authorised to access, and read the board's terms of use.
2. **Look for an official API or data export.** If one exists, use it instead
   of scraping. It is more reliable and clearly permitted.
3. **Inspect the page.** Use right-click > Inspect to find the tags and classes
   for job title, company, location, salary, skills, date posted, and link.
4. **Check whether the data is in the HTML.** Use "View Page Source". If job
   titles are missing there, the page loads them with JavaScript, and
   `requests` will not see them. I would then look for a data feed or use
   browser automation (not covered in this project).
5. **Update the settings and selectors.** Change `base_url` and the tag and
   class names inside `parse_quote()`.
6. **Add the new fields.** Add salary, location, and date posted to
   `parse_quote()` and to `fieldnames` in `save_to_csv()`.
7. **Handle missing data.** Many listings hide the salary. Currently, calling
   `.get_text()` on a missing tag crashes the script. I would check first:

   ```python
   salary_tag = listing.find("span", class_="salary")
   salary = salary_tag.get_text(strip=True) if salary_tag else ""
   ```

8. **Update pagination.** Some boards use `?page=2` in the URL instead of a
   "Next" button, so the page-following logic would change.
9. **Store any login details safely.** If the client provides credentials,
   keep them in environment variables, never in the code or on GitHub.
10. **Stay polite.** Keep the delay and the page cap, and identify the scraper
    honestly if the board asks for this.
11. **Test small first.** Set `MAX_PAGES = 2`, check the CSV, then run the full job.
12. **Plan for maintenance.** Sites change their layout, so scrapers break.
    Weekly runs need monitoring and occasional fixes.

## Ethical and legal checks before scraping

I am not a lawyer. These are the checks I would make first, and I would ask
the client to confirm the legal position with their own adviser.

- **Terms of service.** Do the site's terms forbid automated collection? If
  so, I would ask the owner for permission or an official data feed instead.
- **robots.txt.** Read `sitename.com/robots.txt` and respect the paths it asks
  automated tools to avoid.
- **Authorisation.** Being given a login does not automatically mean
  automated collection is allowed. I would confirm this in writing.
- **Personal data.** Listings may include recruiter names, emails, or phone
  numbers. Kenya's Data Protection Act, 2019 regulates personal data, so I
  would collect only company-level job information (title, skills, salary
  range, location) and skip personal details.
- **Unauthorised access.** Kenya's Computer Misuse and Cybercrimes Act, 2018
  covers access to systems without authorisation. I would never bypass logins,
  CAPTCHAs, or blocks.
- **Copyright.** Facts such as job titles and salary ranges are different from
  copying a site's full text or database. I would not republish a board's content.
- **Server load.** Keep delays and page caps so the site is not strained.
- **Purpose and storage.** Know what the data is for, store it securely, and
  delete what is not needed.
- **Written agreement.** Agree in a contract what is collected, what is not,
  and who is responsible for compliance.
- **Other countries.** If the client or the board is based elsewhere, check
  that country's rules too.

## Pricing note

These are proposed rates for an HR consultancy that wants a weekly competitor
job-postings report. They are estimates based on expected hours and would be
confirmed after I inspect the client's job board. The figures below use an
illustrative rate of KES 2,000 per hour.

### One-time setup fee: KES 20,000 (about 10 hours)

Includes:
- Permission and terms check for the target job board
- Inspecting the site and agreeing the fields to collect
- Adapting the scraper to the board's layout, including missing-data handling
- Testing, then a first full run
- Designing the weekly report format
- A short user guide

### Monthly retainer: KES 16,000 per month (about 8 hours)

Includes:
- One scrape per week (4 per month)
- Data checking and cleaning
- A clean weekly CSV report delivered by email
- Monitoring, and fixes if the site's layout changes
- Up to 1 hour per month of small change requests

### Not included (quoted separately)

- Additional job boards
- Extra fields beyond those agreed
- Boards that need browser automation, logins, or CAPTCHA handling
- Analysis or written recommendations beyond the report

### Assumptions

- The client confirms they are permitted to access the board.
- Prices exclude any taxes.
- Either party may cancel with one month's notice.
- Final prices are confirmed after I inspect the board.

## Limitations

- Built for one specific page layout. If the site changes, the script must be updated.
- Does not handle pages that load data with JavaScript.
- Does not handle logins or CAPTCHAs.
- This is a prototype. A client-ready version would add error logging, dated
  filenames, and monitoring.

## Project files

- `scrape_all.py`: the scraper
- `requirements.txt`: the libraries to install
- `quotes.csv`: sample output
- `README.md`: this file