
# Job Description Crawler Bot

This project is designed to automate the process of:

1. **Crawling job descriptions** from LinkedIn and Indeed.
2. **Extracting keywords** from the job descriptions.
3. **Displaying the results** on a Streamlit dashboard.

## Project Overview

The bot is built to streamline the job search process by automatically gathering and analyzing job descriptions from popular job boards. The primary goals of the project are:

- **AWS Infrastructure**: 
  - Built using ECS and Docker containers.
  - Implemented a microservices architecture.
  - Managed scheduling, storage, and network setup.

- **NLP with OpenAI API**: 
  - Analyzed and extracted relevant keywords from job descriptions using OpenAI's API.

## Current Limitations

While the bot is functional, it faces a few significant challenges:

- **LinkedIn Restrictions**: LinkedIn actively blocks AWS IP addresses, which affects the bot's reliability. Implementing a proxy server could bypass these restrictions, but it would also increase operational costs.
- **Inefficient Job Search Strategy**: Despite automating the process, the current approach may not be the most effective strategy for job hunting.

## Future Considerations

- Explore alternative methods to bypass LinkedIn's restrictions, such as using residential proxies.
- Reevaluate the job search strategy to improve efficiency and results.
- Optimize the cost-effectiveness of the bot's infrastructure.
