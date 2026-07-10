To demonstrate a complete data mining workflow, I present an empirical example: extracting data from the World Bank website (https://data.worldbank.org/indicator). The data processing workflow involves multiple steps and the selection of supporting tools; the implementation diagram is as follows:
<img width="373" height="443" alt="image" src="https://github.com/user-attachments/assets/84a9b751-b0f4-41b1-85f7-d3bb83dc1ef5" />

The report covers the following topics:
1.	Introduction to the website https://data.worldbank.org/indicator and the available data.
2.	Data scraping.
3.	Data transformation and loading process.
4.	Using Airflow.
5.	SQL querying and data visualization using InfluxDB.

II.	WEB WORLDBANK AND DATA

![image](https://github.com/user-attachments/assets/6bc8931c-4d92-4299-8cde-58d584bbd2ed)<br>
The data provided by the World Bank has been collected over the past 50 years, covering a wide range of topics such as finance, business, health, economics, and human development. Users can currently access over 7,000 development indicators.<br>
The "Indicators" page lists 331 indicators from the World Development Indicators (WDI) dataset in alphabetical order. Each year, the World Bank compiles development data from its own primary sources and other globally recognized sources to create the WDI dataset. This serves as a tool for assessing the development progress of economies.<br>
These figures tell the stories of people in emerging and developing nations, thereby contributing to efforts to alleviate poverty.<br>
For this final project, I will utilize data from this "Indicators" page to perform analysis and visualize the information through a desktop application.<br>

III.	ETL Process<br>

III.1.	Extract

Web data extraction is performed using a Python script named `scraping.py`, utilizing the `urllib` and XPath libraries. The data is saved to a local folder.

<img width="469" height="477" alt="image" src="https://github.com/user-attachments/assets/dbfbd3b0-4350-4ce6-b379-cf702bab62a3" />

III.2.	Transform - Load

The transform-load process consists of three steps:

                Upzip     =>    Cleaning    =>      Processing
                
The downloaded data consists of .zip files organized into folders by indicator:
 
![image](https://github.com/user-attachments/assets/083aaeb2-46e2-4502-b906-f753454745df)


Next, we need to process this file to extract the following data:
•	Last Update Date
•	Country Name
•	Country Code
•	Indicator Name
•	Indicator Code
•	Years
•	Values
Using this dataset, we process and load the data into the InfluxDB database via a Python script named `upload.py`. The data is formatted according to InfluxDB's specific requirements.

![image](https://github.com/user-attachments/assets/b95720dc-1181-4160-ae1e-80412dda5fe9)

IV.	AIRFLOW

Python scripts can run independently; however, web data extraction requires frequent updates and the execution of tasks either sequentially or in parallel, necessitating a specific schedule and setup for each task's runtime. Apache Airflow is a useful tool for this purpose.

While all the developed tasks could potentially run in parallel, the scraping task is time-consuming, so it is assigned to its own dedicated DAG, with the scheduler configured to run it once a day.

The remaining tasks are grouped into a second DAG designed for sequential execution, with the scheduler set to run on a minute-by-minute basis. After each task completes, data in the input directory is deleted to prevent data overlap.

Consequently, upon task completion, new folders are created, but they remain empty.
<img width="469" height="259" alt="image" src="https://github.com/user-attachments/assets/674c2827-c3e9-4596-9462-7995e0aa3126" /><br>
![image](https://github.com/user-attachments/assets/7e464999-2f18-45dc-a7b5-8c5da40c494b)<br>
![image](https://github.com/user-attachments/assets/e8730726-0e57-4e16-8f12-344f0417d994)<br>
Tasks are defined using Python code located in the dags folder of the Airflow directory:<br>
![image](https://github.com/user-attachments/assets/7ae5febd-fbb2-4899-a5fb-09465e14df68)

V.	Querying SQL and Displaying Data Using InfluxDB

InfluxDB is a popular time-series database. This report utilizes version 1.8.9. Queries in InfluxDB are performed using an SQL-like language. Although InfluxDB has since evolved to version 2.0—shifting to a NoSQL-style query language—the format of the data input into the program remains unchanged.

![image](https://github.com/user-attachments/assets/f58ca8ee-d542-435e-9bfe-bb921d8c5f6f)

Compared to other database systems, InfluxDB does not offer a wide variety of chart types, as it is primarily designed for visualizing time-series data, including:

![image](https://github.com/user-attachments/assets/7d1ad357-3cac-4b37-8e00-8081f9e2bf58)

This is the program interface for selecting the data to display.

![image](https://github.com/user-attachments/assets/ced37147-6c66-4537-8973-2d4bcb3779fc)

Here is an example dashboard based on data from the World Bank website:

![image](https://github.com/user-attachments/assets/63a164e5-4ab7-41cb-8ae9-d909766042ee)

VI.	CONLUSION

At this stage, the data processing phase can be considered complete. We can proceed to analyze the data in greater detail. The choice of InfluxDB for this study was not entirely suitable; while InfluxDB is excellent for ingesting streaming data from IoT devices, visualizing time-series data, and assessing system performance, the data in this report might be better served by a different database system for visualization purposes.







