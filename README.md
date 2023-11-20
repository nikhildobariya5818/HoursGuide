# Web Scraping Project

This project consists of several Python scripts designed to perform web scraping tasks to gather data from `https://www.hoursguide.com/` websites. The project is organized into different components, each serving a specific purpose. Below is an overview of the components and how to run them.

## Components

1. **get_shopping.py**: This script fetches shopping-related data from websites. It scrapes product information and URLs. The data is stored in a local database for further analysis.

2. **get_states.py**: This script extracts data about different states, including information about their cities and shopping opportunities. It also saves the data to a local database for future reference.

3. **get_City.py**: This component is responsible for collecting data about cities. It scrapes city-related information and shopping details and stores it in a database.

4. **get_shop.py**: This script focuses on gathering data about various shops. It scrapes shop-related URLs and details, which are saved in a local database.

5. **get_data.py**: The final component compiles and processes the data from the previous steps. It performs data analysis, transformations, and generates insights from the collected information.

6. **interface_class.py**: Contains classes and functions related to interfacing with web browsers using Selenium and configuring browser options. It supports proxy usage for web scraping tasks.

7. **helper_class.py**: This script includes a set of utility functions for tasks like file handling, HTTP requests, data processing, and more. It's a shared library across all components.

8. **proxy_interface.py**: This script is responsible for managing proxy configurations for web scraping. It connects to the Webshare.io API to obtain proxies for use in web scraping tasks.

9. **main.py**: The main script to execute the entire project. It orchestrates the execution of each component in the correct order.

## Getting Started

Follow these steps to get started with the project:

### Prerequisites

- Python: Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

- Required Libraries: Install the necessary Python libraries by running the following command:

  ```bash
  pip install -r requirements.txt
  ```

## Execution

1. Clone or download this repository to your local machine.

2. Open a terminal or command prompt and navigate to the directory containing the script.

3. Edit the configuration and URLs in each script to match your specific requirements. You may need to customize these based on the websites you want to scrape.

4. You can customize the download directories, file formats, and database connections as needed for your specific use case.

5. Run the main script to execute the entire project:
 ```bash
 python main.py
 ```

6. Choose an Option: After running the main script, you'll be prompted with a menu to select an option:

    - Select 1 to start scraping data. You can then choose a category to scrape. The available categories include Accessories, Apparel, Arts & Crafts, Automotive, Banks, Beauty & Health, Bookstores, Dental & Hospital, Drug Stores, Electronics, Entertainment, Express & Transport, Gas Stations, Grocery & Market, Hair Salons, Home & Garden, Insurance & Finance, Other Services, Outlets, Pets, Printing, Real Estate, Shoes, Shopping, Sports, Toys & Gifts, and Travel & Lodging.

    - Select 2 to clear the database, removing all existing data.

Each component will run sequentially, collecting data and storing it in a local SQLite database.

Cleare the database before starting new category

## Customization

1. Modify database configurations, data processing logic, and output formats to suit your project requirements.

2. Handle exceptions and errors as needed for your specific use case to ensure robust operation in a production environment.