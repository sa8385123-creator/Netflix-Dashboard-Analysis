# Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as ssn
import time

# Loading Data set
print("Loading Dataset, please wait .......\n")
time.sleep(1)
netflix_data=pd.read_csv(r"D:\Coding\Python Project\Seaborn\NetFlix\netflix_titles.csv")
print("Data Loaded Successfully\n")

# Inspecting Dataset
print("Date is being inspecting For Cleaning ......\n")
time.sleep(1)
print(netflix_data.head(10))
netflix_data.info()
print(netflix_data.isnull().sum())
print(netflix_data.duplicated().sum())
print("Data Inspection Completed Successfully\n")

# cleaning dataset
print("Data is cleaning now so wait .......\n")
time.sleep(1)
# Droping Missing Values in dataset
netflix_clean_data=netflix_data.dropna(subset=["show_id","type","title"])
# Filling missing values in dataset
netflix_clean_data=netflix_clean_data.fillna({
    "director" : "Unknown",
    "cast"     : "Unknown",
    "country":netflix_clean_data["country"].mode()[0],
    "date_added":netflix_clean_data["date_added"].mode()[0],
    "release_year":netflix_clean_data["release_year"].mean(),
    "rating"    : netflix_clean_data["rating"].mode()[0],
    "duration" : netflix_clean_data["duration"].mode()[0],
    "listed_in" : "Unknown",
    "description" : "None"
})

# Removing Duplicate rows
netflix_clean_data=netflix_clean_data.drop_duplicates()

mask = netflix_clean_data["rating"].str.contains("min", na=False)
netflix_clean_data.loc[mask, "duration"] = netflix_clean_data.loc[mask, "rating"]
netflix_clean_data.loc[mask, "rating"] = pd.NA
netflix_clean_data["rating"] = netflix_clean_data["rating"].fillna(
    netflix_clean_data["rating"].mode()[0]
)

# checking Datatypes
print("Now checking Datatypes.....\n")
time.sleep(1)
print(netflix_clean_data.dtypes)

# Convert wrong Data types to correct data types
print("Correcting Data types....")
time.sleep(1)
netflix_clean_data["date_added"] = netflix_clean_data["date_added"].str.strip()

netflix_clean_data["date_added"] = pd.to_datetime(
    netflix_clean_data["date_added"],
    format="%B %d, %Y"
)
print("Datatypes corrected Successfully")

print("Data is cleaned now\n")
# Exporting cleaned Data
#netflix_clean_data.to_csv("netflix_clean_data.csv",index=False)
print("Clean CSV file is stored in your current folder with \'netflix_clean_data.csv\'")

# Building Dashboard

print("Your Dashboard is ready")
plt.figure(figsize=(18,10))
plt.figure(figsize=(18,10))
manager = plt.get_current_fig_manager()
manager.window.state("zoomed")
plt.suptitle("NETFLIX DASHBOARD ANALYSIS",fontsize=20,fontweight="bold",y=1)

total_titles = len(netflix_clean_data)
movies = (netflix_clean_data["type"]=="Movie").sum()
tvshows = (netflix_clean_data["type"] == "TV Show").sum()

plt.figtext(
    0.02, 0.91,
    f"Total Titles : {total_titles}\nMovies : {movies}\nTV Shows : {tvshows}",
    fontsize=12,
    bbox=dict(facecolor="lightyellow", edgecolor="black", boxstyle="round")
)

# Movies VS TV Shows
ssn.set_theme(style="whitegrid")
plt.subplot(3,2,1)
num=netflix_clean_data["type"].value_counts()
plt.pie(num,autopct="%1.1f%%",shadow=True,startangle=90,labels=num.index)
plt.title("Distribution of Netflix Content")
plt.xlabel("")

# Rating
plt.subplot(3,2,2)
ssn.countplot(
    data=netflix_clean_data,
    y="rating",
    order=netflix_clean_data["rating"].value_counts().index,
    palette="Set2",
    edgecolor="black"

)
plt.title("Content Ratings")
plt.xlabel("Number of Titles")

# Top 10 countries where it held
plt.subplot(3,2,3)
top_countries=netflix_clean_data["country"].value_counts().head(10)
ssn.barplot(x=top_countries.values,
            y=top_countries.index,
            palette="viridis",
            edgecolor="black",
            )
plt.xlim(0,4000)
plt.title("Top 10 Countries")
plt.xlabel("Number of Titles")
plt.ylabel("Country")

# top 10 genre
plt.subplot(3,2,4)
ssn.set_theme(style="darkgrid")
genre = netflix_clean_data["listed_in"].str.split(",").str[0]
top_genre = genre.value_counts().head(10)
ssn.barplot(
    x=top_genre.values,
    y=top_genre.index,
    palette="magma",
    edgecolor="black"
)
plt.title("Top 10 Genres")
plt.xlabel("Number of Titles")
plt.ylabel("Genre")

# release per year
plt.subplot(3,2,5)

release_year = (
    netflix_clean_data["release_year"]
    .value_counts()
    .sort_index()
)

ssn.lineplot(
    x=release_year.index,
    y=release_year.values,
    color="blue",
    marker=None,
    linewidth=2.5
)

plt.title("Content Released Per Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.grid(True, linestyle="--", alpha=0.3)

# Content addded per year to netflix
plt.subplot(3,2,6)
netflix_clean_data["added_year"] = netflix_clean_data["date_added"].dt.year
year=netflix_clean_data["added_year"].value_counts().sort_index()
ssn.lineplot(
    x=year.index,
    y=year.values,
    marker="o",
    color="green"
)
plt.title("Content Added to Netflix Per Year")
plt.xlabel("Year Added")
plt.ylabel("Number of Titles")
plt.grid(True, linestyle="--", alpha=0.3)

plt.tight_layout()
plt.subplots_adjust(hspace=0.6,wspace=0.35)
plt.savefig("netflix_dashboard.png",dpi=300,bbox_inches="tight")
plt.show()

print("Netflix Dashboard Imaged is stored successfully.")

